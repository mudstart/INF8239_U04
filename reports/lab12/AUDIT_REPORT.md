# Informe de auditoría de equidad · LAB12

- **Sistema:** Territorial Review DSS - Synthetic
- **Fecha:** 2026-10-21
- **Decisión documentada en:** `student_inputs/lab12_decision.yml`

**Reproducir:**
```
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab12_audit.py --model tree
uv run python scripts/lab12_compare.py
```

## 1. Comprender el dataset (`scripts/describe_dataset.py`)

| Comprobación | Resultado | Lectura |
|---|---|---|
| Distribución del target | 55.2 % positivos, 44.8 % negativos | Hay poco desbalance, pero accuracy no basta: no distingue entre perder un caso de riesgo y una alerta innecesaria, y promedia los grupos. |
| Tamaño por grupo | G1 = 396 y G2 = 244 en total; en test, G1 = 101 y G2 = 59 | Las comparaciones G1/G2 tienen soporte moderado. Las intersecciones requieren cautela (ver §3). |
| Corte temporal | train hasta 2026-09-24; test desde 2026-09-25 (75/25) | Se evalúa sobre casos posteriores al entrenamiento, como en el uso real. No se usa el futuro para predecir el pasado. |
| Variables excluidas | `case_id`, `received_date`, `protected_group`, `target`. Ojo: `age_band`, declarada sensible en `configs/governance.yml`, **sí** entra al modelo | `protected_group` no entra al modelo, pero se conserva para auditar. Quitarlo no elimina el sesgo indirecto: `zone` e `infrastructure_score` pueden correlacionarse con el grupo (riesgo R06 del LAB11). Usar `age_band` como feature debe justificarse o revisarse. |

## 2. Métricas globales y por grupo (test, n = 160)

| Modelo | Accuracy | Recall | FPR | Selección | Brecha recall (IC95) | Brecha FPR | Entrenamiento | Tamaño | Latencia/caso |
|---|---|---|---|---|---|---|---|---|---|
| Regla no predictiva (LAB11) | 0.675 | **0.837** | 0.544 | 0.712 | 0.131 [0.010, 0.290] | 0.106 | — | — | ~0 ms |
| Regresión logística | **0.719** | 0.717 | **0.279** | 0.531 | 0.138 [0.009, 0.322] | 0.125 | 0.06 s | **3.6 KB** | 0.02 ms |
| Árbol (max_depth=5) | 0.706 | 0.717 | 0.309 | 0.544 | 0.181 [0.023, 0.361] | 0.168 | 0.06 s | 7.9 KB | 0.02 ms |

| Grupo | n | Recall logística | Recall árbol | Recall regla | FPR logística | FPR árbol | FPR regla |
|---|---|---|---|---|---|---|---|
| G1 | 101 | **0.653** | **0.633** | 0.898 | 0.250 | 0.269 | 0.519 |
| G2 | 59 | 0.791 | 0.814 | 0.767 | 0.375 | 0.438 | 0.625 |

El IC95 de la brecha de recall se obtuvo con bootstrap de 1000 remuestreos (semilla 42).

**Patrón: métrica global aceptable y recall bajo en un grupo.** La logística pasa las puertas automáticas (`deployment_decision` devuelve **GO**), porque esas puertas solo miran el recall *global*. Pero G1 queda en 0.653, por debajo de 0.68. El promedio oculta una falla localizada en el grupo más grande. Por eso el GO automático no se acepta sin revisión humana.

## 3. Análisis interseccional (protected_group × age_band)

**Política de soporte** (`reports/lab12/support_policy.json`): se interpreta una intersección solo si tiene **20 o más casos y 10 o más positivos**, porque el recall se calcula solo sobre los positivos.

| Intersección | n | Positivos | ¿Interpretable? | Recall logística | FPR logística |
|---|---|---|---|---|---|
| G1 · 18-29 | 18 | 4 | No | (0.75) | (0.14) |
| G1 · 30-44 | 24 | 16 | Sí | **0.563** | 0.125 |
| G1 · 45-59 | 35 | 17 | Sí | **0.588** | 0.389 |
| G1 · 60+ | 24 | 12 | Sí | 0.833 | 0.250 |
| G2 · 18-29 | 11 | 8 | No | (0.88) | (0.00) |
| G2 · 30-44 | 14 | 12 | No | (0.67) | (0.50) |
| G2 · 45-59 | 8 | 6 | No | (1.00) | (0.00) |
| G2 · 60+ | 26 | 17 | Sí | 0.765 | **0.556** |

Los valores entre paréntesis se muestran para no ocultar el grupo, pero **no se interpretan**: con 4 a 12 positivos, un solo caso mueve el recall entre 8 y 25 puntos. Lo que sí se puede leer:
- La falla de G1 se concentra en las edades de **30 a 59 años**, con recall menor a 0.60.
- **G2 · 60+** recibe más alertas innecesarias (FPR 0.556). Eso significa carga de revisión, no intervención.

## 4. Comparación de alternativas y trade-offs

- **Logística frente a árbol:** el árbol no mejora la utilidad (mismo recall global de 0.717 y accuracy menor), amplía las brechas hasta no pasar las puertas (recall 0.181, FPR 0.168) y pesa 2.2 veces más. Es el patrón «un modelo más complejo apenas mejora».
- **Logística frente a la regla no predictiva:** la regla detecta más positivos (recall 0.837, incluso 0.898 en G1), pero marca al 71 % de los casos y su FPR casi duplica el de la logística. Con capacidad de revisión limitada, «priorizar» al 71 % ya no ordena la cola. Es un **compromiso, no una victoria automática**: la regla protege mejor contra el daño priorizado (falso negativo) en G1, mientras que la logística usa mejor la capacidad.

## 5. Green AI

Los dos modelos entrenan en 0.06 s, ocupan menos de 8 KB y predicen en 0.02 ms por caso: el costo computacional es despreciable frente a los límites (500 ms y 1024 KB). Aun así, se prefiere la **opción suficiente**: la logística da la misma utilidad que el árbol con la mitad del tamaño, y es más interpretable para la revisión humana y la apelación. Un modelo más complejo no está justificado.

## 6. Por qué una brecha no prueba discriminación causal

La brecha de recall de 0.138 entre G1 y G2 es una **señal que obliga a investigar, no una prueba de discriminación**:
1. **Es incierta:** el IC95 va de 0.009 a 0.322, así que no sabemos si la brecha real es casi nula o el doble de la tolerancia.
2. **Puede venir de otras causas:** la distribución de zonas, edades o incidentes previos puede ser distinta entre los grupos, o el target puede medir el riesgo con distinta calidad en cada grupo.
3. **Una métrica de equidad no define la justicia:** el modelo no usa `protected_group`. Para afirmar una relación causal se necesitaría un análisis de proxies, conocer el proceso que generó los datos y validarlo con expertos y con las comunidades afectadas.

## 7. Decisión contextual

**LIMITAR.** No se despliega el árbol. La regresión logística solo pasa a un **piloto en modo sombra**: la regla no predictiva sigue ordenando la cola, el modelo se registra en paralelo y un analista revisa cada caso.

- **Condición para GO:** el recall de G1 llega a 0.68 o más, con más datos o con un ajuste de umbral validado por grupo, sin que la brecha de FPR pase de 0.16, y el IC95 de la brecha de recall ya no supera la tolerancia.
- **Acción humana:** monitoreo mensual del recall de G1 · 30-44 y G1 · 45-59; revisión del FPR de G2 · 60+; las apelaciones aceptadas se suman a la auditoría.
- **Responsable:** Product Owner, con el apoyo del Data Scientist.
- **Retiro:** se aplican las condiciones de `student_inputs/lab11_impact.yml`.

## Fuentes

- Fairlearn Contributors. *Performing a Fairness Assessment*, documentación oficial de Fairlearn.
- NIST. *AI RMF 1.0*, funciones MEASURE y MANAGE. DOI: 10.6028/NIST.AI.100-1.
