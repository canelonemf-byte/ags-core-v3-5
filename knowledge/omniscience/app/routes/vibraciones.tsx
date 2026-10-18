import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card } from "@/components/ui/card";
import { FigureGallery } from "@/components/doc-pack";
import { buttonVariants } from "@/components/ui/button";
import {
  chirpSignal,
  dampedFree,
  dftMag,
  linspace,
  phononDiatomic,
  phononMono,
  qhoPsi,
  resonanceAmp,
} from "@/lib/physics";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/vibraciones")({ component: Vibraciones });

function Vibraciones() {
  const [zeta, setZeta] = useState(0.08);

  const free = useMemo(() => {
    const omega0 = 2 * Math.PI * 0.8;
    return linspace(0, 12, 240).map((t) => ({
      t: Number(t.toFixed(2)),
      x: dampedFree(t, omega0, zeta),
    }));
  }, [zeta]);

  const res = useMemo(() => {
    const omega0 = 1;
    return linspace(0.2, 2.2, 160).map((w) => ({
      r: Number(w.toFixed(2)),
      a: resonanceAmp(w, omega0, zeta),
    }));
  }, [zeta]);

  const disp = useMemo(() => {
    return linspace(-Math.PI, Math.PI, 120).map((ka) => {
      const d = phononDiatomic(ka);
      return {
        k: Number((ka / Math.PI).toFixed(3)),
        mono: phononMono(ka),
        ac: d.ac,
        op: d.op,
      };
    });
  }, []);

  const fft = useMemo(() => {
    const sig = chirpSignal(256);
    const mag = dftMag(sig);
    const max = Math.max(...mag, 1e-9);
    return mag.slice(0, 80).map((m, i) => ({ f: i, m: m / max }));
  }, []);

  const qho = useMemo(() => {
    return linspace(-4.2, 4.2, 160).map((x) => ({
      x: Number(x.toFixed(2)),
      n0: qhoPsi(0, x) ** 2,
      n1: qhoPsi(1, x) ** 2,
      n2: qhoPsi(2, x) ** 2,
    }));
  }, []);

  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">C-VIB-001 · nivel 3</p>
        <h1 className="mt-2 text-4xl">Motor vibracional en vivo</h1>
        <p className="mt-3 max-w-prose text-muted">
          Banco de calibración del paquete unificado: oscilador, resonancia, FFT, dispersión 1D, QHO,
          figuras archivadas y la animación modal. H1–H6 no quedan falsadas aquí. No sustituye Phonopy
          ni un Raman de lote. Heredado por todas las líneas del grafo.
        </p>
        <div className="mt-4 flex flex-wrap gap-3">
          <a href="/code/simular_vibraciones.py" download className={cn(buttonVariants({ variant: "secondary" }))}>
            simular_vibraciones.py
          </a>
          <a href="/code/animar_modos.py" download className={cn(buttonVariants({ variant: "secondary" }))}>
            animar_modos.py
          </a>
          <a href="/media/10_modos_cuerda_animacion.mp4" download className={cn(buttonVariants({ variant: "secondary" }))}>
            Animación MP4
          </a>
        </div>
      </header>

      <Card>
        <h2 className="font-display text-xl">Animación modal (archivo 10 del ZIP)</h2>
        <p className="mt-1 text-sm text-muted">
          Superposición de modos de cuerda, 6 s. Artefacto de procedencia, no adorno.
        </p>
        <video
          className="mt-4 w-full rounded-md border border-border"
          src="/media/10_modos_cuerda_animacion.mp4"
          controls
          playsInline
          preload="metadata"
        />
      </Card>

      <Card>
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="font-display text-xl">Amortiguamiento ζ</h2>
            <p className="text-sm text-muted">Q ≈ 1/(2ζ) en el régimen subamortiguado.</p>
          </div>
          <label className="flex min-h-11 items-center gap-3 text-sm">
            <span className="font-mono tabular-nums text-accent">{zeta.toFixed(2)}</span>
            <input
              type="range"
              min={0}
              max={1.2}
              step={0.01}
              value={zeta}
              onChange={(e) => setZeta(Number(e.target.value))}
              className="w-44 accent-accent"
            />
          </label>
        </div>
        <div className="mt-5 grid gap-6 md:grid-cols-2">
          <ChartBlock title="Respuesta libre" data={free} x="t" y="x" yLabel="x(t)" />
          <ChartBlock title="Resonancia" data={res} x="r" y="a" yLabel="A(ω)" />
        </div>
      </Card>

      <Card>
        <h2 className="font-display text-xl">Dispersión Born–von Karman</h2>
        <p className="mt-1 text-sm text-muted">
          Monoatómica y diatómica (m2/m1 = 2.2). El gap óptico–acústico es el primer bandgap de la
          naturaleza.
        </p>
        <div className="mt-4 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={disp}>
              <CartesianGrid stroke="var(--color-border)" />
              <XAxis dataKey="k" tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
              <YAxis tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  background: "var(--color-elevated)",
                  border: "1px solid var(--color-border)",
                  color: "var(--color-fg)",
                }}
              />
              <Line type="monotone" dataKey="mono" stroke="var(--color-muted)" dot={false} strokeWidth={1.5} />
              <Line type="monotone" dataKey="ac" stroke="var(--color-accent)" dot={false} strokeWidth={2} />
              <Line type="monotone" dataKey="op" stroke="var(--color-fg)" dot={false} strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <h2 className="font-display text-xl">FFT del chirp</h2>
          <div className="mt-4 h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={fft}>
                <CartesianGrid stroke="var(--color-border)" />
                <XAxis dataKey="f" tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
                <YAxis tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
                <Line type="monotone" dataKey="m" stroke="var(--color-accent)" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card>
          <h2 className="font-display text-xl">QHO |ψn|²</h2>
          <div className="mt-4 h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={qho}>
                <CartesianGrid stroke="var(--color-border)" />
                <XAxis dataKey="x" tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
                <YAxis tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
                <Line type="monotone" dataKey="n0" stroke="var(--color-accent)" dot={false} />
                <Line type="monotone" dataKey="n1" stroke="var(--color-fg)" dot={false} />
                <Line type="monotone" dataKey="n2" stroke="var(--color-muted)" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <section>
        <h2 className="font-display text-2xl">Figuras del paquete unificado</h2>
        <p className="mt-2 mb-4 text-sm text-muted">
          Las mismas del ZIP. N3 verificada; N0 ilustración. Aplican a YIG, lentes, Drive y el resto
          como oráculo barato, no como medida.
        </p>
        <FigureGallery />
      </section>
    </div>
  );
}

function ChartBlock({
  title,
  data,
  x,
  y,
  yLabel,
}: {
  title: string;
  data: Record<string, number>[];
  x: string;
  y: string;
  yLabel: string;
}) {
  return (
    <div>
      <h3 className="text-sm font-medium">{title}</h3>
      <div className="mt-2 h-48">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="var(--color-border)" />
            <XAxis dataKey={x} tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
            <YAxis tick={{ fill: "var(--color-muted)", fontSize: 11 }} />
            <Line type="monotone" dataKey={y} name={yLabel} stroke="var(--color-accent)" dot={false} strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
