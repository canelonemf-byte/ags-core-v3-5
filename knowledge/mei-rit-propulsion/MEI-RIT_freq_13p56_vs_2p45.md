# MEI-RIT — 13.56 MHz vs 2.45 GHz
2026-09-22. Complementa MEI-RIT_v2.1_QC.md. Canon: llp/proyectos/MEI-RIT.json

Decision: proto1 = 13.56 MHz ICP. 2.45 GHz = rama distinta (ECR/cavity), no dual-band.

| | 13.56 MHz | 2.45 GHz |
|---|---|---|
| lambda0 | 22.1 m | 122 mm |
| p/lambda @ 3-15 mm | 1.4e-4 – 6.8e-4 | 0.025 – 0.123 |
| Metasuperficie EM | no (impedancia concentrada) | si (HIS/FSS) |
| Acoplo | ICP bobina | ECR 875 G o cavidad/ventana |
| f_pe = f | n=2.3e12 m-3 (irrelevante) | n=7.45e16 m-3 |
| delta piel util camara 3 cm | 6-25 mm (lit. ICP) | capa evanescente / zona ECR |
| B_ECR | 4.8 G (inutil) | 87.5 mT |
| Heritage I2 GIT | NPT30, BIT-3, RIT Giessen | μ1/μ10 clase ECR (Xe), no I2 vuelo |
| PPU 50-80 W | ISM Class-E/D, matching LC | GaN SSPA + isolator + launch |
| EMC CubeSat | gestionable | armonicos/radar, mas filtro |
| VQE/I2 | independiente de f | independiente de f |

h nu: 56 neV vs 10 ueV. Ninguno mueve el PES. QC no decide la frecuencia.
