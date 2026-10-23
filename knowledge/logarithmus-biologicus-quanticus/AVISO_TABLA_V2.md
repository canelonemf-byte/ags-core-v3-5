# Aviso: la tabla de resultados LCPB v2.0 no es válida

En el código del documento LOGARITHMUS BIOLOGICUS QUANTICUS v2.0, el término de calibración es
`gamma = Lambda_media - log10(prod_F/prod_R * S) - delta`. Sustituido en `Lambda = log10(prod_F/prod_R * S) + delta + gamma`,
da **Lambda = Lambda_media (la media del MCMC) para todos los planetas**. Los factores de cada planeta se cancelan,
así que la columna "Λ v2.0" y su clasificación no dependen de los datos de cada planeta.

- Demostración: `tests/test_lcpb.py::test_original_gamma_is_circular`.
- Corrección: `lcpb.lcpb(...)` usa gamma = 0. Una calibración real necesita referencias externas (planetas con biosfera conocida), lo que hoy solo cumple la Tierra.
- Hasta recalcularla con datos de entrada documentados, la tabla v2.0 debe tratarse como no válida (E0).
