# Model Card — Territorial Review DSS (regresión logística)

Formato basado en Mitchell et al. (2019), *Model Cards for Model Reporting*, DOI 10.1145/3287560.3287596.

| Campo | Valor |
|---|---|
| Modelo | Regresión logística (`class_weight="balanced"`, `max_iter=1200`, `random_state=42`) con one-hot para `zone` y `age_band`, y escalado estándar para las variables numéricas |
| Versión | paquete 0.1.0 · política 2026-10-21 · los hashes de datos y configuración están en `reports/lab13/deployment_decision.json` |
| Artefacto | `models/logistic.joblib` (3.6 KB; no se versiona en Git y se regenera con `scripts/lab12_audit.py`) |

## Intended use
Ordenar la cola semanal de revisión técnica de casos territoriales **sintéticos**, para que un analista revise primero los de mayor riesgo. La salida es un orden de prioridad. Un humano revisa cada caso y el Product Owner registra la decisión. Fuente: `student_inputs/lab11_impact.yml`.

**Salida del DSS** (`src/inf8239_u04/dss.py`, que se muestra en el tablero): por cada caso, la probabilidad, la señal del modelo (Alta si es 0.7 o más, Media si es 0.5 o más, Baja en otro caso), la posición en la cola, la acción recomendada y las dos variables que más pesan (contribución lineal de la logística). Mientras la decisión no sea GO, la cola la ordena la regla base y el modelo solo se muestra en modo sombra. Las discrepancias entre la regla y el modelo se marcan para revisión humana. `protected_group` no se muestra ni se usa para priorizar.

## Out-of-scope use
Están prohibidos:
- intervención automática;
- decisiones de elegibilidad o de acceso a beneficios;
- declarar emergencias;
- atribuir culpabilidad;
- perfilar personas u hogares;
- usar el grupo protegido o la edad para priorizar;
- cualquier uso con datos o poblaciones reales.

Ver `configs/governance.yml` y la sección 1.5 del E07.

## Data and split
`data/territorial_risk_synthetic.csv`: 640 casos sintéticos, 55.2 % positivos, G1 = 396 y G2 = 244 (ver `docs/DATASET_CARD.md`).
- **Corte temporal 75/25:** entrenamiento hasta el 2026-09-24 y prueba desde el 2026-09-25 (n = 160; G1 = 101, G2 = 59).
- **Variables del modelo:** `zone`, `age_band`, `previous_incidents`, `infrastructure_score` y `exposure`.
- **Excluidas:** `case_id`, `received_date`, `protected_group` (solo se usa para auditar) y `target`.
- **Riesgo de proxies:** `age_band` está declarada sensible pero **sí** entra al modelo, y `zone` puede funcionar como proxy del grupo (riesgo R06).

## Global and subgroup evaluation
| Métrica (test) | Global | G1 | G2 |
|---|---|---|---|
| Accuracy | 0.719 | 0.703 | 0.746 |
| Recall | 0.717 | **0.653** | 0.791 |
| FPR | 0.279 | 0.250 | 0.375 |
| Tasa de selección | 0.531 | 0.446 | 0.678 |

- **Brecha de recall:** 0.138, con IC95 bootstrap de 0.009 a 0.322. **Brecha de FPR:** 0.125.
- **Puertas:** pasan recall global, brechas, latencia y tamaño. **Falla `group_recall`**, porque el recall de G1 (0.653) está por debajo de 0.68. Resultado: **REVIEW**.
- **Intersecciones con soporte suficiente** (20 o más casos y 10 o más positivos): recall de 0.56 en G1 · 30-44 y de 0.59 en G1 · 45-59, y FPR de 0.556 en G2 · 60+. Ver `reports/lab12/AUDIT_REPORT.md`.

Una brecha observada no prueba discriminación causal: es una señal que hay que investigar.

## Green AI evidence
| Alternativa | Recall | FPR | Brecha recall | Entrenamiento | Tamaño | Latencia/caso |
|---|---|---|---|---|---|---|
| Regla no predictiva | 0.837 | 0.544 | 0.131 | — | — | ~0 ms |
| **Regresión logística** | 0.717 | 0.279 | 0.138 | ~0.03–0.06 s | 3.6 KB | 0.02 ms |
| Árbol (max_depth=5) | 0.717 | 0.309 | 0.181 | ~0.06 s | 7.9 KB | 0.02 ms |

El árbol no mejora la utilidad, amplía las brechas y pesa más del doble. Se elige la logística como **opción suficiente**. El costo es despreciable frente a los límites (500 ms y 1024 KB). Fuente: `reports/lab12/model_comparison.csv`.

## Limitations, human oversight and appeal
**Limitaciones:**
- el test es pequeño;
- los intervalos de las brechas son amplios;
- hay cuatro intersecciones sin soporte;
- los datos son sintéticos y el `target` puede no representar el daño real (R09);
- hay riesgo de deriva temporal (R04).

**Supervisión humana:**
- un analista revisa cada caso;
- reordenar la cola exige una justificación registrada;
- el Product Owner puede anular, detener o hacer rollback a la regla.

**Decisión vigente:** **LIMITAR**, con piloto en modo sombra (`student_inputs/lab12_decision.yml`).

**Apelación:** formulario a la coordinación técnica; responde un revisor independiente en 5 días hábiles.

**Retiro:** recall menor a 0.68 (global o por grupo), brecha mayor a 0.16, latencia mayor a 500 ms, uso fuera de alcance o no superar la línea base.

## Owner and review date
- **Accountable:** Product Owner.
- **Responsible de la validación:** Data Scientist (ver `student_inputs/raci.csv`).
- **Fecha de esta versión:** 2026-10-21.
- **Próxima revisión:** 2026-11-25, o antes si se activa una alerta del runbook.
