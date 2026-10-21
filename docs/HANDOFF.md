# Traspaso entre roles (handoff)

El RACI (`student_inputs/raci.csv`) define quién es responsable de cada actividad. Este documento define **qué se entrega, a quién y con qué criterio de aceptación** cuando el trabajo pasa de un rol a otro. Ningún traspaso se da por hecho si no cumple su criterio: el receptor lo devuelve y queda registrado.

## Cadena de traspasos

| # | Entrega (R) | Recibe | Artefactos | Criterio de aceptación (verificable) | Quién aprueba (A) |
|---|---|---|---|---|---|
| 1 | Data Engineer | Data Scientist | `data/*.csv`, `docs/DATASET_CARD.md`, hash sha256 del archivo | `check_environment.py` da `dataset_status: valid`; `tests/test_data.py` y `tests/test_privacy.py` pasan; el hash está anotado en la Dataset Card | Product Owner |
| 2 | Data Scientist | Product Owner | `reports/lab12/` (métricas, intersecciones, comparación), `student_inputs/lab12_decision.yml`, `reports/e08/minimization.csv` | Métricas por grupo e intersección con conteos; política de soporte aplicada; intervalos de las brechas; decisión documentada (`validate_lab12_decision.py`) | Product Owner |
| 3 | Product Owner | ML Engineer | Decisión firmada (LIMITAR), `configs/governance.yml` con `policy_version` | `lab13_governance.py` produce `deployment_decision.json` con versión, política, evidencia y acción humana; `pytest -q` en verde | Product Owner |
| 4 | ML Engineer | Product Owner | Reporte mensual de monitoreo (`reports/monitoring/`) | PSI por variable y estado de las puertas; cualquier alerta queda escalada según el runbook | Product Owner |
| 5 | ML Engineer | Institutional Owner | `reports/lab13/INCIDENT_POSTMORTEM.md`, `reports/lab13/incident_evidence/` | Evidencia preservada antes de cambiar nada; acciones con responsable y fecha | Institutional Owner |
| 6 | Revisor independiente | Data Scientist | Registro de apelaciones resueltas (previsto) | Motivo, decisión y si el modelo se equivocó; se usa en la siguiente auditoría | Product Owner |
| 7 | Product Owner | Representantes de afectados | Aviso de cambio, de incidente o de rollback | Explica qué cambió, cómo apelar y quién responde; sin datos de casos | Institutional Owner |

## Reglas del traspaso
- **Nada pasa sin evidencia:** el receptor verifica el criterio con el comando o el archivo indicado, no con una afirmación.
- **Un solo Accountable por traspaso:** coincide con el RACI y lo valida `validate_raci`.
- **Versión fija:** cada traspaso cita el commit o la etiqueta Git (`u04-e07`, `u04-lab13`) y los hashes de `deployment_decision.json`.
- **Devolución:** si el criterio no se cumple, el receptor devuelve el traspaso con el motivo, y el responsable (R) lo corrige.
- **Cambios de personas:** si un rol cambia de persona, el saliente entrega este documento, el RACI y el último reporte de monitoreo, y el Product Owner confirma el relevo.

## Registro de traspaso (plantilla)

| Campo | Valor |
|---|---|
| Fecha | |
| Traspaso # | |
| Entrega (rol) | |
| Recibe (rol) | |
| Versión (commit o etiqueta) | |
| Artefactos | |
| Criterio verificado con | |
| Resultado | Aceptado / Devuelto (motivo) |
| Aprueba (A) | |

## Ejemplo: traspaso 3 en este proyecto

| Campo | Valor |
|---|---|
| Fecha | 2026-10-21 |
| Entrega | Product Owner → ML Engineer |
| Versión | etiqueta `u04-lab13`, política 2026-10-21 |
| Artefactos | `student_inputs/lab12_decision.yml` (LIMITAR), `configs/governance.yml` |
| Criterio verificado con | `uv run python scripts/lab13_governance.py` → REVIEW (`group_recall`), con la decisión trazable; `uv run pytest -q` en verde |
| Resultado | Aceptado: el modelo solo pasa a modo sombra y la regla base sigue ordenando la cola |
| Aprueba (A) | Product Owner |
