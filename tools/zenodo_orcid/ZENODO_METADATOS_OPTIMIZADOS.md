# Metadatos Zenodo optimizados — 15 DOI

**Autor canónico (usar en todos):**    
Nombre: `López Paz, Lázaro`    
Afiliación: `Investigador independiente, El Prat de Llobregat, Barcelona, España`    
Idioma: `spa`    
Licencia por defecto documentos: `cc-by-4.0`    
No poner BIST, IN2UB, Peptides International, Fundación Medina ni Acoustic Metamaterials Group como *creator*. Si quieres citar un contexto, va en la descripción, no en el autor.

**Cómo aplicar (sin API):**    
Zenodo → record → *Edit* (lápiz) → guardar. En records publicados se pueden corregir título, autores, descripción, keywords, tipo y licencia. No hace falta versión nueva si no cambias ficheros.

**Relación entre records:** en *Related identifiers* añade `isPartOf` / `references` hacia los hermanos de la misma línea (ver bloque al final).

---

## Plantilla de descripción (copiar y rellenar)

```  
Documento de trabajo / nota técnica. Autor: Lázaro López Paz (El Prat de Llobregat).

Estado: [concepto | protocolo de laboratorio | modelo 0D | software]  
Evidencia en este depósito: [lista de ficheros útiles]  
No evidencia: ensayo clínico, vuelo, o resultado experimental no incluido aquí.

Uso: solo investigación y documentación. No es receta clínica ni manual de dispositivo médico.  
```

---

## Correcciones record a record

### 1. 10.5281/zenodo.20761277 — GlyD-QSense  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Expediente Técnico de Validación: Sistema de Termometría Cuántica Orgánica GlyD-QSense | GlyD-QSense: expediente técnico de termometría cuántica orgánica (glicina deuterada) |  
| Creador | Lázaro López Paz / Instituto de Investigaciones Químicas | López Paz, Lázaro — Independiente, El Prat de Llobregat *(quitar IIQ si no hay afiliación formal)* |  
| Tipo | Other | Technical note |  
| Licencia | apache2.0 | cc-by-4.0 |  
| Keywords | glicina | GlyD-QSense; termometría; glicina deuterada; sensor cuántico; nanocristales orgánicos |

Descripción corta: expediente + dossier de implementación de un *concepto* de sensor de temperatura en nanocristales de glicina deuterada. No es un instrumento calibrado publicado.

### 2. 10.5281/zenodo.20812704 — Neuro PK  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | (aceptable) | Sistemas de liberación controlada para enfermedades neurodegenerativas: protocolos de validación (Higuchi / Korsmeyer–Peppas) |  
| Creador | Fundación Medina (publicación: Lázaro…) | López Paz, Lázaro |  
| Tipo | Publication | Technical note |  
| Keywords | alzeimer | Alzheimer; Parkinson; liberación controlada; Higuchi; Korsmeyer-Peppas; BHE |

Descripción: capacidades de laboratorio y modelos PK. No hay resultado clínico en el depósito.

### 3. 10.5281/zenodo.21238123 — 6G / fractal  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Mata materiale y 6G y 7G- aislamiento cuántico | Metamateriales acústicos y fractales para aislamiento y enlaces 6G/7G: dossier conceptual |  
| Creador | Acoustic Metamaterials Group (China)/ Lázaro… | López Paz, Lázaro |  
| Keywords | Metamatariales | metamateriales; 6G; 7G; fractal; aislamiento acústico; CymaQuantum |

### 4. 10.5281/zenodo.21321630 — QSM  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Lubricación_articular_QuantumSynovia_MetaLub_(QSM) | Quantum Synovia Matrix (QSM / MetaLub): lubricación articular biomimética — tutorial técnico |  
| Tipo | (si Other) | Technical note |  
| Keywords | — | QSM; ácido hialurónico; DFT; tribología; osteoartritis; siloxano |

### 5. 10.5281/zenodo.21345185 — Fotónica fractal  
Título: `Ingeniería de sistemas fotónicos y metamateriales fractales: dossier de I+D`    
Keywords: `fotónica; metamateriales; fractal; hardware cuántico (concepto)`

### 6. 10.5281/zenodo.21361772 — Microbiota  
Título: `Plataforma Meta Nano Microbiota Quantum: CQDs, encapsulación y modelo gLV`    
Keywords: `microbiota; carbon quantum dots; alginato; quitosano; gLV; tributirina`    
Nota en descripción: los PDF de 3–6 KB (GMP / clínico / patente) son **borradores incompletos**, no un dossier regulatorio.

### 7. 10.5281/zenodo.21401153 — MEI-RIT  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Lo último en propulsión espacial | MEI-RIT: propulsor iónico de RF de yodo con metasuperficie — propuesta y verificación 2026 |  
| Tipo | Other / Publication | Technical note / Preprint |  
| Keywords | — | MEI-RIT; RF ion thruster; iodine; metasurface; CubeSat; electric propulsion |

Descripción: propuesta de 50–80 W, Isp 2300–2800 s, presupuesto 53–95 k€. Ancla en literatura ThrustMe/Busek. No hay hardware volado.

### 8. 10.5281/zenodo.21513673 — Canelone  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Software para ordenador cuántico dé hoy | Canelone_mf: software de investigación para circuitos cuánticos de pequeña escala |  
| Tipo | Other | Software |  
| Licencia | (si docs+código) | mit o apache-2.0 **solo si el .py es el objeto**; si no, cc-by-4.0 + nota |  
| Keywords | — | Qiskit; software; computación cuántica; Canelone_mf |

### 9. 10.5281/zenodo.21640446 — LCPB  
Título: `LCPB: marco computacional para índices biológicos en búsqueda de vida extrasolar`    
Keywords: `astrobiología; LCPB; exoplanetas; biosignature (modelo)`

### 10. 10.5281/zenodo.21721963 — Gravedad-tiempo  
Título: `Control espacio-tiempo cuántico: informe de viabilidad y límites (simulación Qiskit)`    
Keywords: `relatividad; Qiskit; YIG; gravitación (simulación); no CTC`    
Descripción obligatoria: el informe **descarta** control gravitatorio macroscópico y viaje al pasado. El depósito es simulación + marco conceptual.

### 11. 10.5281/zenodo.21806526 — Péptidos v3  
Título: `Péptidos inteligentes v3: NeuroPlastin, Senolyt-X e ImmuSynth — protocolos realizables en laboratorio`    
Keywords: `SPPS; AzoF; NeuroPlastin; senolíticos; péptidos`    
Licencia: cc-by-4.0

### 12. 10.5281/zenodo.22028729 — FMO-IA  
Título: `Hibridación FMO–HEOM–IA: atlas y pipeline de simulación`    
Keywords: `FMO; HEOM; fotosíntesis; machine learning; open quantum systems`

### 13. 10.5281/zenodo.22131030 — HelioAtlas  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Proyectos 26_8_2026_helio-3 | HelioAtlas 2026: catálogo conceptual de líneas de helio-3 (no es el modelo 0D QMC-H3) |  
| Creador | BIST (Lázaro…) | López Paz, Lázaro |  
| Licencia | apl1.0 | **cc-by-4.0** (APL no encaja) |  
| Tipo | Other | Other / Project deliverable |  
| Keywords | metamatariales | helio-3; HelioAtlas; fusión aneutrónica (concepto); regolito lunar |

Descripción: material de marca/catálogo. El balance 0D del reactor QMC-H3 (Q ≈ 0,04) **no** está en este DOI. Relacionar con un futuro depósito QMC-H3.

### 14. 10.5281/zenodo.22131440 — Péptidos IA (duplicado temático)  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Pedtidos realizados con inteligencia artificial | Arquitectura de péptidos terapéuticos asistida por IA (dossier v1.1 / addendum v1.2) |  
| Creador | Peptides International (United States) (Lázaro…) | López Paz, Lázaro |  
| Licencia | apache2.0 | cc-by-4.0 |  
| Keywords | pedtidos | péptidos; diseño asistido por IA; SPPS |

Related identifier: `isNewVersionOf` o `references` → 10.5281/zenodo.21806526 (v3 realizable).    
Quitar `noteboo.txt` en una versión nueva si no aporta.

### 15. 10.5281/zenodo.22150378 — OMNISCIENCE  
| Campo | Ahora | Propuesto |  
|---|---|---|  
| Título | Vibración proyectos cuánticos | OMNISCIENCE MVP: plataforma de descubrimiento científico (implementación técnica + maestro) |  
| Creador | IN2UB (Lázaro…) | López Paz, Lázaro |  
| Tipo | Presentation | Software o Other |  
| Licencia | (vacía) | cc-by-4.0 |  
| Keywords | vibración | OMNISCIENCE; plataforma científica; MVP |

El ZIP de 172 MB (`grok-workspace-2.zip`) no debe ser el objeto principal del metadato. Describir: «el anexo ZIP es workspace de trabajo, no el entregable».

---

## Identificadores relacionados (red)

En cada record, bloque *Related identifiers* (tipo `doi`, relación `references` o `isPartOf`):

```  
colección portfolio 2026:  
20761277, 20812704, 21238123, 21321630, 21345185, 21361772,  
21401153, 21513673, 21640446, 21721963, 21806526, 22028729,  
22131030, 22131440, 22150378  
```

Pares útiles:  
- 21806526 ↔ 22131440 (péptidos)  
- 22131030 → futuro QMC-H3  
- 21401153 (MEI-RIT) ↔ 22131030 solo como «mismo autor», no como mismo aparato  
- 21721963 no hereda claims de IQM-He3-Anti (ese DOI aún no existe)

URL de perfil (opcional, `isIdenticalTo` no; usa `isDocumentedBy` o simple URL en descripción):    
---

## Orden de edición (15–25 min)

1. Los 6 con **autor-institución falso** (20812704, 21238123, 22131030, 22131440, 22150378, y revisar 20761277/IIQ).    
2. Títulos con falta de ortografía.    
3. Licencias raras (APL, Apache en PDFs).    
4. Keywords.    
5. Descripción de 5–8 líneas + disclaimer de evidencia.    
6. Related identifiers.

## Lo que no cambia el DOI

Corregir metadatos **no** emite un DOI nuevo. Si sustituyes ficheros (quitar `noteboo.txt`, añadir la nota QMC-H3), entonces **New version** → `10.5281/zenodo.XXXX` con `concept DOI` estable (`conceptrecid` ya listado arriba).  
