import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { DocumentPack, FigureGallery } from "@/components/doc-pack";
import { ENGINES, EVIDENCE, PROJECTS } from "@/lib/catalog";

export const Route = createFileRoute("/proyectos")({ component: Proyectos });

function Proyectos() {
  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">Grafo de conocimiento</p>
        <h1 className="mt-2 text-4xl">El paquete unificado hereda a todas las líneas</h1>
        <p className="mt-3 max-w-prose text-muted">
          El ZIP (maestro PDF + LaTeX, informe C-VIB-001, figuras 01–12, Python de simulación y
          animación, MP4 de modos) queda enganchado a Helio-3, Drive, YIG, lentes, nanomedicina,
          CERO-A, C-VIB-001 y MV1. Nadie usa un modo o un gap sin ese banco y sin el régimen de
          evidencia.
        </p>
      </header>

      <section>
        <h2 className="font-display text-xl">Archivo completo</h2>
        <p className="mt-1 mb-3 text-sm text-muted">Descargas del paquete. El ZIP es la fuente; el resto son las piezas.</p>
        <DocumentPack highlight="dossier" />
      </section>

      <section>
        <h2 className="font-display text-xl">Figuras C-VIB-001</h2>
        <p className="mt-1 mb-3 text-sm text-muted">
          N3 = simulación verificada. N0 = ilustración, no dato. Las once imágenes del ZIP.
        </p>
        <FigureGallery />
      </section>

      <div className="grid gap-4 md:grid-cols-2">
        {PROJECTS.map((p) => {
          const ev = EVIDENCE[p.level];
          return (
            <Card key={p.id} className="flex flex-col gap-3">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-[0.14em] text-muted">{p.domain}</p>
                  <h2 className="mt-1 font-display text-2xl">{p.name}</h2>
                </div>
                <Badge tone={p.level >= 3 ? "ok" : p.level === 0 ? "muted" : "accent"}>
                  N{p.level} {ev.name}
                </Badge>
              </div>
              <p className="text-sm text-muted">{p.summary}</p>
              <p className="text-sm text-fg/80">{p.mv1}</p>
              <p className="font-mono text-[11px] text-accent">
                Hereda ZIP · maestro · TeX · C-VIB · MV1 · figs · MP4 · Python
              </p>
              <div className="flex flex-wrap gap-2">
                {p.engines.map((id) => {
                  const eng = ENGINES.find((e) => e.id === id);
                  return (
                    <Badge key={id} tone="muted">
                      {eng?.name ?? id}
                    </Badge>
                  );
                })}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
