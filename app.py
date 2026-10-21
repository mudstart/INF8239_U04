from pathlib import Path
import pandas as pd
import streamlit as st
import yaml
from inf8239_u04.data import load_data
from inf8239_u04.dss import prioritized_queue
from inf8239_u04.governance import load_config,traceable_record
from inf8239_u04.pipeline import run
st.set_page_config(page_title="Governed Green DSS",layout="wide")
st.title("DSS territorial sintético · Gobernanza y Green AI")
st.warning("Demostración educativa con datos sintéticos. No autoriza decisiones automáticas ni representa estadísticas reales.")
cfg=load_config(); result=run(load_data(),cfg["gates"]); record=traceable_record(result,cfg)
st.subheader("Propósito y autoridad"); st.write(cfg["purpose"]); st.write("Usos prohibidos:",", ".join(cfg["prohibited_uses"]))
st.caption("Límite de autoridad: el DSS solo ordena la cola de revisión. No declara emergencias, culpabilidad, elegibilidad ni intervención automática.")
c1,c2,c3,c4=st.columns(4); c1.metric("Accuracy",f"{result['metrics']['accuracy']:.3f}"); c2.metric("Recall",f"{result['metrics']['recall']:.3f}"); c3.metric("Recall mínimo por grupo",f"{result['metrics']['min_group_recall']:.3f}"); c4.metric("Decisión",result["decision"]["status"])
st.subheader("Métricas por grupo"); st.dataframe(result["by_group"],width="stretch")
st.subheader("Puertas de calidad")
st.dataframe(pd.DataFrame({"puerta":list(record["checks"]),"cumple":list(record["checks"].values())}),hide_index=True)
if record["failed"]: st.error(f"Puertas fallidas: {', '.join(record['failed'])}. La recomendación pasa a {record['status']}.")
st.subheader("Cola priorizada (casos de prueba)")
queue=prioritized_queue(result["model"],result["test"],record["status"])
if record["status"]!="GO": st.caption(f"Modo sombra: la recomendación {record['status']} hace que la regla base ({cfg['safe_baseline']}) ordene la cola. La probabilidad del modelo es solo evidencia de apoyo; las discrepancias entre regla y modelo se marcan para revisión humana.")
only=st.checkbox("Mostrar solo discrepancias entre regla y modelo")
shown=queue[queue.discrepancy] if only else queue
st.dataframe(shown.rename(columns={"priority":"prioridad","case_id":"caso","received_date":"recibido","zone":"zona","probability":"probabilidad","model_band":"señal del modelo","rule_first":"regla: primero","explanation":"variables que más pesan","recommended_action":"acción recomendada","discrepancy":"discrepancia"}),hide_index=True,width="stretch")
st.caption(f"{len(shown)} de {len(queue)} casos. No se muestra protected_group: el grupo protegido se usa solo para auditar, no para priorizar.")
comparison=Path("reports/lab12/model_comparison.csv")
if comparison.exists(): st.subheader("Alternativas y Green AI (LAB12)"); st.dataframe(pd.read_csv(comparison),hide_index=True)
st.subheader("Recomendación trazable"); st.json({k:record[k] for k in ["status","version","policy","human_action"]})
decision=Path("student_inputs/lab12_decision.yml")
if decision.exists(): st.subheader("Decisión humana registrada"); st.write(yaml.safe_load(decision.read_text(encoding="utf-8"))["recommendation"])
postmortem=Path("reports/lab13/INCIDENT_POSTMORTEM.md")
if postmortem.exists():
    text=postmortem.read_text(encoding="utf-8"); field=lambda name:next((l.split(":**",1)[1].strip() for l in text.splitlines() if l.startswith(f"- **{name}:**")),"—")
    st.subheader("Estado de incidentes"); st.warning(f"Último simulacro: {field('Detección')[:16].replace('T',' ')} UTC · {field('Señal')}")
    c1,c2=st.columns(2); c1.markdown(f"**Contención:** {field('Contención')}"); c2.markdown(f"**Responsable del postmortem:** {field('Responsable del postmortem')}")
    with st.expander("Ver postmortem completo"): st.markdown(text)
st.info("Acción humana: revisar evidencia, documentar la decisión y activar apelación o rollback cuando corresponda.")
