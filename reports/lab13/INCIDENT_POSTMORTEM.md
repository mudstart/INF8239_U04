# Simulacro de incidente · postmortem

- **Detección:** 2026-10-21T20:48:16.898261+00:00
- **Señal:** puertas fallidas: group_recall. Recall del grupo G1 = 0.653 (mínimo 0.68); recall global = 0.717.
- **Clasificación:** incidente de equidad, severidad alta (riesgo R01 del LAB11: revisión tardía de casos con riesgo real en un grupo).
- **Contención:** estado REVIEW. El modelo queda en modo sombra y la cola se ordena con la línea base segura: FIFO, moving up cases with previous_incidents >= 3 or exposure > 0.7. Autoridad: Product Owner (A); ejecuta ML Engineer (R).
- **Preservación de evidencia:** la decisión, las métricas por grupo y el modelo quedan guardados en `reports/lab13/incident_evidence/` (sha256 de datos 2af1858fe874, sha256 de configuración 4e9fd0c25065, política 2026-10-21).
- **Comunicación:** aviso interno a los analistas y al Product Owner en menos de 24 h; el Product Owner informa a Affected representatives que la cola volvió a la regla transparente y cómo apelar (A: Institutional Owner).
- **Rollback:** la línea base segura está activa; ninguna salida del modelo ordena la cola hasta que pase la puerta por grupo.
- **Acciones correctivas, responsables y fechas:**
  1. Investigar los proxies (zone, infrastructure_score) y la caída de recall de G1 por franja de edad: Data Scientist, antes del 2026-11-04.
  2. Validar un umbral por grupo o conseguir más casos de G1 y repetir la auditoría del LAB12: Data Scientist, antes del 2026-11-20.
  3. Revisar las apelaciones recibidas durante el incidente: Independent Reviewer, antes del 2026-10-28.
  4. Decidir GO, REVIEW o STOP con la nueva evidencia y registrarlo: Product Owner, antes del 2026-11-25.
- **Responsable del postmortem:** Institutional Owner (A), con ML Engineer (R).
