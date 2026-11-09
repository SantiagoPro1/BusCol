# Objetivos de calidad (PSP) — E0

Tipos de defecto (estándar PSP): 10 Documentación · 20 Sintaxis · 40 Asignación · 50 Interfaz · 60 Verificación · 70 Datos · 80 Función · 90 Sistema.
Fases: Planeación · Diseño · Código · Revisión · Prueba · Postmortem.

| # | Objetivo | Métrica | Meta | Cómo se mide |
|---|---|---|---|---|
| 1 | **Captura confiable** | % de ejecuciones del workflow *Captura Bronce* que terminan en verde | ≥ 95 % por entrega | Historial de GitHub Actions |
| 2 | **Datos completos** | % de meses esperados (2021-01 a último informe publicado) presentes en `data/bronce/teus/` | 100 %, sin huecos | Conteo de archivos `AAAA-MM.csv` contra el calendario |
| 3 | **Pocos defectos que lleguen a prueba** | Defectos encontrados en fase Prueba ÷ total de defectos registrados | ≤ 30 % (la mayoría debe salir en Revisión) | `calidad/defectos-*.csv` |

Registro: cada integrante anota su tiempo en `calidad/tiempo-<nombre>.csv` (minutos, por fase) y sus defectos en `calidad/defectos-<nombre>.csv` al momento de encontrarlos.
