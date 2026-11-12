# Objetivos de calidad (PSP) — E0

Tipos de defecto (los diez de PSP): documentación, sintaxis, construcción, asignación, interfaz, verificación, datos, función, sistema y entorno.
Fases: planeacion, diseno, codigo, revision, pruebas, postmortem.

| # | Objetivo | Métrica | Meta | Cómo se mide |
|---|---|---|---|---|
| 1 | **Disponibilidad de la captura** | % de corridas con estado `ok` por fuente | ≥ 95 % por entrega | `data/bronce/bitacora.csv` + historial de GitHub Actions |
| 2 | **Datos completos** | % de horas con pings de GPS y de días con archivo de viajes | 100 % de los días desde 2026-08-01 y ≥ 95 % de las horas | `data/bronce/gps_simulado/` contra el calendario |
| 3 | **Pocos defectos que lleguen a prueba** | Defectos encontrados en fase Prueba ÷ total de defectos registrados | ≤ 30 % (la mayoría debe salir en Revisión) | `calidad/defectos-*.csv` |

Registro: cada integrante anota su tiempo en `calidad/tiempo-<nombre>.csv` (minutos, por fase) y sus defectos en `calidad/defectos-<nombre>.csv` al momento de encontrarlos.
