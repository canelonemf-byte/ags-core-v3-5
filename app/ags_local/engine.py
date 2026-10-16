"""Motor local: reglas primero, AGsGPT solo si hay pesos. Sin claves externas."""
import json
import os
import threading
from pathlib import Path

from .memory import Memory
from .planner import Planner
from .project_registry import Registry

HERE = Path(__file__).resolve().parent
DEFAULT_CFG = {
    "model": {"d": 128, "h": 4, "n_layers": 4, "ctx": 128, "lora_rank": 8, "lora_alpha": 8},
    "learning": {"auto_learn_every_n_turns": 0, "pasos": 40, "max_pasos_api": 200},
}


def _torch_ok() -> bool:
    try:
        import torch  # noqa: F401
        return True
    except ImportError:
        return False


class _SubAgent:
    def __init__(self, engine, pid):
        self.e, self.pid = engine, pid

    def run(self, step: str) -> str:
        hit = self.e.registry.match_tool(self.pid, step)
        if not hit:
            return self.e.gpt_or_gap(step, self.pid)
        nombre, fn = hit
        return f"[{nombre}]\n  [{nombre}] " + fn(step).replace("\n", "\n  ")


class LocalEngine:
    def __init__(self, data_dir: Path | None = None, cfg: dict | None = None):
        self.data_dir = Path(data_dir or os.getenv("AGSGPT_DATA_DIR", HERE.parents[1] / "data"))
        self.cfg = json.loads(json.dumps(cfg or DEFAULT_CFG))
        self.registry = Registry(HERE / "projects.json")
        self.memory = Memory(self.data_dir / "ags_memory.sqlite")
        self.planner = Planner(self)
        self.subagents = {pid: _SubAgent(self, pid) for pid in self.registry.projects}
        self.model, self.tok = None, None
        self._lock = threading.Lock()
        self.last_loss = None
        self._load()

    # ---- rutas ----
    @property
    def ckpt_dir(self) -> Path:
        return Path(os.getenv("AGSGPT_CKPT_DIR", self.data_dir / "checkpoints"))

    def _p(self, name):
        return self.ckpt_dir / name

    # ---- reglas ----
    def route(self, text: str):
        return self.registry.route(text)

    def run_tool(self, pid: str, text: str) -> dict:
        proj = self.registry.get(pid)
        if not proj:
            raise KeyError(pid)
        hit = self.registry.match_tool(pid, text)
        if not hit:
            return {"project": pid, "tool": None, "output": None,
                    "available_tools": list(proj.tools)}
        nombre, fn = hit
        out = fn(text)
        self.memory.add(text, role="user", project=pid)
        self.memory.add(out[:500], role="tool", project=pid)
        return {"project": pid, "tool": nombre, "output": out, "available_tools": list(proj.tools)}

    def can_solve_locally(self, task: str) -> bool:
        steps = self.planner._decompose(task)
        for s in steps:
            p = self.registry.route(s)
            if p and self.registry.match_tool(p.id, s):
                return True
        return False

    def handle(self, text: str) -> str:
        proj = self.registry.route(text)
        pid = proj.id if proj else "general"
        if proj and proj.tools:
            return self.subagents[pid].run(text)
        return self.gpt_or_gap(text, pid)

    # ---- AGsGPT ----
    def _load(self):
        if not _torch_ok():
            return
        tok_p, ck = self._p("tokenizer.json"), self._p("ags_gpt.pt")
        if not (tok_p.exists() and ck.exists()):
            return
        import torch
        from .model import AGsGPT, CharTokenizer, apply_lora
        m = self.cfg["model"]
        tok = CharTokenizer().load(tok_p)
        model = AGsGPT(tok.vocab_size, m["d"], m["h"], m["n_layers"], m["ctx"])
        apply_lora(model, m["lora_rank"], m["lora_alpha"])
        state = torch.load(ck, map_location="cpu", weights_only=True)
        own = model.state_dict()
        fixed = {}
        for k, v in state.items():
            dest = k if k in own else k.replace(".weight", ".base.weight").replace(".bias", ".base.bias")
            if dest in own and own[dest].shape == v.shape:
                fixed[dest] = v
        own.update(fixed)
        model.load_state_dict(own, strict=False)
        lora = self._p("ags_lora.pt")
        if lora.exists():
            extra = torch.load(lora, map_location="cpu", weights_only=True)
            own = model.state_dict()
            own.update({k: v for k, v in extra.items() if k in own and own[k].shape == v.shape})
            model.load_state_dict(own, strict=False)
        model.eval()
        self.model, self.tok = model, tok

    def status(self) -> dict:
        n_total = n_train = 0
        if self.model is not None:
            n_total = sum(p.numel() for p in self.model.parameters())
            n_train = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        return {"torch": _torch_ok(), "weights": self.model is not None,
                "params_total": n_total, "params_lora": n_train,
                "experiences": self.memory.count(), "last_loss": self.last_loss,
                "ckpt_dir": str(self.ckpt_dir), "config": self.cfg["model"],
                "note": "Base aleatoria congelada sin preentrenar: la salida no es fiable ni es una medida."}

    def gpt_or_gap(self, text: str, pid: str) -> str:
        if self.model is None:
            return f"[{pid}] sin herramienta que encaje y AGsGPT no tiene pesos. La física no se inventa."
        import torch
        hits = self.memory.similar(text, 3)
        prompt = "\n".join(hits + [text])[-400:]
        ids = self.tok.encode(prompt) or [0]
        idx = torch.tensor([ids[-self.model.ctx:]])
        out = self.model.generate(idx, max_new=80)
        new = self.tok.decode(out[0, idx.size(1):].tolist())
        return f"[AGsGPT]\n  {new}\n  (caracteres entrenados, no es una medida)"

    def train(self, steps: int | None = None, extra_text: str = "") -> dict:
        if not _torch_ok():
            raise RuntimeError("torch no instalado")
        import torch
        from .model import AGsGPT, CharTokenizer, adapter_state, apply_lora
        steps = int(steps or self.cfg["learning"]["pasos"])
        steps = max(1, min(steps, int(self.cfg["learning"]["max_pasos_api"])))
        with self._lock:
            text = self.memory.corpus() + ("\n" + extra_text if extra_text else "")
            if len(text) < 80:
                text += "\nAGsGPT se entrena con la memoria del operador. Las cuentas físicas las hacen las herramientas."
            m = self.cfg["model"]
            tok = CharTokenizer().fit(text)
            torch.manual_seed(20260416)
            model = AGsGPT(tok.vocab_size, m["d"], m["h"], m["n_layers"], m["ctx"])
            trainable = apply_lora(model, m["lora_rank"], m["lora_alpha"])
            ids = tok.encode(text)
            ctx = m["ctx"]
            opt = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=3e-4)
            model.train()
            last = None
            for i in range(steps):
                if len(ids) < ctx + 1:
                    cut = ids
                else:
                    start = i % (len(ids) - ctx)
                    cut = ids[start:start + ctx + 1]
                if len(cut) < 2:
                    continue
                x = torch.tensor([cut[:-1]]); y = torch.tensor([cut[1:]])
                _, loss = model(x, y)
                opt.zero_grad(); loss.backward(); opt.step()
                last = float(loss.detach())
            self.ckpt_dir.mkdir(parents=True, exist_ok=True)
            tok.save(self._p("tokenizer.json"))
            torch.save(model.state_dict(), self._p("ags_gpt.pt"))
            torch.save(adapter_state(model), self._p("ags_lora.pt"))
            model.eval()
            self.model, self.tok, self.last_loss = model, tok, last
        return {"steps": steps, "loss": last, "trainable_lora_params": trainable,
                "adapter_file": str(self._p("ags_lora.pt"))}


_ENGINE = None


def get_engine() -> LocalEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = LocalEngine()
    return _ENGINE


def reset_engine(engine: LocalEngine | None = None):
    global _ENGINE
    _ENGINE = engine
