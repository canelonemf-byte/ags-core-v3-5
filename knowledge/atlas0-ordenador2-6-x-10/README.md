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
│   └── sprint_01_manifest.json       # Project directives & timeline
├── src/
│   ├── tqc_demo.py                   # [A1] Fibonacci anyon braiding demo
│   └── rewind_demo.rs                # [A2] Reversible logic primer
├── tests/
│   └── rewind/
│       ├── Cargo.toml
│       └── src/lib.rs                # Toffoli & Landauer tests
├── docs/
│   ├── atlas0.md                     # [A7] Markdown dossier
│   ├── atlas0.tex                    # [A7] LaTeX compilation source
│   └── atlas0.bib                    # [A7] Citation metadata for Zenodo
├── Makefile                          # [A8] CI/CD pipeline gate
├── LICENSE                           # [A6/A5] MIT clearance
└── .gitignore
```

## Directives Map

| ID  | Task                  | File(s)                              | Status |
|-----|----------------------|--------------------------------------|--------|
| A1  | TQC anyon braiding   | `src/tqc_demo.py`                   | ✓ Ready  |
| A2  | Reversible logic     | `src/rewind_demo.rs`, `tests/`      | ✓ Ready  |
| A6/A5 | License clearance  | `LICENSE`                            | ✓ MIT/Apache |
| A8  | CI/CD pipeline       | `Makefile`                           | ✓ Green  |
| A7  | Zenodo metadata      | `docs/atlas0.{md,tex,bib}`          | ✓ Prepared |

## Test Pipeline

Run the complete validation (blocks on failure):
```bash
make test-all
```

This executes:
1. Python TQC demo compilation
2. Rust reversible logic unit tests
3. TQC demo execution

## License

MIT License. See `LICENSE` for full text.

## References

- Landauer, R. (1961) "Irreversibility and Heat Generation in the Computing Process"
- Kitaev, A. Yu. (2003) "Fault-tolerant quantum computation by anyons"
- Atlas0 Phase 1 Zenodo dossier (CC BY 4.0)
