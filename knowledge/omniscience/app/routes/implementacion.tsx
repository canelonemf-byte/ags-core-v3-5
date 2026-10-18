import { createFileRoute, Link } from "@tanstack/react-router";
import { Download } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { DocumentPack } from "@/components/doc-pack";
import { PROJECTS } from "@/lib/catalog";
import { DOCUMENTS, PIPELINE, SQL_DDL, SQL_TABLES } from "@/lib/schema";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/implementacion")({ component: Implementacion });

function Implementacion() {
  return (
    <div className="flex flex-col gap-10">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">Documento maestro de implementación</p>
        <h1 className="mt-2 max-w-3xl text-4xl">OMNISCIENCE-MV1, unido al paquete y a cada línea</h1>
        <p className="mt-4 max-w-prose text-muted">
          El PDF de implementación, el ZIP unificado, el maestro LaTeX/PDF, C-VIB-001 y el Python
          adversarial son un solo contrato. Lo heredan Helio-3, el Drive, YIG, las lentes y la
          nanomedicina. Surrogate en el navegador; el código es el del documento, listo para ASE /
          Phonopy / VASP.{" "}
          <Link to="/codigo" className="text-accent underline-offset-4 hover:underline">
            Explorar los scripts
          </Link>
          .
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          {DOCUMENTS.filter((d) => ["pack", "mv1", "maestro", "tex", "py"].includes(d.id)).map((d) => (
            <a
              key={d.id}
              href={d.href}
              download
              className={cn(buttonVariants({ variant: d.id === "pack" || d.id === "mv1" ? "primary" : "secondary" }))}
            >
              <Download className="size-4" />
              {d.short}
            </a>
          ))}
        </div>
      </header>

      <section>
        <h2 className="text-2xl">Paquete unificado (todos los documentos)</h2>
        <p className="mt-2 mb-4 max-w-prose text-sm text-muted">
          Piezas del ZIP más el PDF MV1. Cada proyecto de la lista inferior las hereda.
        </p>
        <DocumentPack highlight="pack" />
      </section>

      <section>
        <h2 className="text-2xl">Los cuatro pasos del orquestador</h2>
        <ol className="mt-4 grid gap-3 md:grid-cols-2">
          {PIPELINE.map((p) => (
            <li key={p.n} className="rounded-lg border border-border bg-surface p-4">
              <p className="font-mono text-xs text-accent">{p.n}</p>
              <h3 className="mt-1 font-display text-xl">{p.title}</h3>
              <p className="mt-2 text-sm text-muted">{p.body}</p>
            </li>
          ))}
        </ol>
        <p className="mt-4 text-sm text-muted">
          Criterio adversarial del PDF: si el tensor MLIP tiene max |F| {'>'} 10 eV/Å, se marca REVISION
          y se sustituye por DFT. Eform ≥ 0 o modos imaginarios cierran la campaña como{" "}
          <span className="font-mono text-danger">falsified</span>.
        </p>
      </section>

      <section>
        <h2 className="text-2xl">Esquema relacional W3C PROV-O</h2>
        <p className="mt-2 max-w-prose text-sm text-muted">
          Cuatro tablas. Cada campaña escribe actividades; cada predicción o estructura es una
          entidad; el humano y los motores son agentes; wasGeneratedBy cierra la procedencia.
        </p>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {SQL_TABLES.map((t) => (
            <Card key={t.name} className="flex flex-col gap-3">
              <div>
                <p className="font-mono text-sm text-accent">{t.name}</p>
                <p className="text-xs text-muted">{t.purpose}</p>
              </div>
              <ul className="grid gap-1">
                {t.columns.map((c) => (
                  <li key={c.name} className="flex justify-between gap-3 border-t border-border pt-1 font-mono text-[11px]">
                    <span>{c.name}</span>
                    <span className="text-muted">
                      {c.type} · {c.note}
                    </span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>
        <pre className="mt-4 overflow-x-auto rounded-lg border border-border bg-elevated p-4 font-mono text-[11px] leading-relaxed text-muted">
          {SQL_DDL}
        </pre>
      </section>

      <section>
        <h2 className="text-2xl">Cómo hereda cada proyecto este archivo</h2>
        <div className="mt-4 grid gap-3">
          {PROJECTS.map((p) => (
            <article key={p.id} className="rounded-lg border border-border bg-surface px-4 py-3">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="font-display text-lg">{p.name}</h3>
                <Badge tone={p.level >= 3 ? "ok" : p.level === 0 ? "muted" : "accent"}>N{p.level}</Badge>
              </div>
              <p className="mt-1 text-sm text-muted">{p.mv1}</p>
              <p className="mt-1 font-mono text-[11px] text-accent">Paquete unificado heredado</p>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl">Contrato Python</h2>
        <p className="mt-2 max-w-prose text-sm text-muted">
          CrystalStructure, ProvenanceRecord, UniversalMatterEngine, VibrationalPhononEngine,
          OmniscienceMV1Workflow. Caso de prueba del PDF: Si2, a = 5.4 Å. El banco de modos está en{" "}
          <Link to="/vibraciones" className="text-accent underline-offset-4 hover:underline">
            vibraciones
          </Link>{" "}
          y el bucle en{" "}
          <Link to="/campana" className="text-accent underline-offset-4 hover:underline">
            campaña
          </Link>
          .
        </p>
      </section>
    </div>
  );
}
