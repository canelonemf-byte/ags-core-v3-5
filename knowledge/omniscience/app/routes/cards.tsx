import { createFileRoute } from "@tanstack/react-router";
import { Check, Copy, Image as ImageIcon } from "lucide-react";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { JSONLD_TYPES, jsonLdNodes, jsonLdString } from "@/lib/jsonld";
import { SAFE_FORMATS, lockupFits, type SafeFormat } from "@/lib/safe-zones";
import {
  ALT,
  BANNER_PATH,
  CARD_KIND,
  CARD_KINDS,
  DESCRIPTION,
  IMAGE_PATH,
  LIMITS,
  PLATFORMS,
  TITLE,
  charCount,
  compareRows,
  ogSnippet,
  tagSnippet,
  twitterTags,
  withinLimit,
  type CardKind,
} from "@/lib/twitter-cards";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/cards")({ component: Cards });

function Cards() {
  const tags = useMemo(() => twitterTags(), []);
  const rows = useMemo(() => compareRows(), []);
  const snippet = useMemo(() => tagSnippet(tags), [tags]);
  const og = useMemo(() => ogSnippet(), []);
  const [kind, setKind] = useState<CardKind>(CARD_KIND);
  const [view, setView] = useState<"compare" | "twitter" | "jsonld" | "stories">("stories");
  const [copied, setCopied] = useState<"og" | "tw" | "ld" | null>(null);
  const ld = useMemo(() => jsonLdString(), []);
  const nodes = useMemo(() => jsonLdNodes(), []);

  const copy = async (which: "og" | "tw" | "ld") => {
    const text = which === "og" ? og : which === "tw" ? snippet : ld;
    try {
      await navigator.clipboard.writeText(text);
      setCopied(which);
      window.setTimeout(() => setCopied(null), 1600);
    } catch {
      setCopied(null);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">Compartir · OG · X · JSON-LD · Stories</p>
        <h1 className="mt-2 text-4xl">Metadatos de descubrimiento</h1>
        <p className="mt-3 max-w-prose text-muted">
          Open Graph para LinkedIn y Facebook, Twitter Cards para X, JSON-LD para buscadores, y
          cubiertas 9:16 con zona segura para Stories.
        </p>
      </header>

      <div className="flex flex-wrap gap-2">
        {(
          [
            ["compare", "Comparar"],
            ["twitter", "Solo X"],
            ["jsonld", "JSON-LD"],
            ["stories", "Zonas"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            onClick={() => setView(id)}
            className={cn(
              "min-h-11 rounded-md border px-3 text-sm transition-colors",
              view === id ? "border-accent bg-elevated text-fg" : "border-border text-muted hover:text-fg",
            )}
          >
            {label}
          </button>
        ))}
      </div>

      {view === "compare" ? (
        <CompareView rows={rows} og={og} tw={snippet} copied={copied} onCopy={copy} />
      ) : view === "jsonld" ? (
        <JsonLdView nodes={nodes} ld={ld} copied={copied === "ld"} onCopy={() => copy("ld")} />
      ) : view === "stories" ? (
        <StoriesView />
      ) : (
        <TwitterView
          kind={kind}
          setKind={setKind}
          tags={tags}
          snippet={snippet}
          copied={copied === "tw"}
          onCopy={() => copy("tw")}
        />
      )}
    </div>
  );
}

function StoriesView() {
  const [id, setId] = useState("tiktok");
  const [dim, setDim] = useState(true);
  const [chrome, setChrome] = useState(true);
  const format = SAFE_FORMATS.find((f) => f.id === id) ?? SAFE_FORMATS[0];
  const { w, h } = format.canvas;
  const phone =
    format.chrome === "stories" ||
    format.chrome === "reels" ||
    format.chrome === "tiktok" ||
    format.chrome === "feed";
  const fits = lockupFits(format);

  return (
    <div className="flex flex-col gap-8">
      <header>
        <p className="text-xs uppercase tracking-[0.2em] text-accent">Recortes · overlays · lockup</p>
        <h2 className="mt-2 font-display text-3xl">Zonas seguras</h2>
        <p className="mt-3 max-w-prose text-muted">
          Cada red tapa o recorta un borde distinto. El título de OMNISCIENCE solo es seguro si cabe
          en la intersección de todas esas ventanas.
        </p>
      </header>

      <div className="flex flex-wrap gap-2">
        {SAFE_FORMATS.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setId(item.id)}
            className={cn(
              "min-h-11 rounded-md border px-3 text-sm transition-colors",
              item.id === id ? "border-accent bg-elevated text-fg" : "border-border text-muted hover:text-fg",
            )}
          >
            {item.label}
            <span className="ml-2 text-subtle">
              {item.canvas.w}×{item.canvas.h}
            </span>
          </button>
        ))}
      </div>

      <div className={cn("grid gap-8 lg:items-start", phone ? "lg:grid-cols-[minmax(0,18rem)_1fr]" : "lg:grid-cols-[minmax(0,28rem)_1fr]")}>
        <SafeFrame format={format} dim={dim} chrome={chrome} compact={phone} />
        <div className="flex flex-col gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone={fits ? "ok" : "danger"}>{fits ? "lockup dentro" : "lockup recortado"}</Badge>
            <Button variant="secondary" size="sm" onClick={() => setDim((v) => !v)}>
              {dim ? "Quitar atenuado" : "Atenuar bordes"}
            </Button>
            <Button variant="secondary" size="sm" onClick={() => setChrome((v) => !v)}>
              {chrome ? "Quitar UI" : "Ver UI"}
            </Button>
          </div>
          <p className="text-sm text-muted">{format.note}</p>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[28rem] text-left text-sm">
              <thead className="text-xs uppercase tracking-[0.12em] text-muted">
                <tr>
                  <th className="pb-2 font-medium">Zona</th>
                  <th className="pb-2 font-medium">Medida</th>
                  <th className="pb-2 font-medium">Qué la ocupa</th>
                </tr>
              </thead>
              <tbody>
                {format.zones.map((zone) => (
                  <tr key={zone.name} className="border-t border-border align-top">
                    <td className="py-3 text-fg">{zone.name}</td>
                    <td className="py-3 font-mono text-accent">{zone.measure}</td>
                    <td className="py-3 text-muted">{zone.contains}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="font-mono text-xs text-subtle">
            lienzo {w}×{h} · top {format.top} · bottom {format.bottom} · left {format.left} · right{" "}
            {format.right}
            {format.centerSquare ? " · recorte 1:1 centrado" : ""}
          </p>
        </div>
      </div>
    </div>
  );
}

function SafeFrame({
  format,
  dim,
  chrome,
  compact,
}: {
  format: SafeFormat;
  dim: boolean;
  chrome: boolean;
  compact: boolean;
}) {
  const { w, h } = format.canvas;
  const top = (format.top / h) * 100;
  const bottom = (format.bottom / h) * 100;
  const left = (format.left / w) * 100;
  const right = (format.right / w) * 100;
  const squareInset = ((h - w) / 2 / h) * 100;

  return (
    <div className={cn("mx-auto w-full", compact ? "max-w-xs" : "max-w-md")}>
      <div className="relative overflow-hidden rounded-xl border border-border bg-ink shadow-[var(--shadow-panel)]">
        <img src={format.src} alt={format.alt} width={w} height={h} className="block w-full" />

        {dim ? (
          <>
            <div className="pointer-events-none absolute inset-x-0 top-0 bg-ink/70" style={{ height: `${top}%` }} />
            <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-ink/70" style={{ height: `${bottom}%` }} />
            <div
              className="pointer-events-none absolute top-0 bg-ink/70"
              style={{ left: 0, width: `${left}%`, top: `${top}%`, bottom: `${bottom}%` }}
            />
            <div
              className="pointer-events-none absolute top-0 bg-ink/70"
              style={{ right: 0, width: `${right}%`, top: `${top}%`, bottom: `${bottom}%` }}
            />
            <div
              className="pointer-events-none absolute border border-dashed border-accent/70"
              style={{ top: `${top}%`, bottom: `${bottom}%`, left: `${left}%`, right: `${right}%` }}
            />
          </>
        ) : null}

        {format.centerSquare && dim ? (
          <div
            className="pointer-events-none absolute inset-x-0 border-y border-dashed border-warn/80"
            style={{ top: `${squareInset}%`, bottom: `${squareInset}%` }}
          />
        ) : null}

        <div
          className="pointer-events-none absolute border border-accent"
          style={{
            left: `${(format.lockup.x / w) * 100}%`,
            top: `${(format.lockup.y / h) * 100}%`,
            width: `${(format.lockup.w / w) * 100}%`,
            height: `${(format.lockup.h / h) * 100}%`,
          }}
        />

        {chrome && format.chrome === "stories" ? <StoriesChrome /> : null}
        {chrome && format.chrome === "reels" ? <ReelsChrome /> : null}
        {chrome && format.chrome === "tiktok" ? <TikTokChrome /> : null}
        {chrome && format.chrome === "feed" ? <FeedChrome /> : null}
        {chrome && format.chrome === "og" ? <OgChrome /> : null}
        {chrome && format.chrome === "x" ? <XChrome /> : null}
      </div>
    </div>
  );
}

function StoriesChrome() {
  return (
    <>
      <div className="pointer-events-none absolute inset-x-3 top-3 flex flex-col gap-2">
        <div className="flex gap-1">
          <span className="h-0.5 flex-1 rounded-full bg-paper" />
          <span className="h-0.5 flex-1 rounded-full bg-paper/30" />
          <span className="h-0.5 flex-1 rounded-full bg-paper/30" />
        </div>
        <div className="flex items-center gap-2">
          <span className="size-8 rounded-full border border-accent/50 bg-elevated" />
          <span>
            <span className="block text-xs font-medium text-paper">OMNISCIENCE</span>
            <span className="block text-xs text-paper/70">ahora</span>
          </span>
        </div>
      </div>
      <div className="absolute inset-x-3 bottom-3">
        <div className="rounded-full border border-paper/30 bg-ink/60 px-4 py-2.5 text-sm text-paper/80">
          Enviar mensaje
        </div>
      </div>
    </>
  );
}

function ReelsChrome() {
  return (
    <>
      <div className="pointer-events-none absolute right-2 bottom-24 flex flex-col items-center gap-4">
        {["me gusta", "comentar", "enviar", "guardar"].map((label) => (
          <span key={label} className="flex flex-col items-center gap-1">
            <span className="size-9 rounded-full border border-paper/40 bg-ink/50" />
            <span className="text-xs text-paper/80">{label}</span>
          </span>
        ))}
      </div>
      <div className="absolute inset-x-3 bottom-3 max-w-[70%]">
        <p className="text-xs font-medium text-paper">@omniscience</p>
        <p className="mt-1 line-clamp-2 text-xs text-paper/80">Materia y fonones · evidencia PROV-O</p>
      </div>
    </>
  );
}

function TikTokChrome() {
  return (
    <>
      <div className="pointer-events-none absolute inset-x-0 top-3 flex justify-center gap-4 text-sm">
        <span className="text-paper/50">Siguiendo</span>
        <span className="border-b border-paper pb-0.5 font-medium text-paper">Para ti</span>
      </div>
      <div className="pointer-events-none absolute right-2 bottom-28 flex flex-col items-center gap-4">
        <span className="size-10 rounded-full border border-accent bg-elevated" />
        {["me gusta", "comentar", "guardar", "enviar"].map((label) => (
          <span key={label} className="flex flex-col items-center gap-1">
            <span className="size-9 rounded-full border border-paper/40 bg-ink/50" />
            <span className="text-xs text-paper/80">{label}</span>
          </span>
        ))}
        <span className="size-9 rounded-full border border-accent/60 bg-elevated" />
      </div>
      <div className="absolute inset-x-3 bottom-10 max-w-[70%]">
        <p className="text-sm font-medium text-paper">@omniscience</p>
        <p className="mt-1 line-clamp-2 text-xs text-paper/80">Materia y fonones · evidencia PROV-O</p>
        <p className="mt-2 text-xs text-paper/60">sonido original · OMNISCIENCE</p>
      </div>
    </>
  );
}

function FeedChrome() {
  return (
    <div className="absolute inset-x-0 bottom-0 border-t border-border bg-ink/80 px-3 py-2">
      <p className="text-xs text-muted">perfil recorta al cuadrado · feed muestra 4:5</p>
    </div>
  );
}

function OgChrome() {
  return (
    <div className="absolute inset-x-0 bottom-0 border-t border-border bg-elevated/95 px-4 py-3">
      <p className="text-xs uppercase tracking-[0.14em] text-subtle">dominio al publicar</p>
      <p className="font-display text-lg text-fg">OMNISCIENCE</p>
    </div>
  );
}

function XChrome() {
  return (
    <div className="absolute inset-x-0 bottom-0 border-t border-border bg-elevated/95 px-4 py-3">
      <p className="text-xs uppercase tracking-[0.14em] text-subtle">summary_large_image</p>
      <p className="font-display text-lg text-fg">OMNISCIENCE</p>
    </div>
  );
}

function JsonLdView({
  nodes,
  ld,
  copied,
  onCopy,
}: {
  nodes: ReturnType<typeof jsonLdNodes>;
  ld: string;
  copied: boolean;
  onCopy: () => void;
}) {
  return (
    <>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {JSONLD_TYPES.map((item) => (
          <Card key={item.id} className="p-4">
            <p className="font-mono text-sm text-accent">{item.id}</p>
            <p className="mt-2 font-display text-xl">{item.role}</p>
            <p className="mt-1 text-sm text-muted">{item.note}</p>
          </Card>
        ))}
      </div>
      <Card>
        <h2 className="font-display text-2xl">Grafo @graph</h2>
        <p className="mt-1 text-sm text-muted">
          Va en el HTML como <span className="font-mono text-fg">script type="application/ld+json"</span>.
          Google, Bing y asistentes lo leen; LinkedIn y X no.
        </p>
        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[36rem] text-left text-sm">
            <thead className="text-xs uppercase tracking-[0.12em] text-muted">
              <tr>
                <th className="pb-2 font-medium">@id</th>
                <th className="pb-2 font-medium">@type</th>
                <th className="pb-2 font-medium">Nombre</th>
              </tr>
            </thead>
            <tbody>
              {nodes.map((node) => (
                <tr key={node["@id"]} className="border-t border-border align-top">
                  <td className="py-3 font-mono text-accent">{node["@id"]}</td>
                  <td className="py-3 font-mono">
                    {Array.isArray(node["@type"]) ? node["@type"].join(", ") : node["@type"]}
                  </td>
                  <td className="py-3">
                    <p className="text-fg">{node.name}</p>
                    {node.description ? <p className="mt-1 text-muted">{node.description}</p> : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
      <Card className="bg-elevated">
        <div className="flex items-center justify-between gap-3">
          <p className="text-xs uppercase tracking-[0.16em] text-muted">application/ld+json</p>
          <Button variant="secondary" size="sm" onClick={onCopy}>
            {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
            {copied ? "Copiado" : "Copiar JSON-LD"}
          </Button>
        </div>
        <pre className="mt-3 max-h-[32rem] overflow-auto font-mono text-xs leading-relaxed text-fg">{ld}</pre>
      </Card>
    </>
  );
}

function CompareView({
  rows,
  og,
  tw,
  copied,
  onCopy,
}: {
  rows: ReturnType<typeof compareRows>;
  og: string;
  tw: string;
  copied: "og" | "tw" | "ld" | null;
  onCopy: (which: "og" | "tw" | "ld") => void;
}) {
  return (
    <>
      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="overflow-hidden p-0">
          <div className="border-b border-border px-5 py-4">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Open Graph</p>
            <h2 className="mt-1 font-display text-2xl">LinkedIn / Facebook</h2>
            <p className="mt-1 text-sm text-muted">property="og:*" · tipo website · 1200×630</p>
          </div>
          <div className="p-5">
            <OgCard />
          </div>
        </Card>
        <Card className="overflow-hidden p-0">
          <div className="border-b border-border px-5 py-4">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Twitter Card</p>
            <h2 className="mt-1 font-display text-2xl">X · summary_large_image</h2>
            <p className="mt-1 text-sm text-muted">name="twitter:*" · si falta, cae a og:*</p>
          </div>
          <div className="p-5">
            <LargeCard />
          </div>
        </Card>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {PLATFORMS.map((p) => (
          <Card key={p.name} className="p-4">
            <Badge tone={p.protocol === "og" ? "accent" : "ok"}>
              {p.protocol === "og" ? "solo OG" : "twitter + OG"}
            </Badge>
            <p className="mt-3 font-display text-xl">{p.name}</p>
            <p className="mt-1 text-sm text-muted">{p.note}</p>
          </Card>
        ))}
      </div>

      <Card>
        <h2 className="font-display text-2xl">Campo a campo</h2>
        <p className="mt-1 text-sm text-muted">
          Verde: el mismo dato en ambos protocolos. El tipo de ficha y el @handle no se copian.
        </p>
        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[48rem] text-left text-sm">
            <thead className="text-xs uppercase tracking-[0.12em] text-muted">
              <tr>
                <th className="pb-2 font-medium">Campo</th>
                <th className="pb-2 font-medium">Open Graph</th>
                <th className="pb-2 font-medium">Twitter Cards</th>
                <th className="pb-2 font-medium">¿Igual?</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.field} className="border-t border-border align-top">
                  <td className="py-3">
                    <p className="text-fg">{row.field}</p>
                    <p className="mt-1 text-muted">{row.usedBy}</p>
                  </td>
                  <td className="py-3">
                    <p className="font-mono text-accent">{row.og.tag}</p>
                    <p className="mt-1 break-all text-fg">{row.og.value || "—"}</p>
                  </td>
                  <td className="py-3">
                    <p className="font-mono text-accent">{row.twitter.tag}</p>
                    <p className="mt-1 break-all text-fg">{row.twitter.value || "—"}</p>
                  </td>
                  <td className="py-3">
                    <Badge tone={row.aligned ? "ok" : "warn"}>{row.aligned ? "alineado" : "distinto"}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="bg-elevated">
          <div className="flex items-center justify-between gap-3">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Bloque OG</p>
            <Button variant="secondary" size="sm" onClick={() => onCopy("og")}>
              {copied === "og" ? <Check className="size-4" /> : <Copy className="size-4" />}
              {copied === "og" ? "Copiado" : "Copiar"}
            </Button>
          </div>
          <pre className="mt-3 overflow-x-auto font-mono text-xs leading-relaxed text-fg">{og}</pre>
        </Card>
        <Card className="bg-elevated">
          <div className="flex items-center justify-between gap-3">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Bloque Twitter</p>
            <Button variant="secondary" size="sm" onClick={() => onCopy("tw")}>
              {copied === "tw" ? <Check className="size-4" /> : <Copy className="size-4" />}
              {copied === "tw" ? "Copiado" : "Copiar"}
            </Button>
          </div>
          <pre className="mt-3 overflow-x-auto font-mono text-xs leading-relaxed text-fg">{tw}</pre>
        </Card>
      </div>
    </>
  );
}

function TwitterView({
  kind,
  setKind,
  tags,
  snippet,
  copied,
  onCopy,
}: {
  kind: CardKind;
  setKind: (k: CardKind) => void;
  tags: ReturnType<typeof twitterTags>;
  snippet: string;
  copied: boolean;
  onCopy: () => void;
}) {
  return (
    <>
      <div className="flex flex-wrap gap-2">
        {CARD_KINDS.map((k) => (
          <button
            key={k.id}
            type="button"
            onClick={() => setKind(k.id)}
            className={cn(
              "min-h-11 rounded-md border px-3 text-sm transition-colors",
              kind === k.id ? "border-accent bg-elevated text-fg" : "border-border text-muted hover:text-fg",
            )}
          >
            {k.label}
            {k.applies ? (
              <span className="ml-2 text-accent">activa</span>
            ) : (
              <span className="ml-2 text-subtle">n/a</span>
            )}
          </button>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <Card className="overflow-hidden p-0">
          <div className="border-b border-border px-5 py-4">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Vista previa en timeline</p>
            <h2 className="mt-1 font-display text-2xl">{CARD_KINDS.find((k) => k.id === kind)?.label}</h2>
            <p className="mt-1 text-sm text-muted">{CARD_KINDS.find((k) => k.id === kind)?.note}</p>
          </div>
          <div className="p-5">
            {kind === "summary_large_image" ? <LargeCard /> : null}
            {kind === "summary" ? <SummaryCard /> : null}
            {kind === "player" || kind === "app" ? (
              <p className="text-sm text-muted">Este tipo no se emite. La tarjeta real sigue siendo summary_large_image.</p>
            ) : null}
          </div>
        </Card>

        <Card className="flex flex-col gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Límites X</p>
            <ul className="mt-3 flex flex-col gap-2">
              <Meter label="twitter:title" value={TITLE} max={LIMITS.title} />
              <Meter label="twitter:description" value={DESCRIPTION} max={LIMITS.description} />
              <Meter label="twitter:image:alt" value={ALT} max={LIMITS.alt} />
            </ul>
          </div>
          <div className="border-t border-border pt-4">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Imagen</p>
            <p className="mt-2 font-mono text-sm">{IMAGE_PATH} · 1200×630 · JPEG</p>
            <p className="mt-1 text-sm text-muted">
              Mínimo 300×157, ideal {LIMITS.imageIdeal.w}×{LIMITS.imageIdeal.h}, menos de 5 MB. SVG no.
            </p>
          </div>
          <div className="border-t border-border pt-4">
            <p className="text-xs uppercase tracking-[0.16em] text-muted">Cabecera de perfil (no es Card)</p>
            <img
              src={BANNER_PATH}
              alt="Banner 50:11 para X"
              width={1200}
              height={264}
              className="mt-3 w-full rounded-md border border-border"
            />
            <p className="mt-2 text-sm text-muted">
              1200×264 es el banner de perfil, no la tarjeta de enlace. La card usa {IMAGE_PATH}.
            </p>
          </div>
        </Card>
      </div>

      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="font-display text-2xl">Etiquetas twitter:*</h2>
            <p className="mt-1 text-sm text-muted">
              Las de estado <span className="text-fg">emitted</span> salen en el HTML al publicar. El
              resto no se fabrica.
            </p>
          </div>
          <Button variant="secondary" size="sm" onClick={onCopy}>
            {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
            {copied ? "Copiado" : "Copiar meta"}
          </Button>
        </div>
        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[40rem] text-left text-sm">
            <thead className="text-xs uppercase tracking-[0.12em] text-muted">
              <tr>
                <th className="pb-2 font-medium">Etiqueta</th>
                <th className="pb-2 font-medium">Valor</th>
                <th className="pb-2 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody>
              {tags.map((tag) => (
                <tr key={tag.name} className="border-t border-border align-top">
                  <td className="py-3 font-mono text-accent">{tag.name}</td>
                  <td className="py-3">
                    <p className="break-all text-fg">{tag.value || "—"}</p>
                    <p className="mt-1 text-muted">{tag.note}</p>
                  </td>
                  <td className="py-3">
                    <Badge
                      tone={
                        tag.status === "emitted"
                          ? tag.required
                            ? "ok"
                            : "accent"
                          : "muted"
                      }
                    >
                      {tag.status === "emitted" ? (tag.required ? "obligatoria" : "emitida") : "omitida"}
                    </Badge>
                    {tag.max ? (
                      <p
                        className={cn(
                          "mt-2 font-mono text-xs",
                          withinLimit(tag.value, tag.max) ? "text-ok" : "text-danger",
                        )}
                      >
                        {charCount(tag.value)}/{tag.max}
                      </p>
                    ) : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card className="bg-elevated">
        <p className="text-xs uppercase tracking-[0.16em] text-muted">Bloque que ve X</p>
        <pre className="mt-3 overflow-x-auto font-mono text-xs leading-relaxed text-fg">
          {snippet}
        </pre>
      </Card>
    </>
  );
}

function OgCard() {
  return (
    <article className="overflow-hidden rounded-lg border border-border bg-elevated">
      <img src={IMAGE_PATH} alt={ALT} width={1200} height={630} className="w-full object-cover" />
      <div className="border-t border-border px-4 py-3">
        <p className="text-xs uppercase tracking-[0.14em] text-subtle">og:type website · og:site_name</p>
        <p className="mt-1 font-display text-xl">{TITLE}</p>
        <p className="mt-1 line-clamp-3 text-sm text-muted">{DESCRIPTION}</p>
      </div>
    </article>
  );
}

function LargeCard() {
  return (
    <article className="overflow-hidden rounded-lg border border-border bg-elevated">
      <img
        src={IMAGE_PATH}
        alt={ALT}
        width={1200}
        height={630}
        className="w-full object-cover"
      />
      <div className="border-t border-border px-4 py-3">
        <p className="text-xs uppercase tracking-[0.14em] text-subtle">dominio al publicar</p>
        <p className="mt-1 font-display text-xl">{TITLE}</p>
        <p className="mt-1 line-clamp-2 text-sm text-muted">{DESCRIPTION}</p>
      </div>
    </article>
  );
}

function SummaryCard() {
  return (
    <article className="flex overflow-hidden rounded-lg border border-border bg-elevated">
      <img src={IMAGE_PATH} alt={ALT} className="size-28 shrink-0 object-cover" />
      <div className="min-w-0 px-4 py-3">
        <p className="text-xs uppercase tracking-[0.14em] text-subtle">dominio al publicar</p>
        <p className="mt-1 truncate font-display text-lg">{TITLE}</p>
        <p className="mt-1 line-clamp-2 text-sm text-muted">{DESCRIPTION}</p>
      </div>
    </article>
  );
}

function Meter({ label, value, max }: { label: string; value: string; max: number }) {
  const n = charCount(value);
  const ok = n <= max;
  const pct = Math.min(100, Math.round((n / max) * 100));
  return (
    <li>
      <div className="flex items-center justify-between gap-3 text-sm">
        <span className="flex items-center gap-2 font-mono">
          <ImageIcon className="size-3.5 text-muted" />
          {label}
        </span>
        <span className={ok ? "text-ok" : "text-danger"}>
          {n}/{max}
        </span>
      </div>
      <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-border">
        <div
          className={cn("h-full rounded-full", ok ? "bg-ok" : "bg-danger")}
          style={{ width: `${pct}%` }}
        />
      </div>
    </li>
  );
}
