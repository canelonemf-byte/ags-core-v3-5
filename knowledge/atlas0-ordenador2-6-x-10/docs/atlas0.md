---
title: "Atlas0: Phase 1 dossier"
author:
  - "Lázaro López Paz"
  - "Atlas0 collaborative node"
keywords: [quantum-computation, topological-logic, reversible-computing, zenodo]
license: "CC BY 4.0"
abstract: |
  Atlas0 consolidates the first computational sprint around topological quantum
  compilation, reversible logic, and the information-theoretic framing of the
  conscious substrate.
---

# Atlas0 Phase 1 dossier

## Summary

This dossier prepares the metadata package for a future Zenodo publication of the
first research phase. The project focuses on three linked axes: Fibonacci anyon
braiding, reversible logic constraints, and the thermodynamic boundary described
by the Landauer limit.

## Scientific framing

1. Topological quantum compilation is evaluated under a Bell-state fidelity model.
2. Reversible logic is represented through Toffoli gates in a reversible register.
3. The thermodynamic ceiling is estimated at 300 K via E = k_B T ln 2.

## Metadata notes

The publication package must keep the license explicit and preserve a future
citation chain in the `.bib` file for bibliographic integration in Zenodo.

## Canonical references

- `src/tqc_demo.py` — Fibonacci anyon braiding with Bell-state fidelity tracking.
- `src/rewind_demo.rs` — Toffoli gate implementation and Landauer limit check.
- `Makefile` — dependency validation and full test trigger.
