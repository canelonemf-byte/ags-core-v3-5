export function linspace(a: number, b: number, n: number) {
  const out = new Array<number>(n);
  const s = n === 1 ? 0 : (b - a) / (n - 1);
  for (let i = 0; i < n; i++) out[i] = a + i * s;
  return out;
}

export function dampedFree(t: number, omega0: number, zeta: number, x0 = 1) {
  if (zeta < 1) {
    const wd = omega0 * Math.sqrt(Math.max(1 - zeta * zeta, 0));
    return Math.exp(-zeta * omega0 * t) * x0 * Math.cos(wd * t);
  }
  if (zeta === 1) return (x0 + omega0 * x0 * t) * Math.exp(-omega0 * t);
  const s = Math.sqrt(zeta * zeta - 1);
  return x0 * Math.exp(-zeta * omega0 * t) * Math.cosh(omega0 * s * t);
}

export function resonanceAmp(omega: number, omega0: number, zeta: number) {
  const d = (omega0 * omega0 - omega * omega) ** 2 + (2 * zeta * omega0 * omega) ** 2;
  return 1 / Math.sqrt(d);
}

export function phononMono(ka: number) {
  return 2 * Math.abs(Math.sin(ka / 2));
}

export function phononDiatomic(ka: number, m1 = 1, m2 = 2.2) {
  const mu = 1 / m1 + 1 / m2;
  const disc = Math.sqrt(Math.max(mu * mu - (4 / (m1 * m2)) * Math.sin(ka / 2) ** 2, 0));
  return { ac: Math.sqrt(mu - disc), op: Math.sqrt(mu + disc) };
}

function hermite(n: number, x: number) {
  if (n === 0) return 1;
  if (n === 1) return 2 * x;
  let h0 = 1;
  let h1 = 2 * x;
  for (let k = 2; k <= n; k++) {
    const h = 2 * x * h1 - 2 * (k - 1) * h0;
    h0 = h1;
    h1 = h;
  }
  return h1;
}

function fact(n: number) {
  let r = 1;
  for (let i = 2; i <= n; i++) r *= i;
  return r;
}

export function qhoPsi(n: number, x: number) {
  const norm = 1 / Math.sqrt(2 ** n * fact(n) * Math.sqrt(Math.PI));
  return norm * Math.exp((-x * x) / 2) * hermite(n, x);
}

export function dftMag(signal: number[]) {
  const n = signal.length;
  const half = Math.floor(n / 2);
  const mag = new Array<number>(half);
  for (let k = 0; k < half; k++) {
    let re = 0;
    let im = 0;
    for (let t = 0; t < n; t++) {
      const ang = (-2 * Math.PI * k * t) / n;
      re += signal[t] * Math.cos(ang);
      im += signal[t] * Math.sin(ang);
    }
    mag[k] = Math.hypot(re, im) / n;
  }
  return mag;
}

export function chirpSignal(n = 256, dt = 1 / 200) {
  const sig = new Array<number>(n);
  for (let i = 0; i < n; i++) {
    const t = i * dt;
    const chirp = 0.7 * Math.sin(2 * Math.PI * (8 + 12 * t) * t);
    const tone = 0.45 * Math.sin(2 * Math.PI * 22 * t);
    const burst = t > 0.7 ? 0.9 * Math.sin(2 * Math.PI * 40 * t) * Math.exp(-(t - 0.7) * 4) : 0;
    sig[i] = chirp + tone + burst;
  }
  return sig;
}
