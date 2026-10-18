import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EVIDENCE, ENGINES, PROJECTS } from "@/lib/catalog";
import { useCampaigns } from "@/lib/store";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  const runs = useCampaigns((s) => s.runs);
  const last = runs[0];

  return (
    <div className="flex flex-col gap-10">
      <section className="grid gap-8 md:grid-cols-[1.4fr_1fr] md:items-end">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-accent">Documento vivo · agosto 2026</p>
          <h1 className="mt-3 max-w-xl text-4xl text-fg md:text-5xl">
            Descubrir es sobrevivir a la refutación.
          </h1>
          <p className="mt-4 max-w-prose text-muted">
            OMNISCIENCE no responde en un chat. Formula hipótesis falsables, ejecuta materia y
            fonones, registra procedencia PROV-O y clasifica cada afirmación por nivel de evidencia.
            El ZIP unificado (maestro, LaTeX, C-VIB-001, figuras, Python, animación) y el PDF MV1
            quedan heredados por todas las líneas de invención.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <a href="/docs/OMNISCIENCE_dossier_completo.pdf" download className={cn(buttonVariants())}>
              Descargar dossier completo
              <ArrowRight className="size-4" />
            </a>
            <Link to="/proyectos" className={cn(buttonVariants({ variant: "secondary" }))}>
              Ver paquete en proyectos
            </Link>
            <Link to="/implementacion" className={cn(buttonVariants({ variant: "secondary" }))}>
              Implementación MV1
            </Link>
            <Link to="/vibraciones" className={cn(buttonVariants({ variant: "secondary" }))}>
              C-VIB-001
            </Link>
          </div>
        </div>
        <Card className="rounded-xl p-5">
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Última campaña</p>
          <p className="mt-2 font-display text-2xl">{last?.id ?? "—"}</p>
          <p className="mt-1 text-sm text-muted">{last?.materialName}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            <Badge tone={last?.status === "verified_prediction" ? "ok" : last?.status === "falsified" ? "danger" : "muted"}>
              {last?.status === "verified_prediction" ? "verificada" : last?.status === "falsified" ? "falsada" : "—"}
            </Badge>
            <Badge tone="accent">nivel {last?.evidence ?? "—"}</Badge>
          </div>
          <p className="mt-4 font-mono text-xs text-subtle">{runs.length} registros en procedencia local</p>
        </Card>
      </section>

      <section>
        <h2 className="text-2xl">Niveles de evidencia</h2>
        <p className="mt-2 max-w-prose text-sm text-muted">
          Nada es un descubrimiento hasta el intento explícito de refutación. C-VIB-001 y MV1 viven en
          el nivel 3: simulación verificada, no laboratorio.
        </p>
        <ol className="mt-5 grid gap-2 sm:grid-cols-2 lg:grid-cols-7">
          {EVIDENCE.map((e) => (
            <li key={e.level} className="rounded-lg border border-border bg-elevated px-3 py-3">
              <p className="font-mono text-xs text-accent">N{e.level}</p>
              <p className="mt-1 text-sm font-medium">{e.name}</p>
              <p className="mt-1 text-xs text-muted">{e.meaning}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Card>
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Motores</p>
          <p className="mt-2 font-display text-4xl tabular-nums">{ENGINES.length}</p>
          <p className="mt-2 text-sm text-muted">Matter y Phonon están cableados. El resto tiene contrato de interfaz.</p>
        </Card>
        <Card>
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Proyectos unidos</p>
          <p className="mt-2 font-display text-4xl tabular-nums">{PROJECTS.length}</p>
          <p className="mt-2 text-sm text-muted">Helio-3, Drive, YIG, lentes, nanomedicina, C-VIB-001.</p>
        </Card>
        <Card>
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Falsación</p>
          <p className="mt-2 font-display text-4xl tabular-nums">{"z > 3"}</p>
          <p className="mt-2 text-sm text-muted">
            Más Eform ≥ 0, |F| MLIP {">"} 10 eV/Å y modos imaginarios.
          </p>
        </Card>
      </section>

      <section>
        <h2 className="text-2xl">Ciclo maestro</h2>
        <p className="mt-3 max-w-4xl font-display text-lg leading-snug text-fg/90">
          Problema → Hipótesis → Predicción → Simulación → Falsación → Réplica → Conocimiento
        </p>
        <p className="mt-3 max-w-prose text-sm text-muted">
          El orquestador MV1 evalúa tensores de fuerza del MLIP en tiempo de ejecución. Si detecta
          anomalías, descarta la inferencia y ejecuta el fallback Ab Initio. Eso es la pieza que el
          documento de implementación añade a todo lo anterior.
        </p>
      </section>
    </div>
  );
}
