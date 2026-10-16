"""Planificador de objetivos multi-paso: descompone, ejecuta, verifica."""
import re


class Planner:
    def __init__(self, orchestrator):
        self.o = orchestrator

    def _decompose(self, goal: str):
        parts = re.split(r",|;| y luego | entonces | después | además | paso \d+[:.]?", goal, flags=re.I)
        return [p.strip(" .").capitalize() for p in parts if p.strip(" .")] or [goal]

    def plan(self, goal: str) -> str:
        steps = self._decompose(goal)
        lines = [f"▶ PLAN: {goal}", f"  {len(steps)} pasos detectados:"]
        fails = 0
        for i, step in enumerate(steps, 1):
            proj = self.o.registry.route(step)
            pid = proj.id if proj else "general"
            result = self._run_step(step, pid)
            ok = self._step_ok(result)
            if not ok:
                retry = self._run_step(step + " (resuélvelo con tus herramientas numéricas)", pid)
                if self._step_ok(retry):
                    result, ok = retry, True
            mark = "✔" if ok else "✘"
            fails += not ok
            lines.append(f"  {i}. [{pid}] {step} {mark}")
            self.o.memory.add(f"PASO {i}: {step}", role="plan", project=pid)
            self.o.memory.add(result[:500], role="plan_result", project=pid)
            for rl in result.split("\n")[1:3]:
                lines.append(f"     {rl.strip()}")
        lines.append(
            "✔ Plan completado: todos los pasos verificados."
            if fails == 0
            else f"⚠ Plan terminado con {fails} paso(s) sin verificar."
        )
        return "\n".join(lines)

    def _run_step(self, step: str, pid: str) -> str:
        proj = self.o.registry.get(pid)
        if proj and proj.tools:
            return self.o.subagents[pid].run(step)
        return self.o.handle(step)

    @staticmethod
    def _step_ok(result: str) -> bool:
        if "error:" in result.lower():
            return False
        body = result.split("\n")[1:]
        return any(l.strip().startswith("[") for l in body) or "Sub-agente" in result
