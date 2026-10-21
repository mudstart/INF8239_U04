# Plan de monitoreo

- **Sistema:** Territorial Review DSS - Synthetic
- **Política:** 2026-10-21 (`configs/governance.yml`, sección `monitoring`)
- **Responsable:** ML Engineer (R) y Product Owner (A), actividad *Monitoring and drift* en `student_inputs/raci.csv`.

## Qué se monitorea

| Señal | Métrica | Umbral | Fuente | Si se activa |
|---|---|---|---|---|
| Deriva de datos | PSI por variable (`previous_incidents`, `infrastructure_score`, `exposure`, `zone`, `age_band`, `protected_group`, `target`) | Aviso si es 0.10 o más; alerta si es 0.25 o más | `scripts/monitor.py` | Aviso: se anota en el reporte. Alerta: se abre el runbook |
| Desempeño | Recall global | 0.68 o más | Puertas (`lab13_governance.py`) | REVIEW y runbook |
| Equidad | Recall mínimo por grupo; brechas de recall y de FPR | Recall por grupo de 0.68 o más; brechas de 0.16 o menos | Puertas | REVIEW, runbook y auditoría del LAB12 |
| Costo | Latencia por caso; tamaño del modelo | 500 ms o menos; 1024 KB o menos | Puertas | REVIEW |
| Privacidad | Identificadores directos en los datos | Ninguno | `validate_schema` | **STOP** |
| Supervisión humana | Reordenamientos y apelaciones aceptadas *(previsto)* | Aumento sostenido de un mes a otro | Registros previstos en `docs/DATA_INVENTORY.md` | Revisión del Product Owner |

Los umbrales de 0.10 y 0.25 para el PSI son convenciones de la industria, no estándares normativos. Se adoptan como criterio propio y se revisan con la evidencia que se acumule.

## Cuándo y cómo
- **Frecuencia:** cada mes, y además antes de cada cambio de datos, de modelo o de política.
- **Comando:** `uv run python scripts/monitor.py`. Genera `reports/monitoring/monitoring_report.json` y `reports/monitoring/drift_psi.csv`.
- **Ventanas:** la referencia es la ventana de entrenamiento y la ventana actual son los casos posteriores. En un despliegue real, la ventana actual sería el último mes.
- **Tablero:** la sección «Monitoreo de deriva (PSI)» de `app.py` muestra el mismo cálculo.
- **Pruebas:** `tests/test_monitoring.py` comprueba que dos muestras iguales no tienen deriva, que un desplazamiento de `exposure` genera una alerta y que la ventana actual no tiene alertas de deriva.

## Resultado actual (2026-10-21)

| Variable | PSI | Estado |
|---|---|---|
| previous_incidents | 0.084 | OK |
| infrastructure_score | 0.067 | OK |
| exposure | 0.031 | OK |
| zone | 0.015 | OK |
| age_band | 0.038 | OK |
| protected_group | 0.001 | OK |
| target | 0.000 | OK |

No hay deriva de datos. **La alerta activa viene de la puerta `group_recall`**: el recall de G1 es 0.653, menor a 0.68. Se escala al Product Owner, y la respuesta ya está registrada en `reports/lab13/INCIDENT_POSTMORTEM.md`.

## Escalamiento
Cada alerta se escala al Accountable de *Monitoring and drift* (Product Owner), que activa `docs/RUNBOOK.md`. El reporte mensual es el traspaso 4 de `docs/HANDOFF.md`.
