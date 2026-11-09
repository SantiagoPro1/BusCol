"""Extractor Bronce: TEUs por puerto desde los informes mensuales oficiales de la
Coordinación General de Puertos y Marina Mercante (gob.mx).

Guarda la tabla "TOTAL DE CONTENEDORES OPERADOS POR TIPO DE TRAFICO" tal como se
publica (acumulado enero–mes, año anterior y año actual) en data/bronce/teus/.
No se suben los PDF (~5 MB c/u); el manifiesto guarda URL y sha256 para reproducir.
"""
import csv, datetime, hashlib, re, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRONCE = RAIZ / "data" / "bronce" / "teus"
MANIFIESTO = RAIZ / "data" / "bronce" / "manifiesto.csv"
PAGINA = "https://www.gob.mx/puertosymarinamercante/acciones-y-programas/informe-estadistico-de-los-puertos-de-mexico-{}"
UA = "ObservatorioManzanillo/1.0 (proyecto escolar; github.com/SantiagoPro1/observatorio-comercio-manzanillo)"
PAUSA = 3  # segundos entre peticiones, para no cargar el servidor
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
NUM = r"(-|[\d,]+)"
FILA = re.compile(rf"^\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ .,]+?)\s{{2,}}{NUM}\s+{NUM}\s+\S+\s+{NUM}\s+{NUM}\s+\S+\s+{NUM}\s+{NUM}\s+\S+\s*$")
COLS = ["ubicacion", "altura_anterior", "altura_actual", "cabotaje_anterior",
        "cabotaje_actual", "total_anterior", "total_actual"]


def bajar(url):
    time.sleep(PAUSA)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def parsear(texto):
    """Devuelve (mes 1-12, filas) de la tabla de TEUs totales, o None si no está."""
    i = texto.find("TOTAL DE CONTENEDORES OPERADOS POR TIPO DE TRAFICO")
    if i < 0:
        return None
    bloque = texto[i:i + 6000]
    # encabezado tipo "enero – diciembre" o "Enero a enero"; el último mes nombrado es el corte
    cab = bloque[:300].lower()
    mes = max((cab.rfind(m), n) for n, m in enumerate(MESES, 1))
    filas = []
    for linea in bloque.splitlines()[3:]:
        m = FILA.match(linea)
        if m:
            filas.append([m.group(1).strip()] + [v.replace(",", "").replace("-", "0") for v in m.groups()[1:]])
        if linea.strip().startswith("TOTAL ") and filas:
            break
    return (mes[1], filas) if mes[0] >= 0 and filas else None


def main():
    BRONCE.mkdir(parents=True, exist_ok=True)
    vistos = set()
    if MANIFIESTO.exists():
        vistos = {r["url"] for r in csv.DictReader(MANIFIESTO.open())}
    nuevos = []
    for anio in range(2022, datetime.date.today().year + 1):
        try:
            html = bajar(PAGINA.format(anio)).decode("utf-8", "ignore")
        except Exception as e:  # la página del año en curso puede no existir todavía
            print(f"{anio}: sin página ({e})")
            continue
        for ruta in sorted(set(re.findall(r"/cms/uploads/attachment/file/\d+/[^\"']+\.pdf", html))):
            url = "https://www.gob.mx" + ruta
            if url in vistos or "acumulado" in ruta.lower():
                continue
            pdf = bajar(url)
            with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
                f.write(pdf); f.flush()
                texto = subprocess.run(["pdftotext", "-layout", f.name, "-"],
                                       capture_output=True, text=True).stdout
            res = parsear(texto)
            periodo = ""
            if res:
                periodo = f"{anio}-{res[0]:02d}"
                destino = BRONCE / f"{periodo}.csv"
                if not destino.exists():  # hay informes duplicados (normal y "comparativo"); gana el primero
                    with destino.open("w", newline="") as out:
                        w = csv.writer(out); w.writerow(COLS); w.writerows(res[1])
            nuevos.append({"url": url, "sha256": hashlib.sha256(pdf).hexdigest(), "periodo": periodo,
                           "descargado": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")})
            print(url, "->", periodo or "sin tabla de TEUs")
    if nuevos:
        nuevo_archivo = not MANIFIESTO.exists()
        with MANIFIESTO.open("a", newline="") as out:
            w = csv.DictWriter(out, fieldnames=["url", "sha256", "periodo", "descargado"])
            if nuevo_archivo:
                w.writeheader()
            w.writerows(nuevos)
    print(f"{len(nuevos)} PDF nuevos; {len(list(BRONCE.glob('*.csv')))} periodos en bronce")


if __name__ == "__main__":
    if "--test" in sys.argv:
        muestra = ("TOTAL DE CONTENEDORES OPERADOS POR TIPO DE TRAFICO\n   enero – septiembre\n   TEUS\n\n"
                   "MANZANILLO, COL.             2,911,798          2,880,209           (1.1)                -                   -         N/C         2,911,798          2,880,209           (1.1)\n"
                   "               TOTAL        650,066                606,510       (6.7)               788                -       N/C      650,854              606,510        (6.8)\n")
        mes, filas = parsear(muestra)
        assert mes == 9 and filas[0] == ["MANZANILLO, COL.", "2911798", "2880209", "0", "0", "2911798", "2880209"], (mes, filas)
        print("ok")
    else:
        main()
