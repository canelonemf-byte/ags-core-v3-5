#!/usr/bin/env python3
"""
Proyecto Integrador de Conocimiento - MetaNanoMicrobiota Quantum + Todos los Proyectos Anteriores
Creado para Lázaro López Paz

Este script permite:
1. Almacenar de forma estructurada todos los proyectos (este y los anteriores)
2. Buscar y relacionar proyectos por tecnologías, fórmulas, aplicaciones, etc.
3. Generar reportes integrados
4. Exportar a formatos útiles (JSON, Markdown, etc.)
5. Servir como base para publicar en bases de datos / repositorios (GitHub, arXiv, wiki personal, etc.)

Uso:
- Ejecutar el script
- Añadir proyectos nuevos
- Buscar conexiones entre proyectos
- Generar resúmenes integrados

Autor: Asistente Grok + Lázaro López Paz
Fecha: Julio 2026
"""

import sqlite3
import json
import datetime
from typing import List, Dict, Optional

DB_NAME = "proyectos_lazaro_lopez_paz.db"

def create_database():
    """Crea la base de datos y las tablas principales si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabla principal de proyectos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            tecnologias TEXT,           -- JSON array: ["nanotecnologia", "metamateriales", "IA", ...]
            formulas_clave TEXT,        -- JSON array de fórmulas o ecuaciones principales
            aplicaciones TEXT,          -- JSON array: ["salud intestinal", "fusion", "mineria lunar", ...]
            estado TEXT,                -- "concepto", "simulacion", "prototipo", "patente", "ensayo_clinico"
            documentos TEXT,            -- JSON array de rutas o enlaces a PDFs, código, etc.
            fecha_creacion TEXT,
            notas TEXT
        )
    ''')

    # Tabla de conexiones entre proyectos (grafo de conocimiento)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conexiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_origen_id INTEGER,
            proyecto_destino_id INTEGER,
            tipo_conexion TEXT,         -- "comparte_tecnologia", "aplicacion_comun", "sinergia_potencial", "misma_linea_investigacion"
            descripcion TEXT,
            fuerza INTEGER DEFAULT 5,   -- 1-10
            FOREIGN KEY (proyecto_origen_id) REFERENCES proyectos(id),
            FOREIGN KEY (proyecto_destino_id) REFERENCES proyectos(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos creada/actualizada correctamente.")

def add_project(titulo: str, descripcion: str, tecnologias: List[str], 
                formulas_clave: List[str], aplicaciones: List[str], 
                estado: str, documentos: List[str] = None, notas: str = "") -> int:
    """Añade un nuevo proyecto a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.datetime.now().isoformat()

    cursor.execute('''
        INSERT INTO proyectos 
        (titulo, descripcion, tecnologias, formulas_clave, aplicaciones, estado, documentos, fecha_creacion, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        titulo,
        descripcion,
        json.dumps(tecnologias),
        json.dumps(formulas_clave),
        json.dumps(aplicaciones),
        estado,
        json.dumps(documentos or []),
        now,
        notas
    ))

    project_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"Proyecto '{titulo}' añadido con ID: {project_id}")
    return project_id

def search_projects(query: str) -> List[Dict]:
    """Busca proyectos que coincidan con la consulta (en título, descripción, tecnologías o aplicaciones)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query_lower = f"%{query.lower()}%"

    cursor.execute('''
        SELECT id, titulo, descripcion, tecnologias, aplicaciones, estado 
        FROM proyectos 
        WHERE LOWER(titulo) LIKE ? 
           OR LOWER(descripcion) LIKE ?
           OR LOWER(tecnologias) LIKE ?
           OR LOWER(aplicaciones) LIKE ?
    ''', (query_lower, query_lower, query_lower, query_lower))

    results = []
    for row in cursor.fetchall():
        results.append({
            "id": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "tecnologias": json.loads(row[3]),
            "aplicaciones": json.loads(row[4]),
            "estado": row[5]
        })

    conn.close()
    return results

def find_connections(project_id: int) -> List[Dict]:
    """Encuentra proyectos relacionados con uno dado."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p2.id, p2.titulo, c.tipo_conexion, c.descripcion, c.fuerza
        FROM conexiones c
        JOIN proyectos p2 ON (c.proyecto_destino_id = p2.id OR c.proyecto_origen_id = p2.id)
        WHERE (c.proyecto_origen_id = ? OR c.proyecto_destino_id = ?)
          AND p2.id != ?
    ''', (project_id, project_id, project_id))

    results = []
    for row in cursor.fetchall():
        results.append({
            "proyecto_id": row[0],
            "titulo": row[1],
            "tipo_conexion": row[2],
            "descripcion": row[3],
            "fuerza": row[4]
        })

    conn.close()
    return results

def generate_integrated_report() -> str:
    """Genera un reporte integrado de todos los proyectos y sus conexiones."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM proyectos")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT titulo, estado FROM proyectos ORDER BY fecha_creacion DESC")
    projects = cursor.fetchall()

    report = f"""
# REPORTE INTEGRADO DE PROYECTOS - Lázaro López Paz
**Fecha:** {datetime.datetime.now().strftime('%Y-%m-%d')}
**Total de proyectos registrados:** {total_projects}

## Lista de Proyectos

"""
    for titulo, estado in projects:
        report += f"- **{titulo}** — Estado: {estado}\n"

    report += "\n## Conexiones Principales Detectadas\n"
    # Aquí se podrían añadir más análisis automáticos

    report += """
## Recomendaciones de Integración

1. Publicar el documento maestro en GitHub + Zenodo (DOI)
2. Subir resúmenes a arXiv / ResearchGate
3. Crear wiki personal o Notion database
4. Usar este script como base de un sistema RAG local (con embeddings)

---
*Generado automáticamente por el Project Integrator de Lázaro López Paz*
"""
    conn.close()
    return report

# ============================================================
# INICIALIZACIÓN CON PROYECTOS CONOCIDOS (ejemplos)
# ============================================================

def initialize_with_known_projects():
    """Añade el proyecto actual y proyectos anteriores conocidos del usuario."""
    print("\nInicializando con proyectos conocidos...")

    # === PROYECTO ACTUAL ===
    add_project(
        titulo="MetaNanoMicrobiota Quantum",
        descripcion="Plataforma integral para optimización de la microbiota intestinal mediante nanotecnología de delivery dirigido (alginato-quitosano + tributirina + minerales), IA de personalización y modelo matemático gLV. Incluye protocolos GMP, estudio clínico piloto y borrador de patente.",
        tecnologias=["nanotecnologia", "metamateriales", "inteligencia_artificial", "modelado_matematico", "postbioticos", "nanomedicina"],
        formulas_clave=[
            "Modelo gLV: dN_i/dt = r_i N_i (1 - sum alpha_ij N_j / K_i) + I_i(t)",
            "Tributirina: C15H26O6",
            "Alginato + Quitosano + Eudragit S100 (pH-responsive)"
        ],
        aplicaciones=["salud_intestinal", "modulacion_microbioma", "nanomedicina_personalizada", "eje_intestino_cerebro"],
        estado="implementacion_completa",
        documentos=[
            "Final_Implementation_Package_MetaNanoMicrobiota_Quantum.pdf",
            "Patent_Draft_MetaNanoMicrobiota_Quantum_Full.pdf",
            "MetaNanoMicrobiota_Quantum_Presentacion.pptx",
            "project_integrator.py"
        ],
        notas="Proyecto principal 2026. Integra nanotecnología avanzada, IA y modelado matemático. Incluye presentación con imágenes Unreal Engine 6."
    )

    # === PROYECTOS ANTERIORES CONOCIDOS ===
    add_project(
        titulo="Helium-3 Lunar Mining Robotic Systems",
        descripcion="Sistemas robóticos autónomos y conceptos integrales para extracción de Helio-3 en la Luna, incluyendo viabilidad técnica, económica, patentes y comparativas estratégicas con otras fuentes de energía.",
        tecnologias=["robotica_espacial", "mineria_lunar", "energia_nuclear", "patentes", "sistemas_autonomos"],
        formulas_clave=["Modelos de viabilidad energética y económica de extracción de He-3", "Ecuaciones de rendimiento de minería robótica"],
        aplicaciones=["energia_fusion", "mineria_espacial", "geopolitica_energetica", "colonizacion_lunar"],
        estado="concepto_avanzado_con_patentes",
        documentos=["Documentos de viabilidad, estudios de factibilidad y borradores de patente"],
        notas="Proyecto recurrente y de alta prioridad del usuario."
    )

    add_project(
        titulo="Quantum Metamaterials for Fusion Reactors and Artificial Gravity",
        descripcion="Diseño y simulación de metamateriales cuánticos (YIG, BN-He3 hybrids, auxéticos, etc.) para reactores de fusión, generación de gravedad artificial y otras aplicaciones avanzadas en energía y espacio.",
        tecnologias=["metamateriales_cuanticos", "fusion_nuclear", "gravedad_artificial", "simulaciones_DFT", "nanotecnologia"],
        formulas_clave=["Simulaciones DFT para interacción material-campo", "Modelos de permeabilidad magnética y gravito-magnética"],
        aplicaciones=["energia_fusion", "propulsion_espacial", "habitats_espaciales", "tecnologia_espacial"],
        estado="investigacion_avanzada_y_simulacion",
        documentos=["Múltiples documentos LaTeX, simulaciones y estudios de viabilidad"],
        notas="Línea principal de investigación del usuario en metamateriales cuánticos."
    )

    add_project(
        titulo="Nanomedicina Cuántica para Enfermedades Neurodegenerativas y Articulaciones",
        descripcion="Desarrollo de plataformas nanotecnológicas y cuánticas para tratamiento de Parkinson, Alzheimer, y terapias biomiméticas para articulaciones (lubricantes cuánticos de hialurónico, parches MetaNO, etc.).",
        tecnologias=["nanomedicina", "metamateriales_cuanticos", "biomimetica", "liberacion_dirigida", "terapias_personalizadas"],
        formulas_clave=["Diseño molecular de transportadores y moléculas activas (NO, etc.)", "Modelos de interacción nanopartícula-tejido"],
        aplicaciones=["enfermedades_neurodegenerativas", "salud_articular", "terapias_personalizadas", "nanomedicina_regenerativa"],
        estado="investigacion_y_desarrollo",
        documentos=["Protocolos de síntesis, estudios de viabilidad y documentos técnicos"],
        notas="Línea importante de nanomedicina del usuario con múltiples aplicaciones de salud."
    )

    print("\nProyectos iniciales añadidos correctamente (4 proyectos).")

# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROJECT INTEGRATOR - Lázaro López Paz")
    print("Sistema de integración de todos tus proyectos")
    print("=" * 60)

    create_database()

    # Inicializar con proyectos conocidos (solo la primera vez)
    # Comenta esta línea después de la primera ejecución si no quieres duplicados
    initialize_with_known_projects()

    print("\n--- Menú de opciones ---")
    print("1. Buscar proyectos")
    print("2. Ver conexiones de un proyecto")
    print("3. Generar reporte integrado")
    print("4. Añadir nuevo proyecto manualmente")
    print("5. Salir")

    while True:
        choice = input("\nElige una opción (1-5): ").strip()

        if choice == "1":
            q = input("Introduce término de búsqueda: ")
            results = search_projects(q)
            for r in results:
                print(f"\n[{r['id']}] {r['titulo']}")
                print(f"   Estado: {r['estado']}")
                print(f"   Tecnologías: {', '.join(r['tecnologias'])}")

        elif choice == "2":
            pid = int(input("ID del proyecto: "))
            conns = find_connections(pid)
            for c in conns:
                print(f"- {c['titulo']} | {c['tipo_conexion']} (fuerza: {c['fuerza']})")

        elif choice == "3":
            report = generate_integrated_report()
            print(report)
            with open("reporte_integrado_proyectos.md", "w", encoding="utf-8") as f:
                f.write(report)
            print("\nReporte guardado en 'reporte_integrado_proyectos.md'")

        elif choice == "4":
            titulo = input("Título del nuevo proyecto: ")
            desc = input("Descripción breve: ")
            tech = input("Tecnologías (separadas por coma): ").split(",")
            formulas = input("Fórmulas clave (separadas por | ): ").split("|")
            apps = input("Aplicaciones (separadas por coma): ").split(",")
            estado = input("Estado actual: ")
            add_project(titulo, desc, [t.strip() for t in tech], 
                       [f.strip() for f in formulas], [a.strip() for a in apps], estado)

        elif choice == "5":
            print("¡Hasta pronto! Todo tu conocimiento está ahora integrado y accesible.")
            break

        else:
            print("Opción no válida.")
