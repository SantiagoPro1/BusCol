# Propuesta del Observatorio — Trusted Data Lab

**Observatorio del Comercio por el Puerto de Manzanillo**
Equipo: Joel Emiliano Salazar Figueroa · Santiago García García
Repositorio: https://github.com/SantiagoPro1/ManzanilloAduanas

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

> ⚠️ **Entrevista SIMULADA, pendiente de validar con un actor real.** Las respuestas de abajo las redactó el equipo como hipótesis de lo que respondería alguien del sector. **No son declaraciones de una persona real.** Antes de E1 se repetirá el guion con un actor real y esta sección se reemplazará con sus respuestas.

| Campo | Dato |
|---|---|
| Perfil simulado | Coordinador(a) de tráfico en una empresa transportista de contenedores de Manzanillo (anónimo) |
| Medio | Ejercicio de escritorio, no hubo entrevista real |
| Entrevista real | Pendiente |
| Preparó | Equipo |

### Guion y respuestas (hipótesis)

1. **¿En qué meses o temporadas se nota más el aumento o la caída de contenedores en su trabajo y cómo se preparan?**
   _Hipótesis:_ De agosto a noviembre sube la importación de Asia por la temporada navideña, y en enero y febrero baja. En temporada alta se contratan operadores eventuales y se rentan unidades extra.
2. **Cuando el puerto se satura, ¿qué problemas le causa a su empresa (tiempos, costos, clientes)? ¿Con cuánta anticipación les gustaría saberlo?**
   _Hipótesis:_ Filas de horas en los accesos y en el patio, citas perdidas y penalizaciones por demoras (*demurrage*) que terminan pagando los clientes. Les gustaría saberlo con 1 o 2 meses de anticipación para contratar a tiempo.
3. **¿Qué factores cree que más afectan el volumen de carga: el tipo de cambio, la demanda de EE. UU., Asia, el clima o los bloqueos?**
   _Hipótesis:_ La demanda de importaciones (sobre todo de Asia), el tipo de cambio, los huracanes que cierran el puerto y los bloqueos carreteros en la salida a Guadalajara.
4. **¿Hoy cómo deciden cuántas unidades o cuánto personal necesitan? ¿Usan algún dato o pronóstico, o es por experiencia?**
   _Hipótesis:_ Por experiencia y por lo que les avisan los clientes y las navieras con pocos días de margen. No usan ningún pronóstico formal.
5. **Si tuviera un tablero con el pronóstico mensual de contenedores y una comparación con Lázaro Cárdenas, ¿lo usaría? ¿Cuánto valdría para su empresa?**
   _Hipótesis:_ Sí, si se actualiza cada mes y explica por qué sube o baja. La comparación con Lázaro Cárdenas sirve porque compiten por la misma carga.

### Aprendizajes esperados (a confirmar con la entrevista real)

- **La estacionalidad es el factor principal.** Esto refuerza el factor A de E2 (temporada alta de agosto a noviembre).
- **Hay factores externos que la serie de TEU no trae**, como huracanes y bloqueos. Se pueden agregar en E1 o E2 como variables indicadoras (*dummies*) de evento.
- **El valor para el cliente está en anticiparse 1 o 2 meses.** Por eso el horizonte de pronóstico de E1 debe cubrir por lo menos ese plazo.
- **La comparación con Lázaro Cárdenas tiene sentido de negocio.** Los datos de Bronce lo apoyan: en 2025 Manzanillo bajó 0.8 % y Lázaro Cárdenas subió 8.7 % (CGPMM, informe de diciembre de 2025). Esto respalda los grupos de E3.

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
- **Factor B, tipo de cambio:** meses con peso fuerte contra peso débil, separados por la mediana del tipo de cambio USD/MXN (fuente 2).
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
| Estructura | Tabla por puerto: ubicación, TEU de altura, de cabotaje y totales, año anterior y año actual (acumulado enero–mes) |
| Frecuencia | Mensual. La CGPMM publica cada informe con 1 o 2 meses de retraso |
| Bronce | `data/bronce/puertos/teus/AAAA-MM.csv` y `data/bronce/puertos/manifiesto.csv` (URL, sha256, periodo, fecha de captura) |
| Automatización | GitHub Actions (`.github/workflows/captura-bronce.yml`), diario a las 07:00 de Colima y a mano con *Run workflow*. Solo descarga informes nuevos |

**Análisis ético y legal**

- **robots.txt** (https://www.gob.mx/robots.txt, revisado el 8 de noviembre de 2026): solo tiene reglas para los agentes de Google, todas con `Disallow:` vacío. No hay ninguna ruta prohibida, y las páginas de informes y la carpeta `/cms/uploads/` quedan permitidas.
- **Términos de uso** (https://www.gob.mx/terminos):
  - "La información del portal gob.mx es pública a menos que se indique lo contrario". Los informes no indican derechos reservados.
  - Quien "reproduzca o procese información contenida en gob.mx deberá referir la localización electrónica y fecha en que se realizó la consulta". **Lo cumplimos con `data/bronce/puertos/manifiesto.csv`**, que guarda la URL exacta, la fecha y hora de descarga y el hash sha256 de cada PDF.
  - Los materiales se autorizan "para su uso personal y no para un uso comercial", y no deben reproducirse ni mostrarse comercialmente. Por eso **no redistribuimos los PDF**: solo guardamos las cifras extraídas, que son información pública, y siempre citamos la fuente. El uso es académico. Si el observatorio se comercializa más adelante (E4), habrá que pedir autorización a la CGPMM o usar la vía de datos abiertos.
- **Buenas prácticas del extractor:**
  - User-Agent que identifica el proyecto y el repositorio.
  - 3 segundos de pausa entre peticiones.
  - No vuelve a descargar los PDF que ya están en el manifiesto, así que en ejecución normal hace pocas peticiones: unas 6 páginas y solo los PDF nuevos.
  - No usa credenciales ni pasa por formularios.
- **Datos personales:** ninguno. Son cifras agregadas por puerto.

### Fuente 2 (funcionando): Frankfurter API, tipo de cambio USD/MXN

| Aspecto | Detalle |
|---|---|
| Publica | Frankfurter (https://frankfurter.dev), API de código abierto que publica las tasas de referencia diarias del Banco Central Europeo |
| URL | `https://api.frankfurter.dev/v1/AAAA-MM-DD..?from=USD&to=MXN` |
| Estructura | JSON: `{"base":"USD","start_date","end_date","rates":{"AAAA-MM-DD":{"MXN":valor}}}` |
| Formato | API REST JSON, sin token |
| Frecuencia | Diaria, en días hábiles del BCE |
| Método | Petición GET por corrida, solo desde la última fecha guardada (la primera trae la historia desde 2021, unas 1,500 fechas) |
| Bronce | `data/bronce/tipo_cambio/AAAA-MM-DD.json`: respuesta tal cual llegó, más fuente, URL y fecha de captura |
| Uso | Factor B de E2 (peso fuerte contra peso débil) y variable explicativa del pronóstico en E1 (promedio mensual) |

**Análisis ético y legal**

- **robots.txt** (https://api.frankfurter.dev/robots.txt, revisado el 9 de noviembre de 2026): `User-agent: * / Allow: /`. Todo está permitido.
- **Términos de uso** (https://frankfurter.dev/license/): software con licencia MIT. Su documentación dice que no hay cuotas diarias ni mensuales, solo un límite de velocidad contra abuso. Hacemos 1 petición al día y citamos al Banco Central Europeo como fuente original de las tasas.
- **Datos personales:** ninguno.

**Fuente alternativa para E1: Banxico SIE (tipo de cambio FIX, serie `SF43718`).** Es la cifra oficial en México, pero pide un token gratuito. Su `robots.txt` solo prohíbe `/dyn/` y `/ALEPH`, y la API (`/SieAPIRest/`) está permitida. Si se tramita el token, se guardará como *secret* `BANXICO_TOKEN` y servirá para validar las cifras de Frankfurter.

### Fuente 3 (respaldo): ASIPONA Manzanillo

El sitio de la Administración del Sistema Portuario Nacional Manzanillo publica estadísticas propias del puerto. Se revisó y por ahora no tiene `robots.txt` (responde 404) ni una página de estadísticas estable. Se queda como respaldo para validar las cifras de la CGPMM en la capa Plata.

### Arquitectura de capas

```
gob.mx (PDF mensuales) ──► extractores/puertos.py     ──► data/bronce/puertos/teus/AAAA-MM.csv  (TEU acumulados, tal cual)
                                                        └► data/bronce/puertos/manifiesto.csv   (URL, fecha, sha256)
Frankfurter API (BCE) ───► extractores/tipo_cambio.py ──► data/bronce/tipo_cambio/AAAA-MM-DD.json (respuesta cruda + metadatos)
ambos ───────────────────► extractores/bitacora.py    ──► data/bronce/bitacora.csv             (una fila por corrida: estado, registros, error)
                                                          data/plata/  (E1: TEU mensual = diferencia de acumulados, validaciones)
                                                          data/oro/    (E2–E3: integración con tipo de cambio y comparativo de puertos)
```

---

## 5. Objetivos de calidad (PSP)

Ver `calidad/objetivos.md`.
