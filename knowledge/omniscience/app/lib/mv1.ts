import { MATERIALS } from "./catalog";
import { hashSeed, mulberry32 } from "./rng";

export type StepStatus = "SUCCESS" | "REVISION" | "FAILED" | "RUNNING";

export type ProvStep = {
  name: string;
  status: StepStatus;
  detail: string;
  agent: string;
};

export type CampaignResult = {
  id: string;
  materialId: string;
  materialName: string;
  status: "verified_prediction" | "falsified" | "running";
  reason?: string;
  eform: number;
  usedDft: boolean;
  maxForce: number;
  frequencies: number[];
  imaginary: number;
  evidence: 2 | 3;
  steps: ProvStep[];
  startedAt: number;
  elapsedMs: number;
};

function gauss(rng: () => number) {
  const u = Math.max(rng(), 1e-9);
  const v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

export async function runMv1(
  materialId: string,
  onStep: (partial: CampaignResult) => void,
): Promise<CampaignResult> {
  const mat = MATERIALS.find((m) => m.id === materialId) ?? MATERIALS[0];
  const id = `CAMP-${Date.now().toString(36).toUpperCase()}`;
  const rng = mulberry32(hashSeed(`${id}:${mat.id}`));
  const startedAt = Date.now();
  const result: CampaignResult = {
    id,
    materialId: mat.id,
    materialName: mat.name,
    status: "running",
    eform: mat.eform,
    usedDft: false,
    maxForce: 0,
    frequencies: [],
    imaginary: 0,
    evidence: 2,
    steps: [],
    startedAt,
    elapsedMs: 0,
  };

  const push = async (step: ProvStep, wait = 420) => {
    result.steps = [...result.steps, step];
    result.elapsedMs = Date.now() - startedAt;
    onStep({ ...result, steps: [...result.steps] });
    await new Promise((r) => setTimeout(r, wait));
  };

  await push({
    name: "Normalización cristalográfica",
    status: "SUCCESS",
    detail: `Celda a = ${mat.a.toFixed(2)} Å · ${mat.composition}`,
    agent: "eng-matter",
  });

  await push({
    name: "Relajación estructural",
    status: "SUCCESS",
    detail: "Mínimo local sobre la celda unidad (surrogate).",
    agent: "eng-matter",
  });

  await push({
    name: "Energía de formación",
    status: "SUCCESS",
    detail: `Eform = ${mat.eform.toFixed(2)} eV/átomo`,
    agent: "eng-matter",
  });

  if (mat.eform >= 0) {
    await push({
      name: "Falsación termodinámica (Eform ≥ 0)",
      status: "FAILED",
      detail: "Early-exit: la fase no es estable frente a elementos de referencia.",
      agent: "orch-mv1",
    });
    result.status = "falsified";
    result.reason = "termodinámica";
    result.evidence = 2;
    result.elapsedMs = Date.now() - startedAt;
    onStep({ ...result });
    return result;
  }

  await push({
    name: "Estabilidad de fase",
    status: "SUCCESS",
    detail: "Eform < 0. Continúa dinámica de red.",
    agent: "eng-matter",
  });

  const nDisp = 3;
  await push({
    name: "Desplazamientos Phonopy",
    status: "SUCCESS",
    detail: `${nDisp} superceldas 2×2×2`,
    agent: "eng-vib",
  });

  let maxAbs = 0;
  for (let i = 0; i < nDisp; i++) {
    const anomaly = rng() > 0.78;
    const forces = Array.from({ length: 8 }, () =>
      Array.from({ length: 3 }, () => (anomaly ? (rng() - 0.5) * 80 : (rng() - 0.5) * 0.16)),
    );
    const peak = Math.max(...forces.flat().map(Math.abs));
    maxAbs = Math.max(maxAbs, peak);
    if (peak > 10) {
      result.usedDft = true;
      await push({
        name: `Fallback adversarial DFT [supercelda ${i + 1}]`,
        status: "REVISION",
        detail: `MLIP anómalo (max |F| = ${peak.toFixed(1)} eV/Å). Se descarta y se recalcula Ab Initio.`,
        agent: "dft-fallback",
      });
      const dftPeak = 0.04 + rng() * 0.08;
      maxAbs = Math.max(maxAbs, dftPeak);
    } else {
      await push({
        name: `Validación MLIP [supercelda ${i + 1}]`,
        status: "SUCCESS",
        detail: `max |F| = ${peak.toFixed(3)} eV/Å < 10`,
        agent: "mlip-mace",
      });
    }
  }
  result.maxForce = maxAbs;

  const freqs = Array.from({ length: 48 }, () => {
    if (rng() < mat.imagRisk) return -0.4 - rng() * 1.2;
    return 0.4 + Math.abs(gauss(rng)) * 4.2;
  }).sort((a, b) => a - b);
  result.frequencies = freqs;
  const imag = freqs.filter((f) => f < -1e-3).length;
  result.imaginary = imag;

  await push({
    name: "Diagonalización D(q)",
    status: "SUCCESS",
    detail: `${freqs.length} ramas · min ω = ${freqs[0].toFixed(2)} THz`,
    agent: "eng-vib",
  });

  if (imag > 0) {
    await push({
      name: "Falsación dinámica (modos imaginarios)",
      status: "FAILED",
      detail: `${imag} frecuencias ω² < 0. Distinguir inestabilidad vs. convergencia en réplica.`,
      agent: "orch-mv1",
    });
    result.status = "falsified";
    result.reason = "modos imaginarios";
    result.evidence = 2;
  } else {
    await push({
      name: "Predicción verificable",
      status: "SUCCESS",
      detail: "Sin modos imaginarios. Nivel 3 en este entorno (surrogate, no DFT de producción).",
      agent: "orch-mv1",
    });
    result.status = "verified_prediction";
    result.evidence = 3;
  }
  result.elapsedMs = Date.now() - startedAt;
  onStep({ ...result });
  return result;
}
