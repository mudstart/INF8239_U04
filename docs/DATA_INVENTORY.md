# Inventario de datos, minimización y retención

- **Sistema:** Territorial Review DSS - Synthetic
- **Política:** 2026-10-21 (`configs/governance.yml`)
- **Responsable del inventario:** Product Owner (A), con el Data Engineer (R). Ver `student_inputs/raci.csv`, actividad *Data quality*.

> Los **plazos de retención** son una **propuesta del estudiante** para un despliegue hipotético. Con datos sintéticos no hay obligación legal de retención; con datos reales, cada plazo tendría que validarse con la unidad legal frente a la Ley 172-13 (ver `docs/NORMATIVE_ANALYSIS.md`).

## 1. Inventario de activos

| Activo | Ubicación | Contenido | Datos personales | Sensibilidad | Acceso | Retención propuesta | Eliminación |
|---|---|---|---|---|---|---|---|
| Dataset de casos | `data/territorial_risk_synthetic.csv` | 640 casos sintéticos, 9 columnas | No (sintético) | Media: contiene `protected_group` y `age_band` | Equipo de datos | Mientras exista el repositorio del curso | Borrado del repositorio al cerrar el curso |
| Modelo entrenado | `models/*.joblib` (no versionado) | Pipeline de la logística o del árbol | No | Baja | ML Engineer | Solo la versión vigente y la anterior | Se regenera; las versiones viejas se borran al reentrenar |
| Configuración y política | `configs/governance.yml` | Puertas, usos prohibidos, línea base | No | Baja | Público en el repo | Mientras el sistema exista (versionado en Git) | No aplica: historial Git |
| Entradas del análisis | `student_inputs/*` | Impacto, interesados, riesgos, RACI, decisión | No | Baja | Público en el repo | Mientras el sistema exista | No aplica: historial Git |
| Reportes de auditoría | `reports/lab11/`, `reports/lab12/`, `reports/e08/` | Métricas agregadas por grupo e intersección | No (solo agregados) | Media: brechas por grupo | Equipo de datos y Product Owner | 2 años después del retiro del sistema (rendición de cuentas) | Borrado tras el plazo; la etiqueta Git conserva la referencia |
| Decisión trazable | `reports/lab13/deployment_decision.json` | Estado, versión, hashes, política, evidencia | No | Baja | Product Owner | Igual que los reportes de auditoría | Igual que los reportes |
| Evidencia de incidente | `reports/lab13/incident_evidence/` | Decisión, métricas y modelo al momento de la detección | No | Media | Institutional Owner y ML Engineer | 12 meses después de cerrar el postmortem | Borrado manual registrado en el postmortem |
| Postmortem | `reports/lab13/INCIDENT_POSTMORTEM.md` | Cronología, responsables y acciones | No | Baja | Institutional Owner | 2 años | Borrado tras el plazo |
| Registro de apelaciones *(previsto, no implementado)* | — | Caso, motivo, respuesta, revisor | **Sí, con datos reales** | Alta | Revisor independiente y Product Owner | 12 meses después de resolver la apelación; luego solo agregados anónimos | Seudonimizar y luego borrar |
| Registro de reordenamientos *(previsto)* | — | Caso, analista, justificación | Sí, del analista | Media | Product Owner | 12 meses | Borrado; se conservan agregados |

**No se recolectan** identificadores directos (`name`, `document_number`, `email`, `phone`): `validate_schema` los rechaza y `tests/test_privacy.py` lo prueba. No se publican secretos (`.streamlit/secrets.toml` está en `.gitignore`).

## 2. Minimización por columna

| Columna | Uso | ¿Necesaria? | Justificación |
|---|---|---|---|
| `case_id` | Trazabilidad, cola y apelación | Sí | Seudónimo. Sin él no se puede revisar ni apelar un caso. No entra al modelo |
| `received_date` | Corte temporal y orden FIFO | Sí | Lo exige la línea base y la evaluación temporal. No entra al modelo |
| `zone` | Variable del modelo | Sí, con vigilancia | Quitarla junto con `age_band` sube la brecha de FPR a 0.245, por encima de 0.16. Es un posible proxy (riesgo R06) |
| `previous_incidents` | Modelo y regla base | Sí | Variable principal de riesgo |
| `infrastructure_score` | Modelo | Sí | Variable principal de riesgo; posible proxy (R06) |
| `exposure` | Modelo y regla base | Sí | Variable principal de riesgo |
| `protected_group` | Solo auditoría | Sí, con acceso restringido | No entra al modelo ni se muestra en la cola. Sin él no se puede auditar la equidad |
| `age_band` | Variable del modelo y auditoría | **No para el modelo** | Ver la sección 3 |
| `target` | Entrenamiento y evaluación | Sí | Necesaria para medir el desempeño |

## 3. Evidencia de minimización: `age_band`

`uv run python scripts/e08_minimization.py` genera `reports/e08/minimization.csv`:

| Variante | Variables | Recall | FPR | Recall G1 | Recall G2 | Brecha recall | Brecha FPR |
|---|---|---|---|---|---|---|---|
| Actual (zone + age_band) | 5 | 0.717 | 0.279 | 0.653 | 0.791 | 0.138 | 0.125 |
| **Sin age_band** | 4 | 0.717 | **0.265** | 0.653 | 0.791 | 0.138 | 0.144 |
| Sin zone ni age_band | 3 | 0.728 | 0.250 | 0.653 | 0.814 | 0.161 | 0.245 |

**Lectura:** quitar `age_band` no cambia el recall global ni el de ningún grupo, y baja el FPR. La variable sensible no aporta utilidad, así que el principio de minimización indica **retirarla del modelo y conservarla solo para auditar**. A cambio, la brecha de FPR sube de 0.125 a 0.144, aunque sigue dentro de 0.16. Quitar también `zone` rompe la puerta de FPR.

**Propuesta:** retirar `age_band` del modelo en la próxima versión, y volver a correr la auditoría del LAB12 y las puertas del LAB13 antes de cambiarlo. El cambio no se aplicó todavía, para no alterar la evidencia ya entregada. Lo decide el Product Owner.

## 4. Revisión del inventario

El inventario se revisa en cada cambio de datos, de modelo o de política, y como mínimo cada 6 meses. La responsabilidad es del Product Owner (A), con el Data Engineer (R).
