# Entrega E0 · BusCol: observatorio de rutas suburbanas de Colima

Equipo: Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1) · Etiqueta: `e0` (versión Manzanillo) · Tablero: pendiente (E1)

> El proyecto cambió el 11 de noviembre de 2026 con la aprobación del profesor. Esta ficha describe la versión nueva. La etiqueta `e0` conserva lo entregado originalmente.

## Resumen en tres líneas

1. Medimos cuánto tardan las rutas que salen de la Central "Los Rojos" y qué las retrasa, para avisar al pasajero cuándo llega su camión.
2. La captura corre cada hora con GitHub Actions: GPS de 8 rutas (⚠️ **simulado** hasta que la concesionaria dé acceso al real) y paradas de camión de OpenStreetMap (161 paradas, una vez al día).
3. El sistema de calidad arranca con registros PSP individuales, una bitácora de cada corrida y 3 objetivos medibles.

## Ingeniería de Datos

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Plan de recopilación | [propuesta.md § 4](propuesta.md#4-plan-de-recopilación-de-datos) | 3 fuentes con estructura, formato, frecuencia, robots.txt y términos |
| Dos fuentes funcionando | [extractores/gps_simulado.py](../../extractores/gps_simulado.py) · [extractores/paradas.py](../../extractores/paradas.py) | El GPS es simulado y está declarado. TomTom se descartó por sus términos (ver propuesta § 4) |
| Una fuente programada | [.github/workflows/captura-bronce.yml](../../.github/workflows/captura-bronce.yml) | Cada hora, más ejecución manual |
| Serie de 36 o más periodos | [data/bronce/gps_simulado/viajes/](../../data/bronce/gps_simulado/viajes/) | Más de 100 días (desde 2026-08-01) y más de 26,000 viajes **simulados** |
| Metadatos de captura | Cada archivo de bronce | Fuente, URL y hora de captura (UTC) |

## Análisis Estadístico

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Pregunta y cliente | [propuesta.md § 1](propuesta.md#1-ficha-del-observatorio) | Cliente: concesionarias que operan en "Los Rojos" |
| Entrevista | [propuesta.md § 2](propuesta.md#2-entrevista-de-campo) | Plática con el asesor (realizada). Entrevista con el corporativo pendiente |
| Tres preguntas analíticas | [propuesta.md § 3](propuesta.md#3-las-3-preguntas-analíticas) | E1: minutos por ruta y hora · E2: hora × día × tipo de ruta · E3: rutas metropolitanas contra foráneas |

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
