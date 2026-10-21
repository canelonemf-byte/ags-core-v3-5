# Correcciones propuestas para las webs (2026-10-21)

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. CC BY 4.0.
**Estado:** solo propuesta. No se ha desplegado nada. No hay código fuente local de estas webs en el box (búsqueda en /workspace sin resultados): las edita el usuario en Grok App Builder.

## Lo que se encontró al descargarlas (14:02, hora de Madrid, HTML servido; las vistas que se pintan con JavaScript no se revisaron)
| web | E-niveles visibles | aviso de simulado | "built with Grok" |
|---|---|---|---|
| NNC Consola (https://quartz-trail-summit-turbo.grok.me) | "Aritmética E3 · evento E0 · FANI confirmado prohibido" | No hay aviso general. Sí aparece "Sin hardware no hay NNC real" y la fila `sim_42ms` | No está en el HTML. La plataforma inyecta `grok.com/grok-app-builder/extensions.js` con un botón "Remix" |
| Búsqueda de anomalías (https://drift-hazel-urban-dawn.grok.me) | "E0 evento, E3 aritmética" y "No es el índice E0–E6" | No hay aviso general | Igual: botón inyectado por la plataforma |

**Nota importante:** en el HTML actual no aparece ninguna insignia "E6". El "E6" que detectó la rutina de X (`niveles_web:["E0","E3","E6"]`) seguramente sale de la frase "No es el índice E0–E6" (falso positivo). Si hay una insignia E6 en alguna vista que se pinta con JavaScript: PENDIENTE DE VERIFICACIÓN (abrir la web en el navegador). Si la hay, se aplica la corrección 1.

## Texto de reemplazo exacto

### 1. Insignia de evidencia (solo si se ve "E6" aplicado a la detección)
Reemplazar por:
> **Detección: E1** (método descrito y programado; sin validación experimental propia). Aritmética: E3. Eventos: E0.

### 2. Aviso de datos simulados (añadir arriba, visible, en las dos webs)
> ⚠️ **Aviso:** parte de los datos de esta página son **simulados o de demostración** (por ejemplo, `sim_42ms`) y se mezclan con fuentes públicas en tiempo real (ADS-B, TLE, MET Norway, AIS). Ningún resultado de esta página es una detección confirmada. Escala de evidencia E0–E6: detección E1.

### 3. Autoría (pie de página, en las dos webs)
> © 2026 Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Software MIT · Documentación CC BY 4.0. Alojado en Grok App Builder (grok.me).

El botón "Remix"/marca de la plataforma lo inyecta grok.com y quizá no se puede quitar desde el proyecto (PENDIENTE DE VERIFICACIÓN en los ajustes de Grok App Builder). El pie de autoría deja clara la autoría aunque el botón siga.

### Instrucción para pegar en Grok App Builder (cada web)
> Añade arriba del todo un aviso visible con este texto exacto: «[texto 2]». Añade un pie de página con este texto exacto: «[texto 3]». Si alguna insignia muestra E6 para la detección, cámbiala por «[texto 1]». No cambies nada más.
