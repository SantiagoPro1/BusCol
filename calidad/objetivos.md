# Objetivos de calidad (PSP) — E0

Tipos de defecto (los diez de PSP): documentación, sintaxis, construcción, asignación, interfaz, verificación, datos, función, sistema y entorno.
Fases: planeacion, diseno, codigo, revision, pruebas, postmortem.

| # | Objetivo | Métrica | Meta | Cómo se mide |
|---|---|---|---|---|
| 1 | **Disponibilidad de la captura** | % de corridas con estado `ok` por fuente | ≥ 95 % por entrega | `data/bronce/bitacora.csv` + historial de GitHub Actions |
| 2 | **Datos completos** | % de horas esperadas con medición de las 8 rutas y con clima | ≥ 95 % de las horas desde que arranca la captura | `data/bronce/rutas/*.jsonl` y `data/bronce/clima/` contra el calendario horario |
| 3 | **Pocos defectos que lleguen a prueba** | Defectos encontrados en fase Prueba ÷ total de defectos registrados | ≤ 30 % (la mayoría debe salir en Revisión) | `calidad/defectos-*.csv` |

Registro: cada integrante anota su tiempo en `calidad/tiempo-<nombre>.csv` (minutos, por fase) y sus defectos en `calidad/defectos-<nombre>.csv` al momento de encontrarlos.
