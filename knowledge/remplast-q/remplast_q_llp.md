# REMPLAST-Q LLP

```json
{
  "proyecto": {
    "meta": {
      "id": "remplast_q",
      "nombre": "REMPLAST-Q",
      "estado": "activo",
      "fecha": "2026-10-30",
      "responsable": "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA",
      "orcid": "0000-0001-8601-1963",
      "licencia": "CC BY 4.0",
      "schema": "llp.proyecto.v1.1",
      "tags": [
        "microplasticos",
        "edar",
        "lodos",
        "tratamiento",
        "aei_2026",
        "cc_by"
      ]
    },
    "objetivo": "Proponer un paquete abierto (CC BY 4.0) de detección y tratamiento de microplásticos en EDAR y lodos, para que lo ejecuten empresas y laboratorios preparados; el autor solo aporta información.",
    "datos_clave": {
      "paquete_publico": "/workspace/remplast_q_publico/",
      "paquete_zip": "/workspace/remplast_q_cc_by.zip",
      "knowledge": "knowledge/remplast-q/",
      "lora_pares": "knowledge/remplast-q/lora_pares.jsonl",
      "lora_pares_n": 78,
      "normativa": [
        "Directiva (UE) 2024/3019",
        "Decisión Delegada 2024/1441"
      ],
      "convocatoria": "AEI Proyectos de Generación de Conocimiento 2026",
      "cierre_aei": "2026-11-24T14:00:00+01:00",
      "rol_autor": "solo_propone_y_aporta_informacion",
      "contactados_2026_10_18": [
        "ICRA",
        "LEQUIA-UdG",
        "Cetaqua",
        "ICTA-UAB"
      ],
      "respuestas": {
        "ICRA": "declinado_2026_10_21",
        "LEQUIA-UdG": "sin_respuesta_a_2026_10_30",
        "Cetaqua": "sin_respuesta_a_2026_10_30",
        "ICTA-UAB": "sin_respuesta_a_2026_10_30"
      },
      "zenodo_record": "22341346",
      "zenodo_nota": "versión antigua con lista de grupos; subir CC BY como nueva versión PENDIENTE DE VERIFICACIÓN / acción manual",
      "drive": "17yHQXal0pbfUoGJkXsW_SHLdLWi-TVWr",
      "github": "canelonemf-byte/REMPLAST-Q",
      "ucs_ingesta": {
        "fecha": "2026-10-30",
        "prefijo": "remplast-q",
        "fragmentos_aprox": 256,
        "memory_total_tras": 1591,
        "omitido": [
          "correo_plantilla_grupo.md"
        ],
        "nota": "sin credenciales ni correos reales; costes/plan como documentación E2 no como experimento"
      }
    },
    "tareas": [
      {
        "id": "T01",
        "tarea": "Paquete público CC BY (revisión, lodos, costes, plan, borrador AEI)",
        "estado": "completado",
        "prioridad": "alta",
        "responsable": "REMPLAST-Q Agent",
        "fecha": "2026-10-20"
      },
      {
        "id": "T02",
        "tarea": "Contacto inicial a 4 entidades",
        "estado": "completado",
        "prioridad": "alta",
        "responsable": "REMPLAST-Q Agent",
        "fecha": "2026-10-18"
      },
      {
        "id": "T03",
        "tarea": "Vigilancia respuestas Gmail L-V 9:00 y 17:00 Madrid hasta 2026-11-24",
        "estado": "activo",
        "prioridad": "alta",
        "responsable": "routine remplast-q-respuestas-de-grupos-aei",
        "fecha": "2026-10-30"
      },
      {
        "id": "T04",
        "tarea": "78 pares LoRA adaptados a esquema FUSIÓN IA (sin fusionar)",
        "estado": "completado",
        "prioridad": "alta",
        "responsable": "REMPLAST-Q Agent",
        "fecha": "2026-10-30"
      },
      {
        "id": "T05",
        "tarea": "Actualizar JSON LLP remplast_q + originalidad + ingesta UCS",
        "estado": "completado",
        "prioridad": "alta",
        "responsable": "REMPLAST-Q Agent",
        "fecha": "2026-10-30"
      },
      {
        "id": "T06",
        "tarea": "Buscar otros grupos/empresas o vías de financiación; recordatorio a 3 sin respuesta tras aprobación del usuario",
        "estado": "pendiente",
        "prioridad": "alta",
        "responsable": "REMPLAST-Q Agent + usuario",
        "fecha": ""
      },
      {
        "id": "T07",
        "tarea": "Subir versión CC BY a Zenodo como nueva versión",
        "estado": "pendiente",
        "prioridad": "media",
        "responsable": "usuario (cuenta Zenodo)",
        "fecha": ""
      }
    ],
    "riesgos": [
      "Sin un doctor vinculado como IP no hay solicitud AEI",
      "Zenodo 22341346 aún con versión antigua que nombra grupos",
      "Plazo AEI 2026-11-24 14:00 Madrid",
      "ICRA declinó; 3 entidades sin respuesta a 2026-10-30",
      "Componentes tecnológicos (coagulación+arena/biochar; pirólisis de lodos) existen por separado en literatura/patentes; el paquete integrado propuesto no se ha encontrado como proyecto idéntico — PENDIENTE DE VERIFICACIÓN exhaustiva de patentes"
    ],
    "decisiones": [
      "Licencia CC BY 4.0; ejecutable sin el autor; solo pedir conocer el resultado",
      "No se envía CV",
      "En todo contacto: el autor solo propone y aporta información para empresas y laboratorios preparados",
      "Evidencia: E1 documental; E2 en costes/plan (estimaciones propias); sin datos experimentales (E0 de experimento)",
      "No fusionar ni entrenar LoRA ni publicar sin aprobación"
    ],
    "proximo_paso": "Buscar otros grupos/empresas o vías de financiación; con aprobación del usuario, dejar borrador de recordatorio a LEQUIA-UdG, Cetaqua e ICTA-UAB.",
    "fuentes": [
      "knowledge/remplast-q/fuentes_cc_by/",
      "/workspace/remplast_q_publico/",
      "/workspace/remplast_q_cc_by.zip"
    ],
    "evidencia_nivel": "E1",
    "evidencia_nota": "E1 = revisión documental y normativa citada. Costes y plan = E2 (estimaciones propias). Sin experimento propio (E0 experimental). Se conserva E1 como nivel documental verificado.",
    "alias": [
      "REMPLAST-Q",
      "remplast-q",
      "remplast_q"
    ],
    "drive_canonicos": [
      "17yHQXal0pbfUoGJkXsW_SHLdLWi-TVWr"
    ],
    "drive_duplicados": [],
    "originalidad": {
      "fecha_busqueda": "2026-10-30",
      "consulta": "tren terciario coagulación+arena con biochar + tratamiento de lodos para microplásticos en EDAR",
      "hallazgos": [
        {
          "tipo": "articulo",
          "titulo": "Coagulation + sand filtration for MPs (PFS+sand ~91%)",
          "url": "https://doi.org/10.1051/e3sconf/202459801005"
        },
        {
          "tipo": "articulo",
          "titulo": "SCG-biochar for small MPs in secondary effluent",
          "url": "https://www.sciencedirect.com/science/article/pii/S2214714425003423"
        },
        {
          "tipo": "articulo",
          "titulo": "Biochar layer in sand columns for MP removal",
          "url": "https://doi.org/10.1016/j.watres.2022.118783"
        },
        {
          "tipo": "proyecto",
          "titulo": "LIFE BIODAPH2O (Quart/Antissa; MP>90%; fin previsto ago 2026)",
          "url": "https://cwp.cat/es/noticias/life-biodaph2o-entra-en-su-fase-final-y-refuerza-el-potencial-de-la-naturaleza-para-eliminar-pfas-y-microplasticos-en-la-regeneracion-de-aguas-residuales/"
        },
        {
          "tipo": "patente",
          "titulo": "US 11795090 / 11434160 sludge pyrolysis (PFAS/plastics → biochar)",
          "url": "https://patents.google.com/?q=11795090"
        },
        {
          "tipo": "patente",
          "titulo": "WO2019215218A1 activated carbon + silsesquioxane for MP removal",
          "url": "https://patents.google.com/patent/WO2019215218A1/en"
        }
      ],
      "conclusion": "Hay trabajos y patentes sobre piezas sueltas (coagulación+arena, biochar en filtro, pirólisis de lodos, LIFE nature-based). No se ha localizado en esta búsqueda un proyecto/patente idéntico al paquete integrado REMPLAST-Q (revisión+lodos+costes+plan AEI CC BY). Conclusión prudente: originalidad documental del empaquetado; no reivindicar novedad tecnológica absoluta. PENDIENTE DE VERIFICACIÓN: barrido exhaustivo de patentes/Espacenet."
    }
  }
}
```
