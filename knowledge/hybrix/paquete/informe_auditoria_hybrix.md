# Auditoría Técnica, Evaluación de Seguridad y Refactorización del Sistema HYBRIX Orchestration API

## 1. Marco de Evaluación y Estado del Sistema

La API de Orquestación HYBRIX constituye la plataforma central para el registro de telemetría de matrices biológicas, el seguimiento de inferencias de modelos de inteligencia artificial y la detección de deriva estadística en ensayos biotecnológicos. Construida sobre FastAPI y Pydantic v2 en Python 3.12, la aplicación gestiona flujos continuos de datos mediante estructuras estructuradas de telemetría y predicciones.

La evaluación técnica llevada a cabo sobre la base de código examinó el modelo de concurrencia, los mecanismos de persistencia en disco, el esquema de autenticación y las herramientas de automatización integradas en el script de orquestación `scripts/hybrix.sh`. A través de la ejecución de una suite de pruebas automatizadas con el marco `unittest` y la clase `TestClient` de FastAPI, se validaron tanto las operaciones nominales como las condiciones límite del sistema.

| Componente | Tecnología Base | Versión Evaluada | Función Principal |
|---|---|---|---|
| Core API | FastAPI / Pydantic v2 | 1.8.1 -> 1.9.0 | Ingesta, validación y consulta de telemetría y predicciones |
| Orquestador | Bash (Shell Scripting) | POSIX / Bash 4+ | Despliegue, pruebas de humo, exportación CSV y verificación |
| Concurrencia | Python `threading.RLock` | Nativo 3.12 | Exclusión mutua en la manipulación del estado en memoria |
| Persistencia | JSON atómico con `os.replace` | Persistencia atómica | Almacenamiento persistente en sistema de archivos local |

---

## 2. Hallazgos Críticos y Diagnóstico Técnico

El análisis estático y dinámico del código original reveló tres vulnerabilidades arquitectónicas que comprometían la integridad operacional y la trazabilidad de las mediciones biológicas.

### 2.1 Pérdida de Datos por Persistencia Diferida en el Ciclo de Vida

En la versión original 1.8.1 de `main.py`, la persistencia del estado en disco mediante la función `_guardar_estado()` estaba delegada exclusivamente a la finalización del gestor de contexto asíncrono `lifespan`. Bajo esta arquitectura, las peticiones HTTP `POST` entrantes modificaban únicamente el diccionario en memoria `app.state.db`.

Ante una interrupción no planificada del proceso —causada por un fallo eléctrico, una excepción no capturada en el nivel del sistema operativo o la recepción de una señal `SIGKILL`— todos los registros de telemetría y predicción ingresados durante la sesión se perdían irremediablemente. Para un sistema que procesa datos de sensores biológicos y electrodos activos, esta volatilidad representa un riesgo operacional inaceptable.

### 2.2 Purga Silenciosa de Registros por Límite de Capacidad

El control de capacidad de almacenamiento en memoria utilizaba la constante `HYBRIX_MAX_RECORDS` (con valor por defecto de 100,000 registros). Al alcanzar dicha capacidad, la función interna `_append()` recortaba la lista mediante la instrucción slicing `del collection[:excess]`.

Esta purga se realizaba de manera completamente silenciosa: no generaba ningún registro en los diarios de auditoría (`logging`), ni incrementaba contadores numéricos de descarte. En consecuencia, al exportar el histórico a CSV mediante `export_hybrix_csv.sh`, los usuarios analistas obtenían un conjunto incompleto de ensayos sin ninguna advertencia del sistema sobre la pérdida de datos históricos.

### 2.3 Desprotección en los Endpoints de Consulta e Inspección

La función de seguridad `require_api_key` estaba configurada como dependencia obligatoria exclusivamente en los métodos `POST` y `DELETE`. Los endpoints de consulta `GET /api/v1/hybrix/telemetry` y `GET /api/v1/hybrix/predictions` carecían de verificación de credenciales. Si bien esto facilitaba la conexión directa del panel de control web (`dashboard.html`), exponía las lecturas viables y las predicciones de los electrodos a cualquier cliente de red con acceso al puerto de la API.

---

## 3. Arquitectura y Refactorizaciones Aplicadas

Para corregir de forma definitiva las deficiencias detectadas, se desarrolló e implementó la versión 1.9.0 de `main.py`, incorporando un diseño defensivo mejorado sin alterar la compatibilidad con el ecosistema de scripts existente.

```
Petición Cliente (POST / DELETE)
       │
       ▼
[ Validante Pydantic v2 ]
       │
       ▼
[ Control de Acceso: require_api_key ]
       │
       ▼
[ Adquisición de Cerrojo: threading.RLock ]
       │
       ├─► Inserción en memoria y verificación MAX_RECORDS
       │     └─► Si hay exceso: Purga + Registro en log + Incremento de contador
       │
       └─► Persistencia Síncrona (_persist_if_configured)
             └─► JSON Temporal -> os.replace() atómico -> Disk (hybrix_api_state.json)
```

### 3.1 Persistencia Síncrona Configurable (`HYBRIX_SYNC_ON_WRITE`)

Se introdujo el mecanismo `_persist_if_configured()`, controlado por la variable de entorno `HYBRIX_SYNC_ON_WRITE` (activa por defecto con el valor `1`). Cada vez que se procesa exitosamente un registro individual o un lote mediante los endpoints de inserción o eliminación, el sistema invoca de forma inmediata la función de escritura atómica `_guardar_estado()`.

Este cambio garantiza que la persistencia en disco ocurra en tiempo real al recibir cada medición:

$$T_{\text{persistencia}} = T_{\text{recepción}} + \Delta t_{\text{I/O}}$$

De esta forma, en caso de fallo crítico del servidor, los datos confirmados previamente mediante códigos de respuesta HTTP `201 Created` quedan resguardados en el archivo `hybrix_api_state.json`.

### 3.2 Trazabilidad de Purgas y Métricas de Rendimiento

Se reestructuró la función `_append()` para supervisar de forma activa el volumen de descartes. Al superar el límite `MAX_RECORDS`, el sistema realiza tres acciones simultáneas:

1. Trunca los registros más antiguos respetando el límite máximo asignado.
2. Incrementa el contador acumulativo `purged_telemetry` o `purged_predictions` dentro del estado global de la aplicación.
3. Emite un mensaje de advertencia estructurado a través del módulo `logging.logger.warning`, indicando el número exacto de elementos eliminados y el total histórico purgado.

Asimismo, el endpoint `GET /api/v1/hybrix/status` fue ampliado para ofrecer una visión completa de la salud del almacenamiento:

```json
{
  "status": "online",
  "timestamp": "2026-10-31T18:45:00Z",
  "records_telemetry": 100000,
  "records_predictions": 100000,
  "purged_telemetry": 150,
  "purged_predictions": 0,
  "sync_on_write": true,
  "last_saved_at": "2026-10-31T18:44:59Z"
}
```

### 3.3 Autenticación de Lectura Opcional (`HYBRIX_REQUIRE_READ_AUTH`)

Se añadió la dependencia `require_read_api_key`, que permite activar la validación de clave de API en los endpoints `GET` configurando la variable de entorno `HYBRIX_REQUIRE_READ_AUTH=1`. Esta mejora permite a los administradores restringir el acceso a las consultas en entornos de producción expuestos a redes compartidas.

---

## 4. Suite de Pruebas y Resultados de Verificación

La validación funcional y de regresión se ejecutó en el entorno local utilizando el módulo `unittest` de Python y la herramienta `TestClient` provista por FastAPI. Se diseñaron escenarios específicos para poner a prueba los límites de capacidad y la resiliencia del almacenamiento.

| ID de Prueba | Escenario de Prueba | Resultado Esperado | Estado |
|---|---|---|---|
| `TEST-01` | Verificación de Estado (`GET /status`) | Código 200, retorne "online" y contadores en 0 | PASS |
| `TEST-02` | Rechazo de Autenticación | Código 401 ante clave ausente o incorrecta en POST | PASS |
| `TEST-03` | Ingesta y Consulta de Telemetría | Código 201 en inserción, recuperable vía GET | PASS |
| `TEST-04` | Persistencia Inmediata (`SYNC_ON_WRITE`) | Confirmación de escritura física en archivo `.json` | PASS |
| `TEST-05` | Control de Purga (`MAX_RECORDS`) | Incremento exacto del contador de registros purgados | PASS |
| `TEST-06` | Borrado Administrativo de Datos | Código 200 con `confirm=true`, vaciado de colecciones | PASS |

Todos los experimentos ejecutados en la suite automatizada arrojaron una tasa de éxito del 100%, confirmando que las refactorizaciones mantienen la compatibilidad total y resuelven las fallas identificadas.

---

## 5. Guía de Operación y Recomendaciones de Seguridad

Para desplegar la versión refactorizada de la API HYBRIX en entornos de producción o laboratorio, se recomienda aplicar el siguiente procedimiento estandarizado:

### 5.1 Configuración de Variables de Entorno

Antes de iniciar el servicio, establezca las variables de entorno para garantizar la máxima seguridad y persistencia:

```bash
export HYBRIX_API_KEY="clave-segura-generada-de-al-menos-32-caracteres"
export HYBRIX_PORT="8000"
export HYBRIX_MAX_RECORDS="200000"
export HYBRIX_SYNC_ON_WRITE="1"
export HYBRIX_REQUIRE_READ_AUTH="1"
```

### 5.2 Comandos de Ejecución y Monitoreo

El script de gestión `scripts/hybrix.sh` permite automatizar las tareas operativas habituales:

1. **Ejecutar la suite completa de verificación:**
   ```bash
   bash scripts/hybrix.sh verificar
   ```
2. **Iniciar el servidor API en modo seguro:**
   ```bash
   bash scripts/hybrix.sh arrancar
   ```
3. **Exportar datos e informe de deriva estadística:**
   ```bash
   bash scripts/hybrix.sh exportar
   ```

Con estas mejoras implementadas, el sistema HYBRIX Orchestration API alcanza una arquitectura sólida, tolerante a fallos y preparada para gestionar telemetría biológica crítica de forma transparente e ininterrumpida.
