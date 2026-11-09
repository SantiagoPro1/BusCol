# Observatorio del Comercio por el Puerto de Manzanillo

Proyecto integrador **Trusted Data Lab**: pronóstico y análisis del movimiento mensual de contenedores (TEU) en Manzanillo, Colima, comparado con otros puertos de México.

**Equipo:** Joel Emiliano Salazar Figueroa · Santiago García García

## Qué observa

- **TEU por puerto** (mensual), del *Informe Estadístico Mensual de los Puertos de México* (CGPMM, gob.mx)
- **Tipo de cambio USD/MXN** (diario), de la API Frankfurter (tasas del Banco Central Europeo)

## Cómo se ejecuta

```bash
sudo apt-get install -y poppler-utils        # pdftotext
python3 extractores/puertos.py --test         # autoprueba del parser
python3 extractores/tipo_cambio.py            # tipo de cambio: solo fechas nuevas
python3 extractores/puertos.py                # informes de puertos: solo PDF nuevos
```

Solo usa la biblioteca estándar de Python 3.11 o superior. En GitHub corre solo todos los días (**Actions → Captura Bronce**) y cada corrida queda anotada en `data/bronce/bitacora.csv`.

## Estructura

| Ruta | Contenido |
|---|---|
| `docs/E0/` | Propuesta (`propuesta.md`) y ficha de entrega (`ENTREGA.md`) |
| `extractores/` | Un módulo por fuente, más `bitacora.py` |
| `data/bronce/` | Datos crudos por fuente y la bitácora de ejecuciones |
| `calidad/` | Registros PSP de tiempo y defectos por integrante y objetivos de calidad |
| `.github/workflows/` | Captura programada |

**Tablero:** pendiente (E1).

Fuentes citadas: CGPMM, gob.mx (uso académico; URL y fecha de cada consulta en `data/bronce/puertos/manifiesto.csv`) · Banco Central Europeo, vía frankfurter.dev.
