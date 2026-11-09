# Propuesta del Observatorio — Trusted Data Lab

**Observatorio del Comercio por el Puerto de Manzanillo**
Equipo: Joel Emiliano Salazar Figueroa · Santiago García García
Repositorio: https://github.com/SantiagoPro1/observatorio-comercio-manzanillo

---

## 1. Ficha del observatorio

| Campo | Definición |
|---|---|
| **Sector** | Comercio exterior y logística portuaria (transporte marítimo de contenedores) |
| **Región** | Manzanillo, Colima, comparado con los principales puertos de contenedores de México |
| **Pregunta detonadora** | ¿Cuántos contenedores moverá el Puerto de Manzanillo en los próximos meses y qué factores explican sus subidas y caídas? |
| **Cliente potencial** | Agencias aduanales, transportistas de carga y empresas de almacenaje y patios de contenedores en Manzanillo, que tienen que planear personal, unidades y espacio con semanas de anticipación |
| **Unidad de medida** | TEU (unidad equivalente a un contenedor de 20 pies) |
| **Periodicidad** | Mensual |

### ¿Por qué Manzanillo?

Manzanillo es el puerto con más movimiento de contenedores de México: en 2025 operó **3.89 millones de TEU**, más que cualquier otro puerto del país, según el informe de diciembre de 2025 de la Coordinación General de Puertos y Marina Mercante (CGPMM). Gran parte de la economía de Colima depende de él: transporte, aduanas, patios, servicios y empleo. Cuando el movimiento sube sin aviso, se saturan los accesos y los patios. Cuando baja, sobran unidades y personal. Un buen pronóstico tiene valor económico directo para quien opera alrededor del puerto.

---

## 2. Entrevista de campo

> **Estado:** pendiente. Esta sección se llena después de la entrevista, que debe durar al menos 15 minutos.

| Campo | Dato |
|---|---|
| Entrevistado(a) | _[nombre o iniciales, si pide anonimato]_ |
| Puesto y empresa | _[ej. tramitador en agencia aduanal, operador de transportista]_ |
| Fecha, hora y medio | _[presencial / llamada / videollamada]_ |
| Duración | _[min]_ |
| Entrevistó | _[integrante]_ |

### Guion y respuestas

1. **¿En qué meses o temporadas se nota más el aumento o la caída de contenedores en su trabajo y cómo se preparan?**
   _Respuesta:_
2. **Cuando el puerto se satura, ¿qué problemas le causa a su empresa (tiempos, costos, clientes)? ¿Con cuánta anticipación les gustaría saberlo?**
   _Respuesta:_
3. **¿Qué factores cree que más afectan el volumen de carga: el tipo de cambio, la demanda de EE. UU., Asia, el clima o los bloqueos?**
   _Respuesta:_
4. **¿Hoy cómo deciden cuántas unidades o cuánto personal necesitan? ¿Usan algún dato o pronóstico, o es por experiencia?**
   _Respuesta:_
5. **Si tuviera un tablero con el pronóstico mensual de contenedores y una comparación con Lázaro Cárdenas, ¿lo usaría? ¿Cuánto valdría para su empresa?**
   _Respuesta:_

### Aprendizajes

- _[Aprendizaje 1: qué confirmó o cambió de la pregunta detonadora]_
- _[Aprendizaje 2: qué variable o factor nuevo apareció]_
- _[Aprendizaje 3: qué tan dispuesto está el cliente a usar o pagar el observatorio]_

---

## 3. Las 3 preguntas analíticas

### E1. Variable a pronosticar
**¿Cuántos TEU mensuales operará el Puerto de Manzanillo en los próximos 6 meses?**
- Variable: TEU totales mensuales de Manzanillo (altura más cabotaje).
- Los informes publican el acumulado enero–mes. El TEU mensual se obtiene restando el acumulado del mes anterior; esta transformación se hace en la capa Plata.
- Serie disponible: enero 2021 a la fecha, 60 meses o más. Los informes de 2022 traen también la columna del año anterior.

### E2. Factores a experimentar
**¿Qué factores cambian de forma significativa el movimiento mensual de contenedores en Manzanillo?**
- **Factor A, temporada:** meses de temporada alta (agosto a noviembre, compras navideñas) contra el resto del año.
- **Factor B, tipo de cambio:** meses con peso fuerte contra peso débil, separados por la mediana del tipo de cambio FIX de Banxico.
- **Factor C, tipo de tráfico:** importación contra exportación. Ambos vienen en la tabla "contenedores por tipo de movimiento" del mismo informe.
- Diseño propuesto: ANOVA factorial sobre los TEU mensuales.

### E3. Grupos multivariados a comparar
**¿Manzanillo se comporta igual que los otros grandes puertos de contenedores o tiene un perfil propio?**
- Grupos: **Manzanillo, Lázaro Cárdenas** (Pacífico) contra **Veracruz, Altamira** (Golfo).
- Variables por puerto y mes: TEU totales, TEU llenos, TEU vacíos, importación, exportación y toneladas de carga contenerizada.
- Técnicas candidatas: MANOVA, análisis de componentes principales y clústeres de puertos.

---

## 4. Plan de recopilación de datos

### Fuente 1 (principal): Informe Estadístico Mensual de los Puertos de México, CGPMM

| Aspecto | Detalle |
|---|---|
| Publica | Coordinación General de Puertos y Marina Mercante, Dirección General de Puertos |
| URL | https://www.gob.mx/puertosymarinamercante/acciones-y-programas/informe-estadistico-de-los-puertos-de-mexico-2025 (una página por año, de 2021 a 2025) |
| Formato | PDF mensual de unos 5 MB, con tablas de carga, buques, contenedores y pasajeros por puerto |
| Método | Descarga de los PDF enlazados y extracción de la tabla "Total de contenedores operados por tipo de tráfico (TEUS)" con `pdftotext` |
| Periodos | 2022-01 a 2025-12 (48 informes) más la columna del año anterior, que cubre 2021 |
| Automatización | GitHub Actions (`.github/workflows/captura-bronce.yml`), cada lunes y a mano con *Run workflow* |

**Análisis ético y legal**

- **robots.txt** (https://www.gob.mx/robots.txt, revisado el 8 de noviembre de 2026): solo tiene reglas para los agentes de Google, todas con `Disallow:` vacío. No hay ninguna ruta prohibida, y las páginas de informes y la carpeta `/cms/uploads/` quedan permitidas.
- **Términos de uso** (https://www.gob.mx/terminos):
  - "La información del portal gob.mx es pública a menos que se indique lo contrario". Los informes no indican derechos reservados.
  - Quien "reproduzca o procese información contenida en gob.mx deberá referir la localización electrónica y fecha en que se realizó la consulta". **Lo cumplimos con `data/bronce/manifiesto.csv`**, que guarda la URL exacta, la fecha y hora de descarga y el hash sha256 de cada PDF.
  - Los materiales se autorizan "para su uso personal y no para un uso comercial", y no deben reproducirse ni mostrarse comercialmente. Por eso **no redistribuimos los PDF**: solo guardamos las cifras extraídas, que son información pública, y siempre citamos la fuente. El uso es académico. Si el observatorio se comercializa más adelante (E4), habrá que pedir autorización a la CGPMM o usar la vía de datos abiertos.
- **Buenas prácticas del extractor:**
  - User-Agent que identifica el proyecto y el repositorio.
  - 3 segundos de pausa entre peticiones.
  - No vuelve a descargar los PDF que ya están en el manifiesto, así que en ejecución normal hace pocas peticiones: unas 6 páginas y solo los PDF nuevos.
  - No usa credenciales ni pasa por formularios.
- **Datos personales:** ninguno. Son cifras agregadas por puerto.

### Fuente 2 (complementaria): Banxico SIE API, tipo de cambio FIX

| Aspecto | Detalle |
|---|---|
| Publica | Banco de México, Sistema de Información Económica |
| URL | https://www.banxico.org.mx/SieAPIRest/service/v1/ (serie `SF43718`, tipo de cambio FIX peso-dólar) |
| Formato | API REST JSON con token gratuito |
| Uso | Factor B de E2 y variable explicativa del pronóstico en E1 (promedio mensual del FIX) |
| Estado | El token se guarda como *secret* `BANXICO_TOKEN` de GitHub, nunca en el código |

**Análisis ético y legal**

- **robots.txt** (https://www.banxico.org.mx/robots.txt): solo prohíbe `/dyn/` y `/ALEPH`. La API está en `/SieAPIRest/`, así que está permitida, y además es un canal oficial pensado para el acceso automatizado.
- **Términos de uso:** Banxico ofrece la API para consulta pública con un token personal y límites de consultas por día. Respetamos ese límite con una sola consulta por ejecución que trae toda la serie. Se cita a Banco de México como fuente.
- **Datos personales:** ninguno.

### Fuente 3 (respaldo): ASIPONA Manzanillo

El sitio de la Administración del Sistema Portuario Nacional Manzanillo publica estadísticas propias del puerto. Se revisó y por ahora no tiene `robots.txt` (responde 404) ni una página de estadísticas estable. Se queda como respaldo para validar las cifras de la CGPMM en la capa Plata.

### Arquitectura de capas

```
gob.mx (PDF mensuales) ──► extractor/puertos.py ──► data/bronce/teus/AAAA-MM.csv   (Bronce: cifras tal cual, acumuladas)
Banxico API ─────────────► (E1)                 ──► data/bronce/manifiesto.csv     (procedencia: URL, fecha, sha256)
                                                    data/plata/  (E1: TEU mensual = diferencia de acumulados, validaciones)
                                                    data/oro/    (E2–E3: integración con tipo de cambio y comparativo de puertos)
```

---

## 5. Objetivos de calidad (PSP)

Ver `calidad/objetivos.md`.
