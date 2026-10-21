# Registro de decisión · LAB11 · Evaluación de impacto ético

- **Sistema:** Territorial Review DSS - Synthetic
- **Fecha:** 2026-10-21
- **Responsable de la decisión:** Product Owner del DSS territorial (rinde cuentas ante el Institutional Owner)
- **Insumos:** `student_inputs/lab11_impact.yml`, `reports/lab11/stakeholders.csv`, `reports/lab11/risk_register_scored.csv` y `reports/lab11/rmf_summary.json`

## 1. Propósito y proporcionalidad

El sistema solo **ordena la cola semanal de revisión técnica**. No decide intervención, elegibilidad ni recursos, y un analista humano revisa cada caso. Que haga falta un modelo se justifica únicamente si mejora a la **alternativa no predictiva**: FIFO, adelantando los casos con 3 o más incidentes previos o exposición mayor a 0.7. Esa alternativa es más transparente y menos invasiva. Mientras el modelo no demuestre que la supera, la opción proporcional es la regla.

## 2. Los tres riesgos prioritarios

`risk_register_scored.csv` ordena la atención con prioridad = probabilidad × impacto. El orden es una ayuda y no una verdad matemática. Abajo reviso los escenarios uno por uno.

| Rank | Riesgo | Prioridad | Responsable | Residual |
|---|---|---|---|---|
| 1 | R01 · Menor recall para un grupo protegido o una zona, lo que retrasa casos de alto riesgo | 12 (3×4) | Data Scientist | **alto** |
| 2 | R02 · Sesgo de automatización: los analistas aceptan el orden sin revisarlo | 9 (3×3) | Product Owner | medio |
| 3 | R04 · Deriva temporal que degrada el recall sin que nadie lo detecte | 9 (3×3) | ML Engineer | medio |

**R01 (crítico).** Es el único riesgo con residual alto. Quitar `protected_group` y `age_band` de las features no garantiza equidad, porque `zone` e `infrastructure_score` pueden funcionar como proxies (lo trata R06). El control real son las puertas `max_recall_gap ≤ 0.16` y `max_fpr_gap ≤ 0.16`, y **todavía no hay evidencia medida**: `rmf_summary.json` marca MEASURE como *LAB12 pending*. Que exista el archivo de configuración no prueba que el control funcione.

**R02.** Un sistema de apoyo deja de serlo si el operador no ejerce su juicio. Los controles son la justificación obligatoria al reordenar y el muestreo mensual. Su eficacia depende de la capacitación y no se ha medido.

**R04.** El split temporal reduce el problema, pero los datos sintéticos no muestran la deriva real. El monitoreo mensual con retiro automático a la regla es el control, y todavía no existe un reporte de monitoreo.

**Empate a revisar.** R06 (proxies territoriales) también tiene prioridad 9. Lo trato con la misma urgencia que R04 porque afecta a las comunidades con menos poder (`power = low` en stakeholders) y amplifica R01. El orden automático lo deja cuarto solo por el desempate en el CSV.

## 3. Incertidumbre

- No hay métricas globales ni por subgrupo (LAB12 pendiente). No sabemos si el modelo supera a la línea base ni si cumple las puertas de equidad.
- El dataset es sintético: el `target` puede no representar el daño real (R09), y nada de esto vale para poblaciones reales.
- Las probabilidades e impactos (1–4) son juicios del equipo, no frecuencias observadas.

## 4. Decisión

**REVISAR (REVIEW): no se despliega. Se continúa solo hacia la auditoría técnica del LAB12.**

Se puede pasar a **GO** únicamente si se cumplen todas estas condiciones:
1. El LAB12 muestra `recall ≥ 0.68` y diferencias de recall y FPR por grupo `≤ 0.16`.
2. El modelo mejora de forma demostrable a la regla FIFO más reglas.
3. Están operativos el formulario de apelación (SLA de 5 días hábiles con un revisor independiente) y el registro de reordenamientos.
4. El runbook documenta el rollback a la regla no predictiva.

## 5. Condición de retiro (STOP)

Se retira el modelo y se vuelve a la regla no predictiva si ocurre cualquiera de estas condiciones:
- recall menor a 0.68;
- diferencia de recall o de FPR entre grupos mayor a 0.16;
- latencia mayor a 500 ms;
- un incidente de uso fuera de alcance (elegibilidad, intervención automática, emergencia, perfilamiento);
- que el piloto no mejore la línea base.

El Product Owner decide en un máximo de 48 horas y lo registra en `docs/RUNBOOK.md`.

## 6. Revisión humana y apelación

Un analista revisa cada caso. Cualquier persona afectada o un analista puede apelar la prioridad mediante un formulario a la coordinación técnica, y responde un revisor que no generó la recomendación. Las apelaciones aceptadas alimentan la auditoría por subgrupo.

## 7. Marco de referencia

NIST AI RMF 1.0 (GOVERN, MAP, MEASURE, MANAGE), DOI 10.6028/NIST.AI.100-1; OECD Recommendation on AI, DOI 10.1787/cc2e1d3e-en.
