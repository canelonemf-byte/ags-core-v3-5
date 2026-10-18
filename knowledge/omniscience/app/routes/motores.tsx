import { createFileRoute, Link } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { ENGINES } from "@/lib/catalog";

export const Route = createFileRoute("/motores")({ component: Motores });

function Motores() {
  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">Núcleo científico</p>
        <h1 className="mt-2 text-4xl">Nueve motores, un orquestador</h1>
        <p className="mt-3 max-w-prose text-muted">
          Matter + Vibrational son el MVP. Quantum Dynamics espera la densidad espectral J(ω) del
          motor fonónico. Bio y fusión exigen aprobación humana antes de laboratorio.
        </p>
      </header>
      <div className="grid gap-4 md:grid-cols-2">
        {ENGINES.map((e) => (
          <Card key={e.id} className="flex flex-col gap-3">
            <div className="flex items-start justify-between gap-3">
              <h2 className="font-display text-2xl">{e.name}</h2>
              <Badge tone={e.id === "matter" || e.id === "vib" ? "ok" : "muted"}>{e.status}</Badge>
            </div>
            <p className="text-sm text-muted">{e.blurb}</p>
            <p className="font-mono text-xs text-accent">{e.eq}</p>
          </Card>
        ))}
      </div>
      <p className="text-sm text-muted">
        Para ejecutar el bucle Matter → Phonon con MLIP y DFT, abre{" "}
        <Link to="/campana" className="text-accent underline-offset-4 hover:underline">
          Campaña MV1
        </Link>
        . El SQL y el Python del documento técnico están en{" "}
        <Link to="/implementacion" className="text-accent underline-offset-4 hover:underline">
          implementación
        </Link>
        .
      </p>
    </div>
  );
}
