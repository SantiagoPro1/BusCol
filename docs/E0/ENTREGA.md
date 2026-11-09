# Entrega E0 · Observatorio del Comercio por el Puerto de Manzanillo

Equipo: Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1) · Etiqueta: `e0` · Tablero: pendiente (E1)

Repositorio: https://github.com/SantiagoPro1/ManzanilloAduanas

## Resumen en tres líneas

1. Observamos el movimiento de contenedores (TEU) del Puerto de Manzanillo para pronosticarlo y explicar sus subidas y caídas.
2. Hay dos fuentes capturando solas cada día con GitHub Actions: los informes oficiales de la CGPMM (48 meses de TEU por puerto) y el tipo de cambio USD/MXN (más de 1,500 días desde 2021).
3. El sistema de calidad arranca con registros PSP individuales, una bitácora de cada corrida de la captura y 3 objetivos medibles.

## Ingeniería de Datos

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Plan de recopilación | [propuesta.md § 4](propuesta.md#4-plan-de-recopilación-de-datos) | Cada fuente con estructura, formato, frecuencia, método, robots.txt y términos de uso |
| Dos fuentes funcionando | [extractores/puertos.py](../../extractores/puertos.py) · [extractores/tipo_cambio.py](../../extractores/tipo_cambio.py) | Extractores éticos: User-Agent identificado, pausas, sin redescargas |
| Una fuente programada | [.github/workflows/captura-bronce.yml](../../.github/workflows/captura-bronce.yml) · [Actions](https://github.com/SantiagoPro1/ManzanilloAduanas/actions) | Diario a las 07:00 de Colima, más ejecución manual |
| Serie de 36 o más periodos en bronce | [data/bronce/puertos/teus/](../../data/bronce/puertos/teus/) | 48 meses (2022-01 a 2025-12). La columna del año anterior cubre 2021 |
| Metadatos de captura | [manifiesto.csv](../../data/bronce/puertos/manifiesto.csv) · [data/bronce/tipo_cambio/](../../data/bronce/tipo_cambio/) | URL, fecha de captura y sha256 de cada PDF. El JSON trae fuente, URL y hora de captura |

## Análisis Estadístico

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Pregunta y cliente | [propuesta.md § 1](propuesta.md#1-ficha-del-observatorio) | Cliente: agencias aduanales, transportistas y patios de Manzanillo |
| Entrevista | [propuesta.md § 2](propuesta.md#2-entrevista-de-campo) | ⚠️ Simulada y declarada como tal. La entrevista con un actor real está pendiente |
| Tres preguntas analíticas | [propuesta.md § 3](propuesta.md#3-las-3-preguntas-analíticas) | E1: TEU mensual de Manzanillo · E2: temporada × tipo de cambio × tipo de tráfico · E3: Manzanillo y Lázaro Cárdenas contra Veracruz y Altamira |

## Calidad en los Sistemas de Información

| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Registros individuales | [calidad/](../../calidad/) | `tiempo-*.csv` y `defectos-*.csv` por integrante, con el formato del Kit |
| Bitácora de ejecuciones | [data/bronce/bitacora.csv](../../data/bronce/bitacora.csv) | Una fila por corrida y fuente: estado, registros nuevos, duración y error |
| Tres objetivos medibles | [calidad/objetivos.md](../../calidad/objetivos.md) | Disponibilidad ≥ 95 %, serie sin huecos, ≤ 30 % de defectos encontrados en pruebas |

## Relatoría de etapa

No aplica en E0. Empieza en E1 (`docs/relatoria-E1.md`).

## Issues de la entrega anterior

No aplica: es la primera entrega.
