# Declaración de Ética, Legalidad y Gobernanza de Datos
**Proyecto:** BusCol — Observatorio de rutas suburbanas de Colima  
**Entregable:** E2 (Unidad 4)  
**Equipo:** Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1)  
**Repositorio:** [https://github.com/SantiagoPro1/BusCol](https://github.com/SantiagoPro1/BusCol)  
**Fecha:** Noviembre 2026  

---

## 1. Marco Legal y Términos de Uso de las Fuentes

El observatorio **BusCol** integra fuentes de datos bajo un marco de estricto apego a las leyes aplicables en los Estados Unidos Mexicanos (Ley Federal del Derecho de Autor y Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados - LGPDPPSO) y a los términos de servicio de los proveedores tecnológicos.

### 1.1 Fuente Primaria Especializada: OpenStreetMap (OSM) vía Overpass API
* **Licencia de Origen:** Open Database License (**ODbL 1.0**) de Open Data Commons.
* **Términos de Servicio y Política de Uso de Overpass:**
  - La Overpass API (`https://overpass-api.de/api/interpreter`) establece límites comunitarios de cortesía: máximo 10,000 consultas diarias o 1 GB de transferencia para evitar saturación de los servidores gestionados por la Fundación OpenStreetMap.
  - **Frecuencia en BusCol:** Se realiza **una única consulta al día** (gestionada por el script `extractores/paradas.py`), validando previamente si el archivo diario ya existe en `data/bronce/paradas/AAAA-MM-DD.json`.
  - **Identificación:** Se incluye en las cabeceras HTTP un `User-Agent` explícito con contacto y propósito:  
    `User-Agent: BusCol/1.0 (proyecto escolar; github.com/SantiagoPro1/BusCol)`.
* **Atribución Legal:** Todo mapa y producto derivado generado en BusCol incluye la leyenda legal obligatoria:  
  *“© OpenStreetMap contributors (ODbL)”*.

### 1.2 Geometrías de Calles y Trazos: OSRM (Open Source Routing Machine)
* **Propósito:** Mapeo de la red vial de las 8 rutas que salen de la Central "Los Rojos".
* **Términos:** Se utilizó la API de demostración de OSRM únicamente para la descarga inicial de las coordenadas vectoriales (`data/referencia/trazos_osrm.json`). El archivo se almacena estáticamente para no generar peticiones recurrentes a la infraestructura pública de OSRM.

### 1.3 Telemetría de Camiones: GPS Simulado (Transparencia Radical)
* **Estatus Actual:** La concesionaria de transporte que opera en la Central "Los Rojos" (ej. Autobuses Nuevo Horizonte) aún no ha formalizado el convenio de acceso a la API del GPS instalado en las unidades.
* **Salvaguarda Ética:** Para no incurrir en espionaje industrial ni en recolección clandestina, BusCol optó por un generador estocástico determinista basado en los horarios oficiales de la central y las distancias viales reales.
* **Marcado Obligatorio:** Cada registro lleva de manera indeleble `simulado=1` y las unidades se denominan `SIM-xxx`. Se prohíbe presentar estas métricas como verdades absolutas del tráfico de Colima hasta contar con el acceso contractual formal.

### 1.4 Fuente Descartada por Razones Legales: TomTom Routing API
* Durante la fase preliminar (E0), se evaluó consumir los tiempos de recorrido de TomTom.
* **Decisión de Retiro:** Tras auditar los Términos y Condiciones de TomTom ([https://docs.tomtom.com/legal/terms-and-conditions](https://docs.tomtom.com/legal/terms-and-conditions)), el equipo identificó dos cláusulas prohibitivas:
  - **Cláusula 11.4:** Prohíbe expresamente almacenar o cachear de forma persistente los resultados de rutas y tiempos.
  - **Cláusula 11.6.1:** Prohíbe crear bases de datos derivadas basadas en la información provista por TomTom.
  - **Cláusula 2.2:** Restringe el uso de las claves no comerciales exclusivamente a pruebas internas sin publicación abierta.
* **Acción Correctiva:** El 12 de noviembre de 2026 se eliminaron todos los extractores y archivos asociados a TomTom, preservando la legitimidad ética del observatorio.

---

## 2. Análisis de Directivas de Acceso y `robots.txt`

En proyectos de ciencia e ingeniería de datos, el respeto a las directivas de los servidores es un pilar fundamental de la ética digital.

### 2.1 Inspección de `https://www.openstreetmap.org/robots.txt`
El archivo de directivas de OSM estipula:
```text
User-agent: *
Disallow: /api/0.6/map?
Disallow: /trace/
Disallow: /traces/
...
```
* **Diagnóstico:** El portal web restringe el rastreo agresivo sobre el visualizador web y la API de edición directa (`/api/0.6/map`) para proteger la experiencia del usuario interactivo.
* **Cumplimiento en BusCol:** BusCol **no realiza web scraping** sobre el sitio web principal ni sobre los tiles gráficos de OpenStreetMap. En su lugar, utiliza el endpoint expresamente diseñado para analítica masiva y consultas semánticas: **Overpass API**.

### 2.2 Inspección de `https://overpass-api.de/robots.txt`
```text
User-agent: *
Disallow: /api/
```
* **Diagnóstico:** La directiva `Disallow: /api/` está orientada a motores de indexación generalistas (Googlebot, Bingbot) para evitar que los robots sigan hipervínculos dinámicos e indexen miles de combinaciones de coordenadas.
* **Política de Uso Aceptable de Overpass:** La documentación oficial de Overpass ([https://wiki.openstreetmap.org/wiki/Overpass_API/Acceptable_Use_Policy](https://wiki.openstreetmap.org/wiki/Overpass_API/Acceptable_Use_Policy)) especifica que el endpoint `/api/interpreter` está abierto al consumo por scripts y clientes de datos siempre que:
  1. No excedan 10,000 peticiones diarias.
  2. Implementen backoff exponencial en respuestas HTTP 429 (Too Many Requests).
  3. No ejecuten peticiones concurrentes en paralelo.
* **Alineación:** BusCol cumple holgadamente con estas reglas al realizar **1 sola consulta cada 24 horas**.

---

## 3. Mitigación de Sesgos

Los observatorios de datos pueden amplificar desigualdades estructurales si no reconocen las limitaciones de sus datos. En BusCol identificamos tres sesgos principales y sus mecanismos de mitigación:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MATRIZ DE MITIGACIÓN DE SESGOS                     │
├───────────────────────┬─────────────────────────┬───────────────────────┤
│    Tipo de Sesgo      │         Impacto         │ Estrategia de Control │
├───────────────────────┼─────────────────────────┼───────────────────────┤
│ 1. Sesgo Geográfico   │ Mayor densidad de       │ Normalización por     │
│    VGI (Voluntariado) │ paradas mapeadas en     │ km de corredor y      │
│                       │ zona urbana (Colima/    │ contraste con         │
│                       │ Villa de Álvarez) que   │ terminales foráneas   │
│                       │ en zonas rurales.       │ oficiales.            │
├───────────────────────┼─────────────────────────┼───────────────────────┤
│ 2. Sesgo de Atributos │ Campos opcionales como  │ No imputar falsos     │
│    Faltantes          │ bancas o techo suelen   │ positivos; categorizar│
│                       │ no estar etiquetados.   │ como "sin registro"   │
│                       │                         │ en lugar de "carece". │
├───────────────────────┼─────────────────────────┼───────────────────────┤
│ 3. Sesgo de Datos     │ Conclusiones ficticias  │ Etiquetado estricto   │
│    Sintéticos         │ sobre retrasos reales   │ simulado=1 y firmas   │
│                       │ del servicio público.   │ de auditoría.         │
└───────────────────────┴─────────────────────────┴───────────────────────┘
```

1. **Sesgo Geográfico de la Información Geográfica Voluntaria (VGI):**  
   - Los datos de OpenStreetMap son aportados por colaboradores voluntarios. En el estado de Colima, la zona conurbada Colima–Villa de Álvarez cuenta con un mapeo de paradas mucho más denso (2.04 paradas/km en Comala) que municipios como Ixtlahuacán (0.29 paradas/km) o Manzanillo (0.12 paradas/km).
   - *Mitigación:* En los análisis de la Capa Oro no se califica a un municipio foráneo como "desatendido" únicamente por el número de paradas en OSM, sino que se documenta explícitamente que la cobertura refleja el estado actual del mapeo colaborativo.
2. **Sesgo de Integridad de Infraestructura:**  
   - De las 161 paradas registradas, menos del 10% tienen etiquetas explícitas sobre si cuentan con refugio contra el sol/lluvia (`shelter=yes`) o bancas (`bench=yes`).
   - *Mitigación:* El pipeline asigna `0` únicamente como ausencia de confirmación, sin asumir que no existe infraestructura física en campo hasta no realizar una validación in situ.

---

## 4. Privacidad y Protección de Datos Personales (Cero PII)

En concordancia con la **LGPDPPSO**:
1. **Inexistencia de Datos Personales (Cero PII):**  
   - El observatorio **no recopila** nombres de choferes, licencias, matrículas vehiculares personales, identificadores de tarjeta de transporte ni patrones de movilidad individual de pasajeros.
2. **Disociación Técnica de Colaboradores de OSM:**  
   - La API de OSM en ocasiones incluye metadatos de edición (`user`, `uid`, `changeset`).
   - *Protocolo de Anonimización:* El extractor de Capa Plata elimina sistemáticamente cualquier identificador de usuario antes de almacenar los registros, conservando exclusivamente la geometría (`lat`, `lon`) y las etiquetas operativas de transporte.
3. **Seguridad y Trazabilidad:**  
   - Cada dato en la Capa Oro está sellado con un hash criptográfico SHA-256 (`lineage_hash_sha256`), lo que garantiza que los datos analíticos no han sido manipulados indebidamente para alterar métricas de puntualidad o desempeño.

---

## 5. Licencia de Distribución de los Datos Derivados

Cumpliendo con la cláusula *Share-Alike* (Compartir Igual) de la licencia ODbL:
* Todo dato depurado (Capa Plata) y toda métrica agregada (Capa Oro) generada por BusCol se publica bajo la licencia **Open Database License (ODbL 1.0)**.
* Cualquier mapa interactivo o visualización generada se comparte bajo la licencia **Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC-BY-SA 4.0)**.
