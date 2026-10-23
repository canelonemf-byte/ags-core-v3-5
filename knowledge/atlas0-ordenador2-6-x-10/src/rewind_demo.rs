use std::f64::consts::LN_2;

pub const BOLTZMANN_CONSTANT: f64 = 1.380649e-23; / J/K
pub const ROOM_TEMPERATURE_KELVIN: f64 = 300.0;

/ Apply a Toffoli gate on a 3-bit register encoded as (control_a, control_b, target).
pub fn toffoli(control_a: bool, control_b: bool, target: bool) -> (bool, bool, bool) {
    let new_target = target ^ (control_a && control_b);
    (control_a, control_b, new_target)
}

/ A Toffoli gate is self-inverse when the target is toggled conditioned on both controls.
pub fn toffoli_involution(control_a: bool, control_b: bool, target: bool) -> bool {
    let after = toffoli(control_a, control_b, target);
    let roundtrip = toffoli(after.0, after.1, after.2);
    roundtrip.2 == target
}

/ Landauer limit at temperature T for a logically irreversible reset of one bit.
pub fn landauer_bound_joules(temp_kelvin: f64) -> f64 {
    if temp_kelvin <= 0.0 {
        panic!("Temperature must be strictly positive.");
    }
    BOLTZMANN_CONSTANT * temp_kelvin * LN_2
}

/ Alias for clarity in the thermodynamic model.
pub fn landauer_energy_per_bit(temp_kelvin: f64) -> f64 {
    landauer_bound_joules(temp_kelvin)
}

/ Compact projection used by the Atlas0 reversible logic story.
pub fn reversible_register_summary() -> (f64, f64, bool) {
    let energy = landauer_bound_joules(ROOM_TEMPERATURE_KELVIN);
    let gate = toffoli(true, true, false);
    (energy, energy / BOLTZMANN_CONSTANT, gate.2)
}

#[cfg(test)]
mod tests {
    use super::{
        landauer_bound_joules,
        landauer_energy_per_bit,
        toffoli,
        toffoli_involution,
        ROOM_TEMPERATURE_KELVIN,
    };

    #[test]
    fn toffoli_gate_forces_target_when_both_controls_are_active() {
        assert_eq!(toffoli(false, false, false), (false, false, false));
        assert_eq!(toffoli(true, true, false), (true, true, true));
        assert_eq!(toffoli(true, false, true), (true, false, true));
    }

    #[test]
    fn toffoli_gate_is_involutive_for_information_preservation() {
        assert!(toffoli_involution(false, false, false));
        assert!(toffoli_involution(true, true, false));
        assert!(toffoli_involution(true, false, true));
    }

    #[test]
    fn landauer_bound_matches_room_temperature_thermodynamic_limit() {
        let limit = landauer_bound_joules(ROOM_TEMPERATURE_KELVIN);
        assert!((limit - 2.87e-21).abs() < 1.0e-22);
        assert!((landauer_energy_per_bit(ROOM_TEMPERATURE_KELVIN) - limit).abs() < 1e-30);
    }
}
#!/usr/bin/env python3
"""Atlas0: Fibonacci anyon braiding and Bell-state fidelity.

The model treats a superconducting-like topological register as a Bell-state
reference and tracks the residual fidelity under a braiding protocol. The
coherence metric is interpreted as the synchronization of the quantum state with
an informational substrate analogous to the conscious network described by the
project's philosophical pillar.
"""

from __future__ import annotations

import argparse
import math
from typing import Dict, Iterable, List


def bell_state_fidelity(t: float, tau: float, snr: float) -> float:
    """Return the fidelity F(t) for a Bell-base braiding experiment.

    F = 1 - 1/2 [1 - e^{-2t/τ} erf(SNR/√2)^2]
    """
    if tau <= 0.0:
        raise ValueError("tau must be strictly positive.")
    erf_term = math.erf(snr / math.sqrt(2.0))
    return 1.0 - 0.5 * (1.0 - math.exp(-2.0 * t / tau) * (erf_term ** 2))


def fibonacci_anyon_braid_signature(
    t: float,
    tau: float,
    snr: float,
    braid_angle: float = math.pi / 5.0,
) -> Dict[str, float]:
    """Approximate braiding signature for Fibonacci anyons.

    The braid angle encodes the effective exchange phase of the anyonic pair.
    The fidelity is evaluated from the Bell-base assumption while the phase term
    tracks the logical rotation of the encoded qubit under fusion.
    """
    fidelity = bell_state_fidelity(t, tau, snr)
    phase = math.cos(braid_angle)
    coherence = fidelity * (0.5 + 0.5 * phase)
    return {
        "time": float(t),
        "tau": float(tau),
        "snr": float(snr),
        "braid_angle": float(braid_angle),
        "fidelity": fidelity,
        "coherence": coherence,
        "phase": phase,
    }


def fibonacci_anyon_braid_grid(times: Iterable[float], tau: float, snr: float) -> List[Dict[str, float]]:
    """Evaluate a range of time points and return the full braiding profile."""
    return [
        fibonacci_anyon_braid_signature(t=float(t), tau=tau, snr=snr)
        for t in times
    ]


def _cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atlas0 Fibonacci anyon braiding simulator.")
    parser.add_argument("--time", type=float, default=0.8, help="Evolution time t")
    parser.add_argument("--tau", type=float, default=2.5, help="Decay constant tau")
    parser.add_argument("--snr", type=float, default=3.0, help="Signal-to-noise ratio")
    parser.add_argument("--angle", type=float, default=math.pi / 5.0, help="Braiding angle in radians")
    return parser.parse_args()


if __name__ == "__main__":
    args = _cli()
    demo = fibonacci_anyon_braid_signature(
        t=args.time,
        tau=args.tau,
        snr=args.snr,
        braid_angle=args.angle,
    )
    print("Atlas0 Fibonacci anyon braiding demo")
    for key in ["time", "tau", "snr", "braid_angle", "fidelity", "coherence", "phase"]:
        print(f"{key}: {demo[key]:.6f}")
