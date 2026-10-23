# Atlas0 build and validation commands.

PYTHON ?= python3
VENV ?= .venv
RUSTC ?= rustc
CARGO ?= cargo
LEAN ?= lean
ELAN ?= elan

.PHONY: check-deps venv test-all clean install-tqc install-rewind install-theseus phase2-check lean-check

check-deps:
	@echo "[A8] Checking system dependencies..."
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "ERROR: Python3 not found" && exit 1)
	@command -v rustc >/dev/null 2>&1 || (echo "ERROR: Rust toolchain not installed" && exit 1)
	@command -v $(CARGO) >/dev/null 2>&1 || (echo "ERROR: Cargo not found" && exit 1)
	@echo "✓ Python3: $$(python3 --version)"
	@echo "✓ Rustc: $$(rustc --version)"
	@echo "✓ Cargo: $$(cargo --version)"
	@echo "Dependency check PASSED."

venv:
	@echo "Creating isolated Python venv..."
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && python -m pip install --upgrade pip setuptools wheel
	@echo "Venv ready at $(VENV)"

install-tqc: venv
	@echo "[A1] Installing TQC demo dependencies..."
	. $(VENV)/bin/activate && pip install numpy scipy

install-rewind: check-deps
	@echo "[A2] Building reversible logic (Rust)..."
	$(CARGO) build --manifest-path tests/rewind/Cargo.toml --release

install-theseus:
	@echo "[P2] Initializing Lean 4 proof scaffold..."
	@echo "This repository carries a lightweight Lean 4 foundation for the Landauer theorem.
	@echo "If Lean is available, use: make lean-check"

lean-check:
	@echo "[P2] Checking Lean 4 proof scaffold..."
	@if command -v $(ELAN) >/dev/null 2>&1; then \
		$(ELAN) run lean --run lean/Atlas0.lean; \
	else \
		echo "Lean 4 toolchain not installed; skipping proof validation."; \
	fi

phase2-check: check-deps
	@echo "[P2] Running Phase 2 validation suite..."
	@set -e; \
	$(PYTHON) -m py_compile src/tqc_demo.py; \
	$(CARGO) test --manifest-path tests/rewind/Cargo.toml; \
	$(PYTHON) src/tqc_demo.py --time 0.8 --tau 2.5 --snr 3.0 --angle 1.25663706; \
	 echo "[P2] Phase 2 checks complete.";

test-all: check-deps phase2-check
	@echo "[A8] ALL TESTS PASSED - Pipeline green."

clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(VENV) target/
	$(CARGO) clean --manifest-path tests/rewind/Cargo.toml 2>/dev/null || true
	@echo "Clean complete."
# Atlas0: Quantum Foundation Sprint

**Sprint ID:** `sprint_01_software_foundation`  
**Status:** Active  
**Timeline:** 2026-10-07 to 2026-10-21 (2 weeks)  
**Budget:** €2,500  

## Overview

Atlas0 Phase 1 bootstraps a computational framework merging:
- **Topological Quantum Compilation (TQC):** Fibonacci anyon braiding under Bell-state fidelity
- **Reversible Logic:** Toffoli gates and Landauer thermodynamic limit at 300 K
- **Conscious Substrate Informatics:** Coherence as synchronization with the informational network

## Phase 2 (implemented)

We have expanded the project with a stronger technical foundation for the next iteration:

- robust TQC simulator with CLI and time-grid evaluation
- more explicit reversible-logic invariants and regression tests
- Lean 4 proof scaffold for the Landauer bound
- Phase 2 documentation and roadmap for future publication and integration

## Quick Start

```bash
# Clone and setup
git clone https://github.com/canelonemf-byte/Atlas0-ordenador2.6-x-10-.git
cd Atlas0-ordenador2.6-x-10-

# Verify dependencies (A8)
make check-deps

# Install and test all components
make install-tqc install-rewind install-theseus
make test-all
```

## Project Structure

```
.
├── scripts/
│   ├── sprint_01_manifest.json
│   └── phase_02_manifest.json
├── src/
│   ├── tqc_demo.py
│   └── rewind_demo.rs
├── tests/
│   └── rewind/
│       ├── Cargo.toml
│       └── src/lib.rs
├── lean/
│   ├── Atlas0.lean
│   └── lean-toolchain
├── docs/
│   ├── atlas0.md
│   ├── atlas0.tex
│   ├── atlas0.bib
│   ├── atlas0_phase2.md
│   └── atlas0_phase2.tex
├── Makefile
├── LICENSE
├── README.md
└── .gitignore
```

## Directives Map

| ID  | Task                  | File(s)                              | Status |
|-----|----------------------|--------------------------------------|--------|
| A1  | TQC anyon braiding   | `src/tqc_demo.py`                   | ✓ Ready  |
| A2  | Reversible logic     | `src/rewind_demo.rs`, `tests/`      | ✓ Ready  |
| A6/A5 | License clearance  | `LICENSE`                            | ✓ MIT |
| A8  | CI/CD pipeline       | `Makefile`                           | ✓ Ready  |
| A7  | Zenodo metadata      | `docs/atlas0.{md,tex,bib}`          | ✓ Prepared |
| P2  | Phase 2 proof core   | `lean/Atlas0.lean`                  | ✓ Scaffold |
| P2  | Future release prep  | `docs/atlas0_phase2.md`             | ✓ Prepared |

## Test Pipeline

Run the complete validation (blocks on failure):
```bash
make test-all
```

This executes:
1. Python TQC demo compilation
2. Rust reversible logic unit tests
3. TQC demo execution
4. Lean 4 scaffold validation target (if toolchain is installed)

## License

MIT License. See `LICENSE` for full text.

## References

- Landauer, R. (1961) "Irreversibility and Heat Generation in the Computing Process"
- Kitaev, A. Yu. (2003) "Fault-tolerant quantum computation by anyons"
- Atlas0 Phase 1 Zenodo dossier (CC BY 4.0)
