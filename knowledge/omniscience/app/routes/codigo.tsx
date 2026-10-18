import { createFileRoute, Link } from "@tanstack/react-router";
import { Download, Play } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PySource } from "@/components/py-source";
import { runMv1Python } from "@/lib/run-python";
import { SCRIPTS, type ScriptId } from "@/lib/scripts";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/codigo")({ component: Codigo });

function Codigo() {
  const [id, setId] = useState<ScriptId>("mv1");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(true);
  const [jump, setJump] = useState<number | undefined>();
  const [running, setRunning] = useState(false);
  const [log, setLog] = useState<{ ok: boolean; stdout: string; stderr: string } | null>(null);

  const meta = useMemo(() => SCRIPTS.find((s) => s.id === id) ?? SCRIPTS[0], [id]);

  useEffect(() => {
    let live = true;
    setLoading(true);
    setSource("");
    setJump(undefined);
    setLog(null);
    fetch(meta.href)
      .then((r) => r.text())
      .then((t) => {
        if (live) setSource(t);
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
    };
  }, [meta.href]);

  const go = (line: number) => {
    setJump(line);
    document.getElementById(`L${line}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  const run = async () => {
    setRunning(true);
    setLog(null);
    try {
      const result = await runMv1Python();
      setLog(result);
    } catch (error) {
      setLog({ ok: false, stdout: "", stderr: error instanceof Error ? error.message : "falló la ejecución" });
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">Paquete unificado · código</p>
        <h1 className="mt-2 text-4xl">Explorar los scripts Python</h1>
        <p className="mt-3 max-w-prose text-muted">
          Los cuatro archivos del ZIP, con índice de funciones y fuente. El orquestador MV1 se puede
          ejecutar aquí: es el mismo algoritmo que la campaña, con numpy real. Los otros tres generan
          las figuras, la animación y el informe que ya están en el grafo.
        </p>
      </header>

      <div className="grid gap-3 md:grid-cols-2">
        {SCRIPTS.map((s) => (
          <button
            key={s.id}
            type="button"
            onClick={() => setId(s.id)}
            className={cn(
              "rounded-lg border p-4 text-left transition-colors min-h-11",
              s.id === id ? "border-accent bg-elevated" : "border-border bg-surface hover:border-accent/40",
            )}
          >
            <div className="flex items-center justify-between gap-2">
              <p className="font-mono text-sm">{s.file}</p>
              <Badge tone={s.runnable ? "ok" : "muted"}>{s.role}</Badge>
            </div>
            <p className="mt-2 text-sm text-muted">{s.summary}</p>
          </button>
        ))}
      </div>

      <Card className="flex flex-col gap-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="font-display text-2xl">{meta.file}</h2>
            <p className="mt-1 font-mono text-xs text-muted">
              {source ? `${source.split("\n").length} líneas` : `${meta.lines} líneas`} · {meta.deps}
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href={meta.href} download className={cn(buttonVariants({ variant: "secondary", size: "sm" }))}>
              <Download className="size-4" />
              Descargar
            </a>
            {meta.runnable ? (
              <Button size="sm" onClick={run} disabled={running}>
                <Play className="size-4" />
                {running ? "Ejecutando…" : "Ejecutar Si2"}
              </Button>
            ) : null}
          </div>
        </div>
        <p className="text-sm text-muted">{meta.summary}</p>
        <p className="font-mono text-[11px] text-accent">Produce: {meta.produces}</p>
      </Card>

      {log ? (
        <Card className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <h2 className="font-display text-xl">Salida de python3</h2>
            <Badge tone={log.ok ? "ok" : "danger"}>{log.ok ? "ok" : "error"}</Badge>
          </div>
          <pre className="overflow-x-auto whitespace-pre-wrap rounded-md border border-border bg-elevated p-3 font-mono text-[12px] text-fg">
            {[log.stdout, log.stderr].filter(Boolean).join("\n") || "(sin salida)"}
          </pre>
          <p className="text-xs text-muted">
            Caso de prueba del documento: CrystalStructure Si2, a = 5.4 Å. El 20 % de las superceldas
            dispara el fallback DFT (max |F| {'>'} 10 eV/Å). La campaña en el navegador usa el mismo
            contrato.{" "}
            <Link to="/campana" className="text-accent underline-offset-4 hover:underline">
              Abrir campaña
            </Link>
          </p>
        </Card>
      ) : null}

      {id === "anim" ? (
        <video
          className="w-full rounded-lg border border-border"
          src="/media/10_modos_cuerda_animacion.mp4"
          controls
          playsInline
          preload="metadata"
        />
      ) : null}

      <section>
        <h2 className="font-display text-xl">Símbolos</h2>
        <ul className="mt-3 grid gap-1">
          {meta.symbols.map((sym) => (
            <li key={sym.name}>
              <button
                type="button"
                onClick={() => go(sym.line)}
                className="flex min-h-11 w-full items-baseline justify-between gap-3 rounded-md px-2 text-left hover:bg-elevated"
              >
                <span>
                  <span className="font-mono text-xs text-accent">{sym.kind}</span>{" "}
                  <span className="font-mono text-sm">{sym.name}</span>
                  <span className="ml-2 text-sm text-muted">{sym.note}</span>
                </span>
                <span className="font-mono text-xs text-subtle">L{sym.line}</span>
              </button>
            </li>
          ))}
        </ul>
      </section>

      {loading ? (
        <p className="text-sm text-muted">Cargando fuente…</p>
      ) : (
        <PySource source={source} highlightLine={jump} />
      )}
    </div>
  );
}
