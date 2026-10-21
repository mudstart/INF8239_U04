# Declaración de uso de IA

- **Herramienta utilizada:** Claude, asistente de IA generativa de Anthropic (modelo Claude Opus 5.5), el 21 de octubre de 2026, en la aplicación Claude.
- **Para qué se usó:**
  - comprobar si el proyecto cumplía los requisitos del LAB11, el LAB12 y el E07;
  - preparar una primera versión de los archivos de la evaluación de impacto y de la auditoría;
  - correr los scripts y las pruebas;
  - arreglar una falla del script entregado con el proyecto base;
  - redactar el análisis normativo;
  - en el LAB13, ajustar las puertas y la trazabilidad del DSS, redactar la Model Card, el runbook y la Dataset Card, y corregir el simulacro de incidente.

  Los commits y el push los hice yo.

## Prompts relevantes

| Fase | Prompt (resumido) | Resultado |
|---|---|---|
| LAB11 | Preparar borradores de la evaluación de impacto a partir del enunciado | Ficha, interesados, riesgos y registro de decisión |
| E07 | Contrastar el trabajo con el mandato y la rúbrica | Lista de pendientes |
| LAB12 | Ejecutar la auditoría de equidad y preparar la decisión | Métricas, comparación de modelos y borrador de decisión |
| Documento | Integrar las evidencias en un PDF con formato académico | Este documento |
| LAB13 | Completar el DSS gobernado a partir del enunciado | Puertas, RACI, Model Card, runbook, simulacro y tablero |

## Partes en las que intervino la IA

**LAB11**
- `student_inputs/lab11_impact.yml`: primera redacción de los nueve campos de la ficha de propósito.
- `student_inputs/stakeholders.csv`: beneficios, daños y formas de participación de los cuatro actores.
- `student_inputs/risk_register.csv`: nueve riesgos (R01 a R09), cada uno con su escenario, control, responsable y evidencia.
- `reports/lab11/DECISION_RECORD.md`: análisis de los tres riesgos con mayor prioridad y la recomendación de revisar (REVIEW).
- `scripts/lab11_impact.py`: ajuste técnico para que el script se pudiera ejecutar, y MEASURE ligado a la evidencia del LAB12.

**LAB12**
- `scripts/lab12_compare.py`: script nuevo. Compara la regla no predictiva con los dos modelos, calcula intervalos bootstrap de las brechas y aplica una política de soporte para las intersecciones.
- `student_inputs/lab12_decision.yml`: borrador de los seis campos de la decisión.
- `reports/lab12/AUDIT_REPORT.md`: informe de auditoría con las métricas, los trade-offs, Green AI y la decisión LIMITAR.

**E07**
- `docs/NORMATIVE_ANALYSIS.md`: separación entre obligación legal, marco voluntario y recomendación ética. La IA buscó en la web el estado regulatorio de República Dominicana; las fuentes están citadas en el documento.

**LAB13**
- `src/inf8239_u04/governance.py` y `pipeline.py`: nueva puerta `group_recall` (recall mínimo por grupo), validación de un único Accountable en el RACI y registro trazable (versión, hashes, política, evidencia y acción humana).
- `configs/governance.yml`: `policy_version`, `safe_baseline` y `min_group_recall`.
- `student_inputs/raci.csv`: cinco actividades nuevas (auditoría de equidad, monitoreo, apelación, rollback y comunicación externa).
- `scripts/lab13_governance.py` y `app.py`: la decisión trazable, las puertas, la comparación Green AI, la decisión humana y el estado del último simulacro de incidente se muestran en el tablero.
- `scripts/simulate_incident.py`: corrección y simulacro basado en la señal real de las puertas; genera `reports/lab13/INCIDENT_POSTMORTEM.md`.
- `src/inf8239_u04/dss.py`: módulo nuevo con la cola priorizada por caso (probabilidad, prioridad, acción recomendada, explicación y discrepancias entre la regla y el modelo), que se muestra en el tablero.
- `docs/MODEL_CARD.md`, `docs/RUNBOOK.md` y `docs/DATASET_CARD.md`: redacción con la evidencia de los LAB11 y LAB12.
- `tests/`: ocho pruebas nuevas (RACI, puerta por grupo, trazabilidad, columna faltante y cola priorizada).

**E08**
- `docs/DATA_INVENTORY.md`: inventario de activos, minimización por columna y propuesta de plazos de retención (los plazos son una propuesta que el estudiante debe confirmar).
- `scripts/e08_minimization.py`: compara el modelo con y sin `age_band` y con y sin `zone`; genera `reports/e08/minimization.csv`.
- `docs/DATASET_CARD.md`: reestructurada en formato datasheet, con rangos y conteos verificados en los datos.
- `docs/HANDOFF.md`: siete traspasos entre roles, con criterios de aceptación verificables.
- `src/inf8239_u04/monitoring.py`, `scripts/monitor.py` y `docs/MONITORING_PLAN.md`: monitoreo de deriva con PSI y escalamiento; la sección se muestra en el tablero y tiene tres pruebas nuevas.
- `docs/NORMATIVE_ANALYSIS.md`: sección «Aplicación a la gobernanza (E08)».

Las métricas no las escribió la IA: salen de ejecutar `scripts/lab12_audit.py` y `scripts/lab12_compare.py`, y se pueden reproducir con la semilla 42.

## Fallas encontradas y cómo se resolvieron

1. **Error del script base:** `scripts/lab11_impact.py` no se podía ejecutar (`SyntaxError`), porque un texto entre comillas tenía saltos de línea escritos directamente. Se cambiaron por la secuencia `\n` y se añadió una validación para que el script no reemplace `DECISION_RECORD.md` cuando ese archivo ya existe.
2. **Error de la IA:** en el LAB11 la IA escribió que `age_band` estaba excluida del modelo. Era falso: `features()` en `src/inf8239_u04/data.py` sí la incluye. El error apareció al revisar el código en el LAB12 y se corrigió en `risk_register.csv`, `DECISION_RECORD.md` y `AUDIT_REPORT.md`.
3. **Puerta automática engañosa:** `deployment_decision` devolvía GO para la regresión logística porque solo mira el recall global. La revisión por grupo mostró que G1 tiene un recall de 0.653, por debajo de 0.68, y por eso no se aceptó el GO.
4. **Dato faltante en el proyecto:** el LAB12 pide no interpretar grupos «con menos observaciones que el mínimo documentado», pero el proyecto no documentaba ningún mínimo. Se fijó en 20 casos y 10 positivos (`reports/lab12/support_policy.json`). Es un criterio propio, no un estándar.
5. **Error del script de simulacro:** `scripts/simulate_incident.py` tenía el mismo `SyntaxError` que el script del LAB11. Se reescribió para que el simulacro use la señal real de las puertas y no deje campos en `REPLACE`.
6. **Puerta corregida en el LAB13:** la falla 3 se resolvió en el código. La nueva puerta `group_recall` hace que el pipeline devuelva REVIEW, como exige el laboratorio («una puerta fallida debe producir REVIEW o STOP, nunca ocultarse»).
7. **Error de la IA:** en el primer borrador de la Dataset Card, la IA escribió «un caso por día». Al verificarlo en los datos resultó falso: hay 324 fechas distintas entre el 2026-01-01 y el 2026-12-27. Se corrigió.
8. **Hallazgo de minimización:** al medir el modelo sin `age_band`, el recall global y el de cada grupo no cambiaron, y el FPR bajó de 0.279 a 0.265. La IA propuso retirar la variable; el cambio **no se aplicó** para no alterar la evidencia entregada, y queda como decisión del Product Owner.

## Revisión humana

Leí con calma todo lo que generó la IA y lo fui contrastando con el caso y con lo que vimos en la unidad. Revisé que el propósito y los actores tuvieran sentido, y que cada riesgo fuera concreto y tuviera un responsable y una evidencia que se pudieran verificar. También ejecuté el script y las pruebas para confirmar que todo funcionaba. La recomendación de REVISAR la hago mía: sin las métricas por grupo del LAB12 no me parece responsable desplegar el sistema todavía.

En el LAB12 revisé las métricas por grupo y por intersección, y la comparación con la regla no predictiva. Con esa evidencia, la decisión final que asumo es LIMITAR: el modelo funciona bien en promedio, pero falla justo en el grupo G1, así que solo lo acepto como piloto en modo sombra con revisión humana. Las normas que cito en el análisis normativo las verifiqué en fuentes oficiales.
