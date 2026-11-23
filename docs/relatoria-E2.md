# Relatoría de Etapa — Entrega E2
**Proyecto:** BusCol: observatorio de rutas suburbanas de Colima  
**Unidad:** Unidad 4 — Integración Avanzada, Trazabilidad y Ética  
**Equipo:** Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1)  
**Fecha:** 23 de noviembre de 2026  

---

## 1. Contexto y Objetivos de la Etapa

En esta segunda etapa del observatorio BusCol, el objetivo primordial fue evolucionar el repositorio desde la ingesta inicial en Capa Bronce hacia una arquitectura de datos avanzada y auditable. Esto requirió:
1. Integrar una fuente de datos especializada de naturaleza geoespacial mediante **GeoPandas**.
2. Garantizar una cadena de custodia y linaje ininterrumpido desde el dato crudo en Bronce hasta las tablas analíticas en Capa Oro.
3. Formalizar una declaración de ética, legalidad y gobernanza de datos que blindara al proyecto ante cualquier contingencia regulatoria o de uso indebido.

---

## 2. Desafíos Técnicos Enfrentados y Soluciones Implementadas

### 2.1 El Problema de las Proyecciones Cartográficas en Cálculos de Buffer
* **El Reto:** Las coordenadas de OpenStreetMap y OSRM se entregan en el sistema de coordenadas geográficas estándar **WGS84 (EPSG:4326)**, cuyas unidades son grados decimales. Si se intenta calcular un búfer de proximidad directamente en grados, la distorsión geográfica produce radios elípticos erróneos y no escalables en metros.
* **La Solución:** Mediante **GeoPandas**, implementamos una transformación de proyección al vuelo hacia el sistema proyectado oficial de México: **ITRF2008 / UTM Zona 13N (EPSG:6369)**. Con esto, pudimos trazar con exactitud geodésica corredores de amortiguamiento de 300 metros alrededor de las 8 rutas de camión y determinar con precisión métrica qué paradas de autobús pertenecen a cada corredor de transporte.

### 2.2 Pérdida de Linaje en Agregaciones Espaciales
* **El Reto:** Cuando se aplican operaciones de cruce espacial (`spatial join` o intersección de polígonos) y agrupamiento (`groupby`), las librerías tradicionales de datos tienden a descartar las marcas de tiempo y los identificadores de archivo originales de la Capa Bronce, produciendo métricas desvinculadas de su fuente.
* **La Solución:** Diseñamos un esquema de preservación de linaje en el script `extractores/geo_procesamiento.py`. Cada fila de la Capa Oro conserva:
  - La ruta relativa exacta del archivo JSON de Bronce donde se descargó la información.
  - La marca de tiempo UTC en que se ejecutó la petición a la API.
  - Una muestra explícita de los IDs de los nodos originales de OSM.
  - Una firma criptográfica **SHA-256** (`lineage_hash_sha256`) calculada a partir de los datos crudos y la fecha de transformación, lo que permite auditar si una métrica ha sufrido alteraciones no autorizadas.

### 2.3 Visualización Accesible sin Dependencia de Servidores GIS Pesados
* **El Reto:** La visualización cartográfica no debía depender de software de escritorio como QGIS o ArcGIS, pues el evaluador o usuario debe poder explorar los resultados en cualquier navegador sin configuraciones complejas.
* **La Solución:** Desarrollamos un generador con **Folium** (`extractores/mapa_observatorio.py`) que compila en un archivo autónomo HTML (`docs/E2/mapa_observatorio_colima.html`) con control de capas, clustering interactivo de paradas y cuadros emergentes (*popups*) que muestran no solo las características operativas de la parada sino también sus metadatos de linaje Bronce.

---

## 3. Decisiones de Arquitectura y Diseño

1. **Adopción del Formato Apache Parquet:**  
   Para la Capa Plata y Oro se optó por guardar tanto en Parquet como en CSV. Parquet garantiza la preservación estricta de los tipos de datos geométricos y optimiza los tiempos de lectura para análisis posteriores.
2. **Separación de la Pregunta Analítica E2:**  
   En la Capa Oro se construyeron dos productos analíticos:
   - `cobertura_rutas_paradas.parquet`: que resuelve la dimensión espacial y la densidad de paradas por kilómetro.
   - `factores_retraso_oro.parquet`: que aborda la pregunta analítica E2 sobre el impacto del Factor A (hora pico vs valle), Factor B (fin de semana vs entre semana) y Factor C (ruta metropolitana vs foránea) sobre los minutos de retraso.

---

## 4. Reflexión Ética y Lecciones Aprendidas

1. **La Ética del Descarte:**  
   Una de las lecciones más valiosas de este proyecto fue aprender a descartar fuentes atractivas cuando violan principios éticos o legales. El retiro de TomTom Routing API demostró que la facilidad técnica nunca debe estar por encima del respeto a los términos de servicio (cláusulas 11.4 y 11.6.1).
2. **Consciencia de los Sesgos en Datos Colaborativos:**  
   Al auditar los datos de OpenStreetMap, comprendimos que los datos comunitarios (VGI) reflejan la geografía socioeconómica de sus colaboradores: los centros urbanos de Colima y Comala presentan una alta densidad de paradas registradas, mientras que municipios como Minatitlán o Ixtlahuacán aparecen con escaso reporte. Reconocer este sesgo en `docs/etica-datos.md` evitó que el observatorio emitiera juicios erróneos sobre la calidad del servicio en zonas periféricas.
3. **Cero Datos Personales como Principio Innegociable:**  
   Diseñar el observatorio desde la perspectiva de *Privacy by Design* nos permitió enfocarnos en la infraestructura y los vehículos, disociando cualquier identificador que pudiera comprometer la privacidad de usuarios o choferes.

---

## 5. Conclusiones y Próximos Pasos (Hacia E3)

La Entrega E2 concluye exitosamente con un pipeline robusto, probado mediante tests automatizados con `pytest` y soportado por una sólida base ética. 

Para la **Entrega E3**, el observatorio BusCol abordará:
- Modelado estadístico multivariado (MANOVA y análisis de conglomerados) para clasificar perfiles de ruta.
- Integración de métricas de puntualidad basadas en la comparación entre el tiempo de recorrido base y la densidad de paradas por kilómetro calculada en esta etapa.
