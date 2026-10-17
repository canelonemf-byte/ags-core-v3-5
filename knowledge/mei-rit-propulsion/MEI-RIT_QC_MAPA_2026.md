# QC 2026 — qué entra en MEI-RIT y qué no
Fecha: 2026-09-22. No hay QPU en este sandbox.

## Hacer (con evidencia de literatura 2025-2026)
1. CASSCF/VQE/SQD del espacio activo I2 (10e,8o) + ECP. 16 qubits JW.
   Referencia clasica corrida aqui: CASSCF(10e,8o)/cc-pVDZ-PP De=1.187 eV vs 1.542 exp. Error de BASE, no de QPU.
2. SQD IBM (Heron + supercomputador) si hay cuenta. Sustituye VQE ruidoso en espacios mayores. Demo N2 / Fe-S 2025; proteinas 2026. I2 es MAS pequeno: viable como job, no como hito de thruster.
3. QUBO/QAOA del anillo binario 8x8. Literature 2025-26: QAOA para RIS/metasuperficies, annealers inspirados. En proto1 el anillo es lumped: QAOA no es camino critico.

## No hacer
Maxwell 3D, PIC, Gamma, empuje, 2.45 GHz ECR, "universo consciente".
VQE all-electron I2 (106 e-).
Afirmar que QC corrige el error 0.35 eV del ECP/base: eso es quimica clasica (base + SOC + CV).

## Stack
PySCF CASSCF = verdad de referencia (hecho, E3 sim).
VQE statevector = demo algoritmo (vqe_i2.py).
SQD Qiskit addon = siguiente si hay backend IBM.
QAOA = opcional sobre surrogate CST.

SOC de yodo no esta en el CAS de hoy. Sin SOC el PES de I2 esta incompleto (E1 debil para tasas).
