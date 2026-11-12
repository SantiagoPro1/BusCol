# Entrega E0 · Observatorio de Rutas Suburbanas de Colima _(nombre provisional)_

Equipo: Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1) · Etiqueta: `e0` (versión Manzanillo) · Tablero: pendiente (E1)

> El proyecto cambió el 11 de noviembre de 2026 con la aprobación del profesor. Esta ficha describe la versión nueva. La etiqueta `e0` conserva lo entregado originalmente.

## Resumen en tres líneas

1. Medimos cuánto tardan las rutas que salen de la Central "Los Rojos" y qué las retrasa, para avisar al pasajero cuándo llega su camión.
2. La captura corre cada hora con GitHub Actions: clima desde 2022 (42,600 horas) y tiempos de recorrido con tráfico de 8 rutas (en cuanto se configure la clave de TomTom).
3. El sistema de calidad arranca con registros PSP individuales, una bitácora de cada corrida y 3 objetivos medibles.

## Ingeniería de Datos

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Plan de recopilación | [propuesta.md § 4](propuesta.md#4-plan-de-recopilación-de-datos) | 3 fuentes con estructura, formato, frecuencia, robots.txt y términos |
| Dos fuentes funcionando | [extractores/clima.py](../../extractores/clima.py) · [extractores/rutas.py](../../extractores/rutas.py) | Rutas: pendiente del *secret* `TOMTOM_KEY` y de verificar los términos de TomTom |
| Una fuente programada | [.github/workflows/captura-bronce.yml](../../.github/workflows/captura-bronce.yml) | Cada hora, más ejecución manual |
| Serie de 36 o más periodos | [data/bronce/clima/](../../data/bronce/clima/) | 42,600 horas sin huecos desde 2022-01-01 |
| Metadatos de captura | Cada archivo de bronce | Fuente, URL y hora de captura (UTC) |

## Análisis Estadístico

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Pregunta y cliente | [propuesta.md § 1](propuesta.md#1-ficha-del-observatorio) | Cliente: concesionarias que operan en "Los Rojos" |
| Entrevista | [propuesta.md § 2](propuesta.md#2-entrevista-de-campo) | Plática con el asesor (realizada). Entrevista con el corporativo pendiente |
| Tres preguntas analíticas | [propuesta.md § 3](propuesta.md#3-las-3-preguntas-analíticas) | E1: minutos por ruta y hora · E2: hora × día × lluvia · E3: rutas metropolitanas contra foráneas |

## Calidad en los Sistemas de Información

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Registros individuales | [calidad/](../../calidad/) | `tiempo-*.csv` y `defectos-*.csv` por integrante |
| Bitácora de ejecuciones | [data/bronce/bitacora.csv](../../data/bronce/bitacora.csv) | Una fila por corrida y fuente |
| Tres objetivos medibles | [calidad/objetivos.md](../../calidad/objetivos.md) | Disponibilidad ≥ 95 %, horas completas ≥ 95 %, ≤ 30 % de defectos en pruebas |

## Relatoría de etapa

No aplica en E0.

## Issues de la entrega anterior

No aplica: es la primera entrega.
