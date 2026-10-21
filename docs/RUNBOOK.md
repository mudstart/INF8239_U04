# Incident Runbook — Territorial Review DSS

Los roles salen de `student_inputs/raci.csv`. El simulacro se ejecuta con `uv run python scripts/simulate_incident.py`, y su resultado está en `reports/lab13/INCIDENT_POSTMORTEM.md`.

1. **Detection and classification:** la detección es automática y se apoya en las puertas de `configs/governance.yml`, que se evalúan con `scripts/lab13_governance.py`, y en el monitoreo mensual de deriva con `scripts/monitor.py` (ver `docs/MONITORING_PLAN.md`), cada mes y antes de cada cambio de modelo o de datos. Cualquier puerta fallida produce REVIEW. Cada señal se clasifica así:
   - **Equidad** (`group_recall`, `recall_gap`, `fpr_gap`): severidad alta.
   - **Desempeño o deriva** (`recall`, o un PSI de 0.25 o más en `monitor.py`): severidad alta.
   - **Costo** (`latency`, `model_size`): severidad media.
   - **Privacidad** (`validate_schema` rechaza identificadores directos): **STOP inmediato**.
   - **Uso fuera de alcance:** **STOP inmediato**.

   También son señales un aumento de apelaciones aceptadas y los reordenamientos frecuentes de los analistas.
2. **Containment authority:** la autoridad la tiene el **Product Owner** (A), que puede poner el sistema en REVIEW o STOP sin esperar a nadie. Ejecuta el ML Engineer (R). En incidentes de privacidad o de uso fuera de alcance, la autoridad pasa al **Institutional Owner** (A de *Incident response*). La contención consiste en sacar el modelo del orden de la cola y dejarlo en modo sombra.
3. **Evidence preservation:** antes de cambiar nada se guardan, en `reports/lab13/incident_evidence/`, la decisión trazable (versión, hashes de datos y de configuración, política y métricas), las métricas por grupo y el artefacto del modelo. No se sobrescriben los reportes del LAB12. Los commits y la etiqueta de Git identifican la versión desplegada.
4. **Internal and affected-party communication:**
   - **Interna:** aviso a los analistas y al Product Owner en menos de 24 h, con la señal, la contención y la acción esperada.
   - **Hacia los afectados:** el Product Owner (R de *External communication*, con A del Institutional Owner) informa a los representantes de los afectados que la cola volvió a la regla transparente y cómo apelar.
   - No se publican datos de casos.
5. **Rollback or safe baseline:** se vuelve a la línea base segura de `configs/governance.yml`: FIFO, adelantando los casos con `previous_incidents >= 3` o `exposure > 0.7`. Decide el Product Owner (A) y ejecuta el ML Engineer (R). La regla sigue activa hasta que todas las puertas pasen con evidencia nueva y el Product Owner registre un GO. Plazo máximo para decidir: 48 h.
6. **Postmortem, owner and due date:**
   - **Responsable:** el Institutional Owner (A), con el ML Engineer (R).
   - **Plazo:** el postmortem se entrega en un máximo de 10 días hábiles.
   - **Contenido:** cronología, causa probable (sin afirmar causalidad sin evidencia), acciones correctivas con responsable y fecha, y la decisión final GO, REVIEW o STOP.
   - **Registro:** las apelaciones del periodo se revisan y se suman a la auditoría.
   - **Último simulacro:** 2026-10-21. Señal: `group_recall` (recall de G1 de 0.653). Acciones con fechas de entrega del 2026-10-28 al 2026-11-25.
