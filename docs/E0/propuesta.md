# Propuesta del Observatorio — Trusted Data Lab

**BusCol: observatorio de rutas suburbanas de Colima**
Equipo: Joel Emiliano Salazar Figueroa · Santiago García García
Repositorio: https://github.com/SantiagoPro1/BusCol

> **Cambio de proyecto (11 de noviembre de 2026).** La versión entregada en la etiqueta `e0` trataba el comercio por el Puerto de Manzanillo. Con la aprobación del profesor, el observatorio cambió a las rutas de autobús que salen de la Central "Los Rojos". La versión anterior sigue disponible en la etiqueta `e0`.

---

## 1. Ficha del observatorio

| Campo | Definición |
|---|---|
| **Sector** | Transporte público suburbano y foráneo de pasajeros |
| **Región** | Zona metropolitana Colima–Villa de Álvarez y municipios conectados por autobús desde la Central de Autobuses Suburbanos "Los Rojos" (Blvd. Rodolfo Chávez Carrillo, Colima) |
| **Pregunta detonadora** | ¿Cuánto tardan realmente las rutas que salen de "Los Rojos" y qué hace que se retrasen (hora, día, tráfico)? ¿Se puede avisar al pasajero cuándo llega su camión? |
| **Cliente potencial** | Las empresas concesionarias (por ejemplo, Nuevo Horizonte, que renta su espacio en la central) y la propia central, que pagarían por un tablero y una app de rastreo que atraiga más pasajeros. Usuarios finales: los pasajeros que hoy esperan "a ver si pasa" |
| **Producto final** | Tablero de tiempos y retrasos por ruta, aviso tipo "tu camión llega en 6 minutos" y buzón de quejas e incidentes |

### Por qué

Hoy el pasajero no sabe si el camión ya pasó, si viene retrasado o si hubo un accidente, y pierde tiempo esperando. En ciudades europeas como Berlín o Viena la parada anuncia "el siguiente autobús llega en 6 minutos". No pedimos puntualidad suiza, sino **saber dónde viene el camión**. Las unidades ya traen GPS. Falta unir y mostrar esos datos. Si el pasajero sabe cuándo llega el camión, lo usa más, y eso es lo que le interesa a la empresa.

---

## 2. Entrevista de campo

### 2.1 Plática con el asesor del proyecto (realizada)

| Campo | Dato |
|---|---|
| Entrevistado | Profesor y asesor del proyecto (conoce la operación del transporte en Colima) |
| Fecha y medio | 11 de noviembre de 2026, nota de voz (~4 min) |
| Evidencia | Audio de WhatsApp, transcrito |

Lo que dijo, en resumen:
1. **Quién opera:** la movilidad de Colima y Villa de Álvarez la manejan distintas centrales o concesionarias. Flecha Amarilla cubre la zona norte, hacia Tonila. **Nuevo Horizonte** llega a la Central "Los Rojos" y paga una renta por usarla.
2. **Tecnología disponible:** las unidades **ya tienen GPS**. No hay que instalar nada, solo conseguir que el corporativo dé **acceso a la ubicación en tiempo real**.
3. **Paradas:** las rutas salen de "Los Rojos" y tienen paradas internas en Colima y Villa de Álvarez. Hay que **unificar las paradas** de las distintas empresas.
4. **Referencia:** el transporte en Alemania o Austria, donde la parada avisa cuánto falta para el siguiente autobús, y también si hubo un accidente o dónde viene la unidad.
5. **Modelo de negocio:** primero presentar la idea al corporativo y ver si la compra. Si no, replantear la propuesta de valor. El argumento es que **más usuarios usarán el transporte si saben dónde viene el camión**. Hoy, no saberlo significa pérdida de tiempo.

### 2.2 Entrevista con actor del sector (pendiente)

> **Pendiente.** Esta entrevista, de al menos 15 minutos, es con el contacto del corporativo de transporte que nos va a presentar el profesor. Se llenará con este guion.

1. ¿Qué rutas salen de "Los Rojos", con qué frecuencia y cuántas unidades tiene cada una?
2. ¿Qué tanto se retrasan las unidades y en qué horarios o tramos? ¿Cómo se enteran hoy?
3. ¿Qué GPS usan, quién lo administra y en qué formato se puede exportar la ubicación (API, archivo, plataforma)?
4. ¿Qué quejas reciben más de los pasajeros y por qué medio les llegan?
5. Si hubiera una app con la ubicación en vivo, el tiempo de llegada y un buzón de quejas, ¿la usarían? ¿Cuánto pagarían o qué tendría que demostrar?

---

## 3. Las 3 preguntas analíticas

### E1. Variable a pronosticar
**¿Cuántos minutos tardará cada ruta desde "Los Rojos" en la siguiente hora y el siguiente día?**
- Variable: tiempo de recorrido (minutos) por ruta y por hora.
- Fuente: el GPS de las unidades cuando la empresa dé acceso (datos reales de cada camión). Mientras tanto, y después como comparación, el tiempo con tráfico de TomTom.

### E2. Factores a experimentar
**¿Qué factores aumentan de forma significativa el tiempo de recorrido?**
- **Factor A, hora:** hora pico (7–9 h y 13–15 h) contra hora valle.
- **Factor B, día:** entre semana contra fin de semana.
- **Factor C, tipo de ruta:** metropolitana contra foránea, o número de paradas en el trayecto (fuente 2).
- Diseño: ANOVA factorial sobre el retraso respecto al tiempo sin tráfico, por ruta.

### E3. Grupos multivariados a comparar
**¿Las rutas metropolitanas se comportan distinto de las foráneas?**
- **Metropolitanas:** Villa de Álvarez, Comala, Coquimatlán y Cuauhtémoc.
- **Foráneas:** Tecomán, Manzanillo, Minatitlán e Ixtlahuacán.
- Variables por ruta: tiempo medio, variabilidad, retraso por tráfico, velocidad media (km/h) y número de paradas.
- Técnicas: MANOVA, componentes principales y clústeres de rutas.

---

## 4. Plan de recopilación de datos

### Fuente 1: tiempos de recorrido con tráfico (TomTom Routing API)

| Aspecto | Detalle |
|---|---|
| Qué mide | Tiempo de recorrido con tráfico, retraso por tráfico y distancia de "Los Rojos" a 8 destinos |
| URL | `https://api.tomtom.com/routing/1/calculateRoute/{origen}:{destino}/json?traffic=true&travelMode=bus` |
| Estructura | JSON → `routes[0].summary`: `travelTimeInSeconds`, `trafficDelayInSeconds`, `lengthInMeters`, `departureTime`, `arrivalTime` |
| Formato y acceso | API REST con clave gratuita (*secret* `TOMTOM_KEY`) |
| Frecuencia | Cada hora con GitHub Actions: 8 rutas × 24 = 192 peticiones al día, de un límite gratuito de 2,500 |
| Bronce | `data/bronce/rutas/AAAA-MM-DD.jsonl`, una línea por ruta y hora con fuente y hora de captura |
| robots.txt | `https://api.tomtom.com/robots.txt` responde 404, así que no hay restricciones publicadas para la API |
| Términos | ⚠️ **Por verificar.** Las condiciones de TomTom podrían limitar el guardado permanente de resultados. Antes de acumular historia hay que revisar sus términos para el plan gratuito. Si no lo permiten, esta fuente se reemplaza por la fuente 3 |

### Fuente 2: paradas de camión de OpenStreetMap (Overpass API), funcionando

| Aspecto | Detalle |
|---|---|
| Qué mide | Paradas de autobús (`highway=bus_stop`, `public_transport=platform`) y rutas de autobús (`route=bus`) del estado de Colima |
| URL | `https://overpass-api.de/api/interpreter` (consulta POST con la caja 18.85,-104.40,19.45,-103.55) |
| Estructura | JSON → `elements[]`: tipo, id, coordenadas (`lat`/`lon` o `center`) y etiquetas (`name`, `operator`, `route_ref`, etc.) |
| Formato y acceso | API REST JSON, sin clave |
| Frecuencia | Una vez al día. El workflow lo llama cada hora, pero si ya existe la captura del día no vuelve a consultar |
| Situación actual | **161 paradas** mapeadas y **0 rutas**: nadie ha mapeado todavía las rutas de camión de Colima en OSM. BusCol puede aportar ese mapeo |
| Bronce | `data/bronce/paradas/AAAA-MM-DD.json`: respuesta cruda más fuente, consulta, licencia y hora de captura |
| Uso | Unificar las paradas de las distintas empresas, ubicar las paradas en cada trayecto y contarlas para E3 |
| robots.txt | `Disallow: /api/` para todos los agentes. Va dirigido a buscadores. La política de uso de Overpass permite expresamente consultas por API (menos de 10,000 al día y 1 GB). Hacemos 1 al día |
| Términos y licencia | Datos de OpenStreetMap con licencia **ODbL**: se pueden usar y guardar citando "© OpenStreetMap contributors", y los datos derivados se comparten con la misma licencia |

### Fuente 3: GPS de las unidades (pendiente de acceso)

- **Qué es:** la ubicación en tiempo real de los camiones, tomada de la plataforma GPS de la concesionaria. Es la fuente principal del producto.
- **Acceso:** solo con autorización por escrito del corporativo, en la forma que ellos indiquen (API, exportación o plataforma). No haremos *scraping* de su plataforma sin permiso.
- **Ética:** son datos de unidades, no de personas. No se guardan datos de conductores ni de pasajeros. Las ubicaciones en vivo solo se publican con permiso de la empresa.

### Arquitectura de capas

```
TomTom Routing API ──► extractores/rutas.py ──► data/bronce/rutas/AAAA-MM-DD.jsonl   (tiempo por ruta y hora)
OSM / Overpass ──────► extractores/paradas.py ► data/bronce/paradas/AAAA-MM-DD.json  (paradas, 1 vez al día)
GPS concesionaria ───► (cuando haya acceso)  ──► data/bronce/gps/
ambos ───────────────► extractores/bitacora.py ► data/bronce/bitacora.csv            (una fila por corrida)
                                               data/plata/ (E1: tiempos limpios por ruta y hora, con sus paradas)
                                               data/oro/   (E2–E3: retrasos por factor y perfil por ruta)
```

---

## 5. Objetivos de calidad (PSP)

Ver `calidad/objetivos.md`.
