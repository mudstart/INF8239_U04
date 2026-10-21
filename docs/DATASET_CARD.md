# Dataset Card

Synthetic territorial-risk dataset generated with a fixed educational seed. It contains no real persons, locations, rates or official Dominican Republic statistics. Intended only to practice contracts, temporal evaluation, subgroup auditing and governance. Prohibited: operational profiling or inference about real populations.

Formato de *Datasheets for Datasets* (Gebru et al., 2021, DOI 10.1145/3458723).

| Campo | Valor |
|---|---|
| Archivo | `data/territorial_risk_synthetic.csv` |
| Versión | sha256 `2af1858fe874` (prefijo; ver `reports/lab13/deployment_decision.json`) |
| Etiquetas Git | `u04-e07`, `u04-lab13` |
| Responsable | Data Engineer (R) y Product Owner (A), actividad *Data quality* en `student_inputs/raci.csv` |

## Motivación
- **Para qué se creó:** para practicar contratos de datos, evaluación temporal, auditoría por subgrupos y gobernanza de un DSS en los LAB11 a LAB13 del curso INF-8239.
- **Quién lo creó:** viene incluido en el proyecto base del curso. Se generó con una semilla fija y no tiene financiamiento ni fuente externa.

## Composición
- **Tamaño:** 640 casos (filas), uno por caso territorial sintético. No hay valores faltantes ni filas duplicadas, y `case_id` es único.
- **Fechas:** `received_date` va del 2026-01-01 al 2026-12-27, con 324 fechas distintas.
- **Objetivo:** `target` es binario y tiene 55.2 % de positivos.

| Columna | Tipo | Valores |
|---|---|---|
| `case_id` | Seudónimo | `CASE-0001` … `CASE-0640` |
| `received_date` | Fecha | 2026-01-01 a 2026-12-27 |
| `zone` | Categórica | Sur 164 · Este 164 · Oeste 157 · Norte 155 |
| `protected_group` | Categórica sensible | G1 396 · G2 244 |
| `age_band` | Categórica sensible | 60+ 179 · 30-44 163 · 45-59 150 · 18-29 148 |
| `previous_incidents` | Entero | 0 a 9 (media 3.28) |
| `infrastructure_score` | Continua | 0.032 a 0.984 (media 0.519) |
| `exposure` | Continua | 0 a 1 (media 0.503) |
| `target` | Binaria | 0 / 1 |

- **Datos personales:** no tiene. Los registros no corresponden a personas, zonas ni estadísticas reales.

## Proceso de recolección
No hubo recolección: los datos son **sintéticos** y se generaron por programa con una semilla fija. No hubo consentimiento porque no hay personas reales. El proceso de generación no está documentado en el proyecto base, y esa es una limitación para validar el `target` (R09).

## Preprocesamiento y contrato
`src/inf8239_u04/data.py` aplica un contrato antes de usar los datos:
- **Columnas obligatorias:** si falta alguna, el dataset se rechaza antes de predecir (`tests/test_data.py`).
- **Identificadores directos prohibidos:** `name`, `document_number`, `email` y `phone`. Si aparece alguno, se rechaza (`tests/test_privacy.py` y `tests/test_data.py`).
- **Objetivo:** `target` solo puede tomar los valores 0 y 1.
- **Orden y partición:** los datos se ordenan por `received_date` y se separan 75/25. El entrenamiento va hasta el 2026-09-24 y la prueba desde el 2026-09-25 (160 casos). Así se evita evaluar con información del futuro.
- **Transformaciones del modelo:** one-hot para `zone` y `age_band`, y escalado estándar para las variables numéricas (`src/inf8239_u04/model.py`).

## Usos
- **Usos previstos:** priorizar la revisión humana de casos sintéticos, auditar la equidad y demostrar la gobernanza.
- **Usos prohibidos:** perfilamiento operativo, inferencias sobre poblaciones reales, intervención automática, elegibilidad y declarar emergencias (`configs/governance.yml`).
- **Atributos sensibles:** `protected_group` no entra al modelo y se usa solo para auditar. `age_band` **sí** entra al modelo, pero el análisis de minimización muestra que no aporta utilidad, así que se propone retirarla (`docs/DATA_INVENTORY.md`, sección 3).
- **Proxies:** quitar un atributo sensible no elimina el sesgo indirecto, porque `zone` e `infrastructure_score` pueden funcionar como proxies (riesgo R06).

## Distribución
El dataset se distribuye dentro del repositorio del curso (https://github.com/mudstart/INF8239_U04) para fines académicos. Como es sintético, no tiene restricciones de privacidad, pero no debe presentarse como información real.

## Mantenimiento
- **Responsable:** el Data Engineer (R) y el Product Owner (A).
- **Cambios:** cualquier cambio en el archivo cambia su hash. Hay que volver a correr `check_environment.py`, las auditorías del LAB12 y las puertas del LAB13, y actualizar esta ficha.
- **Retención y eliminación:** ver `docs/DATA_INVENTORY.md`.

## Limitaciones
- **Etiqueta didáctica:** el `target` puede no representar el daño real (R09).
- **Muestra pequeña** para el análisis interseccional: cuatro de las ocho intersecciones no tienen soporte suficiente.
- **Sin datos reales:** cualquier uso con datos reales exige una nueva evaluación de impacto y aplicar en pleno la Ley 172-13.
