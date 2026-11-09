# Ficha de entrega técnica — E0

| Campo | Valor |
|---|---|
| Proyecto | Trusted Data Lab: Observatorio del Comercio por el Puerto de Manzanillo |
| Entrega | E0, pregunta central, validación y capa Bronce |
| Tag | `e0` |
| Repositorio | https://github.com/SantiagoPro1/observatorio-comercio-manzanillo |
| Integrantes | Joel Emiliano Salazar Figueroa (@EmiSalazarrrr) · Santiago García García (@SantiagoPro1) |
| Fecha límite | lunes 9 de noviembre de 2026, 23:59 |

## Entregables

| # | Entregable | Ubicación | Estado |
|---|---|---|---|
| 1 | Propuesta del observatorio | `docs/E0/propuesta.md` | ✅ (entrevista: ver sección 2) |
| 2a | Extractor ético | `extractor/puertos.py` | ✅ |
| 2b | Ejecución automática | `.github/workflows/captura-bronce.yml` (cada lunes + manual) | ✅ |
| 2c | Serie histórica cruda ≥ 36 periodos | `data/bronce/teus/` + `data/bronce/manifiesto.csv` | ✅ |
| 3a | Registros PSP por integrante | `calidad/tiempo-*.csv`, `calidad/defectos-*.csv` | ✅ |
| 3b | 3 objetivos de calidad medibles | `calidad/objetivos.md` | ✅ |
| 4 | Esta ficha | `docs/E0/ENTREGA.md` | ✅ |

## Cómo reproducir la capa Bronce

```bash
sudo apt-get install -y poppler-utils   # pdftotext
python3 extractor/puertos.py --test      # autoprueba del parser
python3 extractor/puertos.py             # descarga lo nuevo y actualiza data/bronce/
```

Solo usa la biblioteca estándar de Python 3.11 o superior y `pdftotext`. En GitHub también se puede correr desde **Actions → Captura Bronce → Run workflow**.

## Estructura de los datos crudos

`data/bronce/teus/AAAA-MM.csv` contiene una fila por puerto o litoral tal como aparece en el informe. Los valores son el **acumulado enero–mes** en TEU.

| Columna | Significado |
|---|---|
| `ubicacion` | Puerto o litoral (PACIFICO, GOLFO - CARIBE, TOTAL) |
| `altura_anterior`, `altura_actual` | TEU de tráfico internacional, año anterior y año del informe |
| `cabotaje_anterior`, `cabotaje_actual` | TEU de tráfico entre puertos nacionales |
| `total_anterior`, `total_actual` | Suma de altura y cabotaje |

Los `-` del informe se guardan como `0`. El cálculo del TEU mensual y las validaciones quedan para la capa Plata (E1).

## Limitaciones conocidas

- Algunos meses de 2025 se publican dos veces, como informe normal y como "comparativo". El extractor se queda con el primero que encuentra.
- La página de 2026 todavía no existe en gob.mx. El workflow la intenta cada semana y la toma en cuanto se publique.
- La fuente 2 (Banxico) espera el *secret* `BANXICO_TOKEN`. Se integra en E1.
