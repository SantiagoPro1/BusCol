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
python3 extractores/gps_simulado.py --test   # autoprueba del simulador
python3 extractores/gps_simulado.py          # viajes desde 2026-08-01 y pings de la última hora
python3 extractores/paradas.py               # paradas OSM (una vez al día)
```

Solo usa la biblioteca estándar de Python 3.11 o superior. En GitHub corre solo cada hora (**Actions → Captura Bronce**) y cada corrida queda en `data/bronce/bitacora.csv`.

## Estructura

| Ruta | Contenido |
|---|---|
| `docs/E0/` | Propuesta y ficha de entrega |
| `extractores/` | Un módulo por fuente, más `bitacora.py` |
| `data/bronce/` | Datos crudos por fuente y la bitácora |
| `calidad/` | Registros PSP por integrante y objetivos de calidad |
| `.github/workflows/` | Captura programada |

Paradas y ubicaciones: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) (ODbL). Trazos de ruta: OSRM sobre OpenStreetMap.
