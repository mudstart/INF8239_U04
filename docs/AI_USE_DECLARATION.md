# Declaración de uso de IA

- **Herramienta utilizada:** Claude, asistente de IA generativa de Anthropic (modelo Claude Opus 5.5), el 21 de octubre de 2026.
- **Para qué se usó:** comprobar si el proyecto cumplía los requisitos del LAB11, preparar una primera versión de los archivos de la evaluación de impacto, correr los scripts y las pruebas, y arreglar una falla del script entregado con el proyecto base.
- **Partes en las que intervino la IA:**
  - `student_inputs/lab11_impact.yml`: primera redacción de los nueve campos de la ficha de propósito.
  - `student_inputs/stakeholders.csv`: beneficios, daños y formas de participación de los cuatro actores.
  - `student_inputs/risk_register.csv`: nueve riesgos (R01 a R09), cada uno con su escenario, control, responsable y evidencia.
  - `reports/lab11/DECISION_RECORD.md`: análisis de los tres riesgos con mayor prioridad y la recomendación de revisar (REVIEW).
  - `scripts/lab11_impact.py`: ajuste técnico para que el script se pudiera ejecutar.
- **Fallas encontradas y cómo se resolvieron:** el script `scripts/lab11_impact.py` no se podía ejecutar (`SyntaxError`), porque un texto entre comillas tenía saltos de línea escritos directamente. Se cambiaron por la secuencia `\n` y se añadió una validación para que el script no reemplace `DECISION_RECORD.md` cuando ese archivo ya existe.
- **Revisión humana:** leí con calma todo lo que generó la IA y lo fui contrastando con el caso y con lo que vimos en la unidad. Revisé que el propósito y los actores tuvieran sentido, y que cada riesgo fuera concreto y tuviera un responsable y una evidencia que se pudieran verificar. También ejecuté el script y las pruebas para confirmar que todo funcionaba. La recomendación de REVISAR la hago mía: sin las métricas por grupo del LAB12 no me parece responsable desplegar el sistema todavía.

