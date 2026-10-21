# Dataset Card

Synthetic territorial-risk dataset generated with a fixed educational seed. It contains no real persons, locations, rates or official Dominican Republic statistics. Intended only to practice contracts, temporal evaluation, subgroup auditing and governance. Prohibited: operational profiling or inference about real populations.

Formato inspirado en Gebru et al. (2021), *Datasheets for Datasets*, DOI 10.1145/3458723.

## Procedencia
- **Archivo:** `data/territorial_risk_synthetic.csv`, incluido en el proyecto base del curso. Se generó con una semilla fija y no tiene ninguna fuente real.
- **Composición:** 640 casos con fecha de recepción entre el 2026-01-01 y el 2026-12-27 (324 fechas distintas).
- **Objetivo:** `target` es binario y tiene 55.2 % de positivos.
- **Grupos:** G1 = 396 y G2 = 244.

## Contrato de datos (`src/inf8239_u04/data.py`)
- **Columnas obligatorias:** `case_id`, `received_date`, `zone`, `protected_group`, `age_band`, `previous_incidents`, `infrastructure_score`, `exposure` y `target`. Si falta alguna, el dataset se rechaza antes de predecir (`tests/test_data.py`).
- **Identificadores directos prohibidos:** `name`, `document_number`, `email` y `phone`. Si aparece alguno, se rechaza (`tests/test_privacy.py` y `tests/test_data.py`).
- **Objetivo:** `target` solo puede tomar los valores 0 y 1.

## Exclusiones y atributos sensibles
- **Sensibles** (`configs/governance.yml`): `protected_group` y `age_band`.
- **`protected_group`:** no entra al modelo; se conserva solo para auditar.
- **`age_band`:** **sí** entra al modelo. Es un riesgo documentado que hay que justificar o revisar.
- **Fuera del modelo:** `case_id`, `received_date` y `target`.
- **Proxies:** quitar el atributo sensible no elimina el sesgo indirecto, porque `zone` e `infrastructure_score` pueden funcionar como proxies (riesgo R06).

## Corte temporal
Los datos se ordenan por `received_date` y se separan 75/25: entrenamiento hasta el 2026-09-24 y prueba desde el 2026-09-25 (160 casos). Así se evita evaluar con información del futuro.

## Limitaciones
- **Etiqueta didáctica:** el `target` puede no representar el daño real (R09).
- **Muestra pequeña** para el análisis interseccional: cuatro de las ocho intersecciones no tienen soporte suficiente.
- **Sin datos reales:** cualquier uso con datos reales exige una nueva evaluación de impacto y aplicar en pleno la Ley 172-13.
