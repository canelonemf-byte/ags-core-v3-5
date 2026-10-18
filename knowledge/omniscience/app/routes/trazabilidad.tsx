import { createFileRoute, Link } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AGENTS } from "@/lib/catalog";
import { SQL_TABLES } from "@/lib/schema";
import { useCampaigns } from "@/lib/store";

export const Route = createFileRoute("/trazabilidad")({ component: Trazabilidad });

function Trazabilidad() {
  const runs = useCampaigns((s) => s.runs);
  const clearRuns = useCampaigns((s) => s.clearRuns);

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-accent">W3C PROV-O</p>
          <h1 className="mt-2 text-4xl">Registro de procedencia</h1>
          <p className="mt-3 max-w-prose text-muted">
            El SQL del PDF MV1 se materializa aquí: entidad, agente, actividad y wasGeneratedBy. Cada
            campaña escribe pasos SUCCESS / REVISION / FAILED. C-VIB-001 no se borra. Esquema
            completo en{" "}
            <Link to="/implementacion" className="text-accent underline-offset-4 hover:underline">
              implementación
            </Link>
            .
          </p>
        </div>
        <Button variant="secondary" onClick={clearRuns}>
          Vaciar derivadas
        </Button>
      </header>

      <section>
        <h2 className="font-display text-xl">Tablas del PDF</h2>
        <ul className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
          {SQL_TABLES.map((t) => (
            <li key={t.name} className="rounded-md border border-border bg-surface px-3 py-3">
              <p className="font-mono text-[11px] text-accent">{t.name}</p>
              <p className="mt-1 text-xs text-muted">{t.purpose}</p>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="font-display text-xl">Agentes</h2>
        <ul className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {AGENTS.map((a) => (
            <li key={a.id} className="rounded-md border border-border bg-surface px-3 py-3">
              <p className="font-mono text-[11px] text-accent">{a.id}</p>
              <p className="text-sm">{a.name}</p>
              <p className="text-xs text-muted">{a.type}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className="flex flex-col gap-3">
        <h2 className="font-display text-xl">Actividades y wasGeneratedBy</h2>
        {runs.map((r) => (
          <Card key={r.id} className="flex flex-col gap-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <p className="font-mono text-xs text-muted">{r.id}</p>
                <p className="font-display text-xl">{r.materialName}</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge tone={r.status === "verified_prediction" ? "ok" : r.status === "falsified" ? "danger" : "warn"}>
                  {r.status}
                </Badge>
                <Badge tone="accent">nivel {r.evidence}</Badge>
                {r.usedDft && <Badge tone="warn">DFT fallback</Badge>}
              </div>
            </div>
            <p className="font-mono text-[11px] text-muted">
              entity {r.materialId} ← activity {r.id}
            </p>
            <ol className="grid gap-1">
              {r.steps.map((s, i) => (
                <li
                  key={`${r.id}-${i}`}
                  className="flex flex-wrap items-baseline justify-between gap-2 border-t border-border pt-2 text-sm"
                >
                  <span>{s.name}</span>
                  <span className="font-mono text-[11px] text-muted">
                    {s.agent} · {s.status}
                  </span>
                </li>
              ))}
            </ol>
          </Card>
        ))}
      </section>
    </div>
  );
}
