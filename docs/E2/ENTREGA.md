# Entrega E2 · BusCol: observatorio de rutas suburbanas de Colima

**Unidad:** Unidad 4 — Integración Avanzada, Trazabilidad y Ética (Ponderación: 20%)  
**Equipo:** Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1)  
**Etiqueta de Git:** `e2`  
**Repositorio:** [https://github.com/SantiagoPro1/BusCol](https://github.com/SantiagoPro1/BusCol)  
**Fecha de Entrega:** 23 de noviembre de 2026  

---

## Resumen en tres líneas

1. Integramos la fuente especializada **Geoespacial** combinando las 161 paradas de OpenStreetMap (Overpass API) y los trazos vectoriales de las 8 rutas suburbanas de Colima mediante **GeoPandas** y **Shapely**, publicando un mapa interactivo con **Folium** ([mapa_observatorio_colima.html](mapa_observatorio_colima.html)).
2. Formalizamos la **Declaración de Ética y Legalidad** ([docs/etica-datos.md](../etica-datos.md)) analizando términos de uso (ODbL 1.0), auditoría de `robots.txt`, justificación del retiro de TomTom, mitigación de sesgos de voluntariado y garantía estricta de Cero Datos Personales (Cero PII).
3. Implementamos **linaje y trazabilidad criptográfica completa**: el 100% de los registros en la **Capa Oro** contienen metadatos obligatorios (`lineage_archivo_bronce_paradas`, `lineage_fecha_ingesta_bronce_utc`, `lineage_hash_sha256`) auditados mediante pruebas automáticas con `pytest` ([tests/test_trazabilidad.py](../../tests/test_trazabilidad.py)).

---

## Matriz de Cumplimiento de la Rúbrica E2

| Criterio de la Rúbrica | Entregable / Evidencia | Ubicación en el Repositorio | Nota Técnica del Equipo |
|---|---|---|---|
| **1. Fuente Especializada Integrada (Geoespacial)** | Ingesta y modelado vectorial con GeoPandas | [extractores/geo_procesamiento.py](../../extractores/geo_procesamiento.py) | Modela paradas (`Point`) y rutas (`LineString`) en EPSG:4326 y proyecta a EPSG:6369 (UTM 13N México) para calcular buffers de 300 m y densidad de paradas por kilómetro. |
| **Visualización Cartográfica** | Mapa web interactivo con Folium | [docs/E2/mapa_observatorio_colima.html](mapa_observatorio_colima.html) | Muestra la Central "Los Rojos", las 4 rutas metropolitanas, las 4 rutas foráneas, clusters de paradas y popups con datos de trazabilidad. |
| **2. Declaración de Ética y Legalidad** | Documento normativo integral | [docs/etica-datos.md](../etica-datos.md) | Términos de OpenStreetMap y OSRM, auditoría de `robots.txt`, explicación del descarte de TomTom (cláusulas 11.4 y 11.6.1), mitigación de sesgos VGI y protección Cero PII. |
| **3. Linaje y Trazabilidad de Datos** | Registros Oro rastreables a Bronce con fecha de ingesta | [data/oro/cobertura_rutas_paradas.parquet](../../data/oro/cobertura_rutas_paradas.parquet) · [tests/test_trazabilidad.py](../../tests/test_trazabilidad.py) | Cada registro en Oro cuenta con origen en Bronce, timestamp UTC de ingesta y firma SHA-256. Validado con 5 pruebas unitarias automatizadas (`100% passed`). |
| **4. Ficha de Entrega y Relatoría** | Documentación de etapa | [docs/E2/ENTREGA.md](ENTREGA.md) · [docs/relatoria-E2.md](../relatoria-E2.md) | Ficha oficial de entrega con instrucciones de reproducción y relatoría técnica de la etapa. |
| **5. Etiqueta en Git** | Tag oficial de entrega | Tag `e2` en repositorio remoto | Generado y firmado para congelar el estado del código para evaluación. |

---

## Arquitectura de Datos por Capas (Medallón)

```
[ Capa Bronce: Raw & Inmutable ]
├── data/bronce/paradas/2026-11-12.json          (161 nodos OSM crudos con metadata de ingesta)
├── data/bronce/gps_simulado/viajes/*.csv        (103 archivos diarios, >26,000 viajes simulados)
└── data/referencia/trazos_osrm.json             (Geometrías viales base de las 8 rutas)
                     │
                     ▼  extractores/geo_procesamiento.py (GeoPandas + Shapely)
[ Capa Plata: Depurada y Normalizada ]
├── data/plata/paradas_colima.parquet            (GeoDataFrame EPSG:4326 con atributos limpios)
└── data/plata/rutas_trazos.parquet              (LineStrings georreferenciados)
                     │
                     ▼  Análisis Espacial (Buffer 300m, Intersecciones, Cruces y Linaje SHA-256)
[ Capa Oro: Analítica y Trazable ]
├── data/oro/cobertura_rutas_paradas.parquet     (8 rutas con densidad de paradas y linaje a Bronce)
├── data/oro/factores_retraso_oro.parquet        (32 combinaciones factoriales de retraso)
└── docs/E2/mapa_observatorio_colima.html        (Visualización cartográfica interactiva con Folium)
```

---

## Guía de Reproducción y Evaluación Rápida

Para verificar y replicar los resultados de la Entrega E2 de forma limpia en cualquier máquina:

```bash
# 1. Clonar el repositorio y posicionarse en la etiqueta e2
git clone https://github.com/SantiagoPro1/BusCol.git
cd BusCol
git checkout e2

# 2. Instalar dependencias geoespaciales
pip install geopandas shapely folium pandas pyarrow pytest

# 3. Ejecutar el pipeline de procesamiento geoespacial (Plata y Oro)
python3 extractores/geo_procesamiento.py

# 4. Generar el mapa cartográfico interactivo
python3 extractores/mapa_observatorio.py

# 5. Ejecutar la suite automatizada de pruebas de linaje
python3 -m pytest tests/test_trazabilidad.py -v
```

---

## Evidencia de Pruebas Unitarias de Trazabilidad

Ejecución de `pytest tests/test_trazabilidad.py -v`:
```text
tests/test_trazabilidad.py::test_existencia_archivos_capa_oro PASSED     [ 20%]
tests/test_trazabilidad.py::test_columnas_obligatorias_linaje PASSED     [ 40%]
tests/test_trazabilidad.py::test_trazabilidad_paradas_oro_hacia_bronce PASSED [ 60%]
tests/test_trazabilidad.py::test_trazabilidad_viajes_factores_hacia_bronce PASSED [ 80%]
tests/test_trazabilidad.py::test_firmas_criptograficas_sha256 PASSED     [100%]
============================== 5 passed in 0.27s ===============================
```
