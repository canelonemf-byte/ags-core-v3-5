import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { MATERIALS } from "@/lib/catalog";
import { runMv1, type CampaignResult } from "@/lib/mv1";
import { useCampaigns } from "@/lib/store";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/campana")({ component: Campana });

function Campana() {
  const [materialId, setMaterialId] = useState("Si");
  const [live, setLive] = useState<CampaignResult | null>(null);
  const [busy, setBusy] = useState(false);
  const addRun = useCampaigns((s) => s.addRun);
  const selected = MATERIALS.find((m) => m.id === materialId)!;

  async function launch() {
    if (busy) return;
    setBusy(true);
    const final = await runMv1(materialId, setLive);
    addRun(final);
    setBusy(false);
  }

  const freqData =
    live?.frequencies.map((f, i) => ({ i: i + 1, f: Number(f.toFixed(3)), imag: f < 0 })) ?? [];

  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">OMNISCIENCE-MV1</p>
        <h1 className="mt-2 text-4xl">Algoritmo maestro con validación adversarial</h1>
        <p className="mt-3 max-w-prose text-muted">
          El mismo algoritmo del PDF: normaliza, relaja, calcula Eform, genera superceldas y predice
          fuerzas con MLIP. Si max |F| {'>'} 10 eV/Å, invoca DFT. Luego diagonaliza D(q) y busca modos
          imaginarios. Surrogate en el navegador — no es VASP. Contrato y SQL en{" "}
          <Link to="/implementacion" className="text-accent underline-offset-4 hover:underline">
            implementación MV1
          </Link>
          .
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-[1fr_1.1fr]">
        <Card className="flex flex-col gap-4">
          <h2 className="font-display text-xl">Estructura inicial</h2>
          <div className="grid grid-cols-2 gap-2">
            {MATERIALS.map((m) => (
              <button
                key={m.id}
                type="button"
                onClick={() => setMaterialId(m.id)}
                className={cn(
                  "min-h-11 rounded-md border px-3 py-2 text-left text-sm transition-colors duration-150",
                  materialId === m.id
                    ? "border-accent bg-elevated text-fg"
                    : "border-border text-muted hover:text-fg",
                )}
              >
                {m.name}
              </button>
            ))}
          </div>
          <p className="text-sm text-muted">{selected.note}</p>
          <p className="font-mono text-xs text-subtle">
            Eform tabla = {selected.eform.toFixed(2)} eV/at · riesgo imaginario ={" "}
            {Math.round(selected.imagRisk * 100)}%
          </p>
          <Button onClick={launch} disabled={busy} className="min-h-12">
            {busy ? "Ejecutando…" : "Ejecutar campaña"}
          </Button>
        </Card>

        <Card className="flex min-h-72 flex-col gap-3">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-display text-xl">Trazas PROV-O</h2>
            {live && (
              <Badge
                tone={
                  live.status === "verified_prediction"
                    ? "ok"
                    : live.status === "falsified"
                      ? "danger"
                      : "warn"
                }
              >
                {live.status}
              </Badge>
            )}
          </div>
          {!live && <p className="text-sm text-muted">Aún no hay ejecución en esta sesión.</p>}
          <ol className="flex flex-col gap-2">
            {live?.steps.map((s, i) => (
              <li key={`${s.name}-${i}`} className="rounded-md border border-border bg-elevated px-3 py-2">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm">{s.name}</span>
                  <Badge
                    tone={s.status === "FAILED" ? "danger" : s.status === "REVISION" ? "warn" : "ok"}
                  >
                    {s.status}
                  </Badge>
                </div>
                <p className="mt-1 font-mono text-[11px] text-muted">{s.detail}</p>
              </li>
            ))}
          </ol>
        </Card>
      </div>

      {live && live.frequencies.length > 0 && (
        <Card>
          <h2 className="font-display text-xl">Espectro fonónico (surrogate)</h2>
          <p className="mt-1 text-sm text-muted">
            {live.imaginary} modos imaginarios · max |F| = {live.maxForce.toFixed(2)} eV/Å · DFT
            fallback {live.usedDft ? "sí" : "no"} · nivel {live.evidence}
          </p>
          <div className="mt-4 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={freqData}>
                <CartesianGrid stroke="var(--color-border)" vertical={false} />
                <XAxis dataKey="i" tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
                <YAxis
                  tick={{ fill: "var(--color-muted)", fontSize: 11 }}
                  label={{ value: "THz", angle: -90, fill: "var(--color-muted)" }}
                />
                <Tooltip
                  contentStyle={{
                    background: "var(--color-elevated)",
                    border: "1px solid var(--color-border)",
                    color: "var(--color-fg)",
                  }}
                />
                <Bar dataKey="f" fill="var(--color-accent)" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}
    </div>
  );
}
