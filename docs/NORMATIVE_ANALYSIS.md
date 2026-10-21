# Análisis normativo · Obligación legal, marco voluntario y recomendación ética

- **Sistema:** Territorial Review DSS - Synthetic
- **Fecha:** 2026-10-21
- **Alcance:** República Dominicana

> **Aviso:** este análisis lo preparé como estudiante y no es una opinión jurídica. Hay que verificar el estado de los proyectos de ley en el Congreso Nacional y la versión vigente de cada norma antes de citarla.

Distingo tres niveles porque tienen consecuencias distintas. Una **obligación legal** se puede exigir y sancionar. Un **marco voluntario** es una buena práctica que la institución adopta por decisión propia. Una **recomendación ética** es un criterio propio de este proyecto: va más allá de lo que piden la ley o los marcos, y hay que justificarlo.

## 1. Obligación legal (exigible)

| Norma | Qué exige y cómo aplica a este sistema | Dónde se atiende en el repositorio |
|---|---|---|
| **Constitución de la República Dominicana**: igualdad (art. 39), intimidad (art. 44) y hábeas data (art. 70) | No discriminar; proteger la intimidad; dar a las personas acceso a sus datos y la posibilidad de corregirlos. | Auditoría por grupo (`reports/lab12/`); mecanismo de apelación (`student_inputs/lab11_impact.yml`) |
| **Ley 172-13 de Protección Integral de los Datos Personales** | Licitud, consentimiento, finalidad y calidad del tratamiento de datos; seguridad; derechos de acceso, rectificación y supresión. | `validate_schema` rechaza identificadores directos (`name`, `document_number`, `email`, `phone`) y lo prueba `tests/test_privacy.py`; la finalidad está acotada y los usos prohibidos están en `configs/governance.yml` |

**Límites de la ley actual:**
- **No hay una ley de IA aprobada** a octubre de 2026. Hay proyectos en la Cámara de Diputados y en el Senado; uno propone crear un Centro Nacional de IA (CENIA).
- La Ley 172-13 **no regula de forma específica las decisiones automatizadas, la explicabilidad ni el perfilado**. Hay una reforma en discusión que agregaría las decisiones automatizadas.

Mientras esas normas no estén vigentes, lo que exijan **no es una obligación legal** para este proyecto. Lo trato como un riesgo regulatorio que hay que vigilar.

**Datos sintéticos:** el dataset es sintético y no contiene personas reales (`docs/DATASET_CARD.md`). La Ley 172-13 aplicaría en pleno si el sistema se usara con datos reales, y en ese caso haría falta una nueva evaluación de impacto (riesgo R09).

## 2. Marco voluntario (adoptado por decisión institucional)

| Marco | Cómo se usa |
|---|---|
| **NIST AI RMF 1.0** (DOI 10.6028/NIST.AI.100-1) | Estructura el expediente con sus cuatro funciones: GOVERN (responsables, RACI y políticas), MAP (propósito, interesados y 9 riesgos), MEASURE (auditoría del LAB12) y MANAGE (decisión LIMITAR, retiro y apelación). Resumen en `reports/lab11/rmf_summary.json`. |
| **Recomendación de la OECD sobre IA** (DOI 10.1787/cc2e1d3e-en) | Aporta los principios de equidad, transparencia, robustez y rendición de cuentas. República Dominicana no es miembro de la OECD, así que esta recomendación es una referencia y no la obliga. |
| **Fairlearn** (documentación *Performing a Fairness Assessment*) | Método técnico para medir las métricas por grupo (`MetricFrame`). Es una herramienta, no un estándar normativo. |
| **Estrategia Nacional de IA (ENIA), coordinada por OGTIC** | Política pública de orientación, no una ley. Prevé actualizar la Ley 172-13 y crear un sandbox regulatorio. |

## 3. Recomendación ética (criterio propio del proyecto)

Ni la ley ni los marcos exigen estas decisiones. Las tomé yo y tengo que poder justificarlas:

| Decisión | Por qué |
|---|---|
| Tolerancia de **0.16** en la brecha de recall y de FPR, y recall mínimo de **0.68** | Se toma de `configs/governance.yml`. Es un umbral de juicio: ninguna norma lo fija. |
| Exigir recall de al menos 0.68 **en cada grupo**, no solo en el global | El daño priorizado es el falso negativo, y el promedio ocultaba que G1 tiene 0.653. |
| **Alternativa no predictiva** como línea base obligatoria | Proporcionalidad: si el modelo no mejora la regla, se usa la regla, que es más transparente. |
| Soporte mínimo para interpretar intersecciones (**20 casos y 10 positivos**) | Evita sacar conclusiones con grupos inestables, sin ocultar esos grupos. |
| **Apelación** con respuesta humana en 5 días hábiles y un revisor independiente | Va más allá del hábeas data: permite impugnar la *prioridad*, no solo corregir datos. |
| **No aceptar el GO automático** y decidir **LIMITAR** (piloto en modo sombra) | Las puertas pasan, pero una brecha observada obliga a investigar y no prueba que el sistema sea justo. |
| Excluir `protected_group` y revisar el uso de `age_band` como variable | La ley no lo exige, pero reduce el riesgo de trato desigual y de que las variables proxy reproduzcan desigualdades. |

## Síntesis

| Nivel | Exigible | Ejemplo en este proyecto |
|---|---|---|
| Obligación legal | Sí | Sin identificadores directos; finalidad acotada; hábeas data y apelación |
| Marco voluntario | No, se adopta | Funciones del NIST AI RMF; principios de la OECD |
| Recomendación ética | No, se justifica | Umbrales de 0.16 y 0.68 por grupo; regla base; LIMITAR |

## Fuentes consultadas sobre el estado regulatorio (verificar en fuentes oficiales)

- Diego Ceredi, «¿Hay ley de IA en República Dominicana? Estado de la regulación en 2026»: https://www.diegoceredi.com/blog/regulacion-ia-republica-dominicana-2026
- Alegra, «Inteligencia artificial República Dominicana 2026: guía para empresas»: https://blog.alegra.com/republica-dominicana/inteligencia-artificial-republica-dominicana/
- Acento, «¿En qué quedó la Estrategia de Inteligencia Artificial de República Dominicana?»: https://acento.com.do/actualidad/en-que-quedo-la-estrategia-de-inteligencia-artificial-de-republica-dominicana-9533130.html
- Fuentes oficiales para confirmar: Gaceta Oficial (Ley 172-13), Congreso Nacional (Senado y Cámara de Diputados) y OGTIC (ENIA).
