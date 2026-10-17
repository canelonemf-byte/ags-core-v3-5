> Texto extraído automáticamente del PDF original «REMPLAST-Q_FAT-SAT-001_RevA.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/16DK8n3eZoOdU16_kX6iEVCduogMQ1bfh/view?usp=drivesdk



REMPLAST-Q  ·  FAT-SAT-001  ·  Pruebas de taller y sede 1

Lázaro López Paz  ·  REMPLAST-Q  ·  Documento original  ·  Rev. A  2026-09-05

FAT-SAT-001 — Protocolo de pruebas de fábrica y de sede

Agua de red primero. Efluente real solo con actas S1–S8 firmadas.

FAT = en taller del integrador, con agua potable. SAT = contenedor ya anclado en la EDAR, todavía con agua de red
o efluente secundario solo cuando el titular lo autorice por escrito. Cada línea se marca PASA / FALLA / N/A. Tres
firmas: Promotor, integrador, interlocutor EDAR (esta última solo en SAT).

A. FAT — taller

ID Prueba Criterio P/F Iniciales

F1 Continuidad de tierra y diferencial 30 mA Dispara en ensayo

F2 Sentido de giro P-101 y P-301 a 20 Hz Sin cavitación 5 min

F3 Calibración PT-301/302/303 a 0 y 2 bar Error ≤ 1 % f.e.

F4 TMP calculada = diferencia leída Desvío ≤ 0,02 bar

F5 Integridad de membrana (punto de burbuja o
productor) Acta del módulo

F6 Curva J vs TMP con agua 20 °C, 3 m/s J limpia 250–450 LMH

F7 Secuencia backwash 30 s V-304 abre; Q inversa OK

F8 Receta CIP en seco (agua, sin NaOH) I-09 bloquea si V-401 abierta

F9 I-01 simulado (4 mA en LE-101) P-101 off, V-101 cierra <3 s+TON

F10 I-02 HH con calibrador en PT-301 HOLD del skid

F11 I-04 puerta SE-201 Láseres off; reset remoto denegado

F12 I-06 seta y corte magnetotérmico V-101 y V-401 cerradas <3 s

F13 Historiador 15 min P, Q, T, estados de válvula

F14 Fuga visual 1,5 × TMP de diseño, 30 min 0 gotas en uniones clamp

Tabla 4. FAT. Sin F5, F12 y F14 el contenedor no viaja.

B. SAT — sede EDAR

ID Prueba Criterio P/F Iniciales

S1 Repetir I-06 con la acometida real Mismo criterio F12

S2 I-07: desconectar Ethernet 9 s Aísla como I-06

S3 I-04 + intento de reset por VPN Denegado

S4 Llenar TK-401 hasta HH (I-08) Sin rebose de cubeto

S5 I-09 CIP vs V-401 V-601 no abre

S6 Historiador + hora NTP Marca de tiempo coherente

S7 Derivación: abrir V-101 2 min a Q mínima con retorno
autorizado Sin fugas en batería; EDAR estable

S8 72 h continuas agua de red o efluente según permiso Disponibilidad ≥ 90 %; first-out registrado

Tabla 5. SAT. S7 no se hace de noche ni un viernes sin interlocutor.

C. Acta tipo

Proyecto REMPLAST-Q · Documento FAT-SAT-001 · Fecha ____ / ____ / ______ · Lugar ______________ FAT /
SAT (táchese) · Resultado global: PASA / FALLA · First-out observado: I-__ · Desviaciones:
_______________________________________________________________ Firma Promotor _____________
Integrador _____________ EDAR (solo SAT) _____________

Texto original. No reproduce protocolos de integradores comerciales.
