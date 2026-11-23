# BusCol

Observatorio de rutas suburbanas de Colima

Proyecto integrador **Trusted Data Lab**: tiempos de recorrido y retrasos de las rutas de autobús que salen de la Central "Los Rojos" (Colima), con el objetivo de avisar al pasajero cuándo llega su camión.

**Equipo:** Joel Emiliano Salazar Figueroa · Santiago García García

> La versión anterior del proyecto (Puerto de Manzanillo) está en la etiqueta `e0`.

## Qué observa

- **GPS de los camiones** de 8 rutas desde "Los Rojos": ⚠️ **simulado** hasta que la concesionaria dé acceso al real (cada fila lleva `simulado=1`)
- **Paradas de camión** de Colima, una vez al día (OpenStreetMap vía Overpass)

## Cómo se ejecuta

```bash
# Ingesta Bronce (base)
python3 extractores/gps_simulado.py          # viajes desde 2026-08-01 y pings de la última hora
python3 extractores/paradas.py               # paradas OSM (una vez al día)

# Entrega E2: Procesamiento geoespacial avanzado, capas Plata/Oro y mapa
python3 extractores/geo_procesamiento.py     # pipeline geoespacial (Plata y Oro) con linaje
python3 extractores/mapa_observatorio.py      # mapa interactivo Folium en docs/E2/mapa_observatorio_colima.html
python3 -m pytest tests/test_trazabilidad.py # auditoría automatizada de trazabilidad
```

## Estructura

| Ruta | Contenido |
|---|---|
| `docs/E0/` | Propuesta y ficha de entrega E0 |
| `docs/E2/` | Ficha de entrega E2 y mapa interactivo cartográfico |
| `docs/etica-datos.md` | Declaración de ética, legalidad, robots.txt y licencias |
| `docs/relatoria-E2.md` | Memoria técnica y relatoría de la etapa E2 |
| `extractores/` | Ingesta, pipeline geoespacial avanzado (`geo_procesamiento.py`) y mapa (`mapa_observatorio.py`) |
| `data/bronce/` | Datos crudos por fuente (OSM, GPS simulado) y la bitácora |
| `data/plata/` | Capa Plata: paradas y rutas georreferenciadas con GeoPandas |
| `data/oro/` | Capa Oro: métricas analíticas de cobertura y factores con trazabilidad estricta |
| `tests/` | Pruebas de linaje y validación de procedencia Bronce-Oro |
| `calidad/` | Registros PSP por integrante y objetivos de calidad |
| `.github/workflows/` | Captura programada |

Paradas y ubicaciones: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) (ODbL). Trazos de ruta: OSRM sobre OpenStreetMap.
