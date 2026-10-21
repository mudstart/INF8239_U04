import json, shutil
from datetime import datetime,timezone,timedelta
from pathlib import Path
import pandas as pd
from inf8239_u04.data import load_data
from inf8239_u04.governance import load_config,traceable_record
from inf8239_u04.pipeline import run
# Drill: run the governed pipeline, treat any failed gate as the incident signal and record the response.
cfg=load_config(); result=run(load_data(),cfg["gates"]); record=traceable_record(result,cfg)
now=datetime.now(timezone.utc); out=Path("reports/lab13"); evidence=out/"incident_evidence"; evidence.mkdir(parents=True,exist_ok=True)
(evidence/"decision_at_detection.json").write_text(json.dumps(record,indent=2),encoding="utf-8"); result["by_group"].to_csv(evidence/"by_group_at_detection.csv")
if Path("models/model.joblib").exists(): shutil.copy("models/model.joblib",evidence/"model_at_detection.joblib")
raci=pd.read_csv("student_inputs/raci.csv").set_index("activity")
owner=lambda activity,role="A": raci.loc[activity,role]
g=result["by_group"]; worst=g["recall"].astype(float).idxmin()
signal=", ".join(record["failed"]) or "ninguna (simulacro sin puerta fallida)"
due=lambda days:(now+timedelta(days=days)).date().isoformat()
text=f"""# Simulacro de incidente · postmortem

- **Detección:** {now.isoformat()}
- **Señal:** puertas fallidas: {signal}. Recall del grupo {worst} = {g.loc[worst,'recall']:.3f} (mínimo {cfg['gates']['min_group_recall']}); recall global = {result['metrics']['recall']:.3f}.
- **Clasificación:** incidente de equidad, severidad alta (riesgo R01 del LAB11: revisión tardía de casos con riesgo real en un grupo).
- **Contención:** estado {record['status']}. El modelo queda en modo sombra y la cola se ordena con la línea base segura: {cfg['safe_baseline']}. Autoridad: {owner('Rollback to safe baseline')} (A); ejecuta {owner('Rollback to safe baseline','R')} (R).
- **Preservación de evidencia:** la decisión, las métricas por grupo y el modelo quedan guardados en `reports/lab13/incident_evidence/` (sha256 de datos {record['version']['data_sha256']}, sha256 de configuración {record['version']['config_sha256']}, política {cfg['policy_version']}).
- **Comunicación:** aviso interno a los analistas y al Product Owner en menos de 24 h; el {owner('External communication','R')} informa a {owner('External communication','I')} que la cola volvió a la regla transparente y cómo apelar (A: {owner('External communication')}).
- **Rollback:** la línea base segura está activa; ninguna salida del modelo ordena la cola hasta que pase la puerta por grupo.
- **Acciones correctivas, responsables y fechas:**
  1. Investigar los proxies (zone, infrastructure_score) y la caída de recall de {worst} por franja de edad: {owner('Fairness audit','R')}, antes del {due(14)}.
  2. Validar un umbral por grupo o conseguir más casos de {worst} y repetir la auditoría del LAB12: {owner('Model validation','R')}, antes del {due(30)}.
  3. Revisar las apelaciones recibidas durante el incidente: {owner('Appeal review','R')}, antes del {due(7)}.
  4. Decidir GO, REVIEW o STOP con la nueva evidencia y registrarlo: {owner('Deployment')}, antes del {due(35)}.
- **Responsable del postmortem:** {owner('Incident response')} (A), con {owner('Incident response','R')} (R).
"""
path=out/"INCIDENT_POSTMORTEM.md"; path.write_text(text,encoding="utf-8"); print(path)
