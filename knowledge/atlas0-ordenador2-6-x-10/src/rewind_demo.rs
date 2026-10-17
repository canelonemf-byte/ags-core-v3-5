use std::f64::consts::LN_2;

pub const BOLTZMANN_CONSTANT: f64 = 1.380649e-23; // J/K
pub const ROOM_TEMPERATURE_KELVIN: f64 = 300.0;

/// Apply a Toffoli gate on a 3-bit register encoded as (control_a, control_b, target).
pub fn toffoli(control_a: bool, control_b: bool, target: bool) -> (bool, bool, bool) {
    let new_target = target ^ (control_a && control_b);
    (control_a, control_b, new_target)
}

/// Landauer limit at temperature T for a logically irreversible reset of one bit.
pub fn landauer_bound_joules(temp_kelvin: f64) -> f64 {
    if temp_kelvin <= 0.0 {
        panic!("Temperature must be strictly positive.");
    }
    BOLTZMANN_CONSTANT * temp_kelvin * LN_2
}

/// Compact projection used by the Atlas0 reversible logic story.
pub fn reversible_register_summary() -> (f64, f64, bool) {
    let energy = landauer_bound_joules(ROOM_TEMPERATURE_KELVIN);
    let gate = toffoli(true, true, false);
    (energy, energy / BOLTZMANN_CONSTANT, gate.2)
}

#[cfg(test)]
mod tests {
    use super::{landauer_bound_joules, toffoli, ROOM_TEMPERATURE_KELVIN};

    #[test]
    fn toffoli_gate_forces_target_when_both_controls_are_active() {
        assert_eq!(toffoli(false, false, false), (false, false, false));
        assert_eq!(toffoli(true, true, false), (true, true, true));
        assert_eq!(toffoli(true, false, true), (true, false, true));
    }

    #[test]
    fn landauer_bound_matches_room_temperature_thermodynamic_limit() {
        let limit = landauer_bound_joules(ROOM_TEMPERATURE_KELVIN);
        assert!((limit - 2.87e-21).abs() < 1.0e-22);
    }
}
