# BusCol

Observatorio de rutas suburbanas de Colima

Proyecto integrador **Trusted Data Lab**: tiempos de recorrido y retrasos de las rutas de autobús que salen de la Central "Los Rojos" (Colima), con el objetivo de avisar al pasajero cuándo llega su camión.

**Equipo:** Joel Emiliano Salazar Figueroa · Santiago García García

> La versión anterior del proyecto (Puerto de Manzanillo) está en la etiqueta `e0`.

## Qué observa

- **Tiempo de recorrido con tráfico** de "Los Rojos" a 8 destinos, cada hora (TomTom Routing API)
- **Paradas de camión** de Colima, una vez al día (OpenStreetMap vía Overpass)
- **GPS de las unidades** cuando la concesionaria dé acceso

## Cómo se ejecuta

```bash
python3 extractores/rutas.py --test          # autoprueba
TOMTOM_KEY=... python3 extractores/rutas.py  # tiempos de las 8 rutas en este momento
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

Paradas y ubicaciones: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) (ODbL). Tiempos de recorrido: TomTom.
