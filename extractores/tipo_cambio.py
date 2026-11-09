"""Extractor Bronce: tipo de cambio diario USD/MXN desde la API pública Frankfurter
(tasas de referencia del Banco Central Europeo, sin token).

Cada corrida guarda la respuesta JSON tal cual llegó, con metadatos de captura, en
data/bronce/tipo_cambio/AAAA-MM-DD.json. La primera trae la historia desde 2021;
las siguientes solo desde la última fecha ya capturada.
"""
import datetime, json, sys, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRONCE = RAIZ / "data" / "bronce" / "tipo_cambio"
API = "https://api.frankfurter.dev/v1/{}..?from=USD&to=MXN"
UA = "ObservatorioManzanillo/1.0 (proyecto escolar; github.com/SantiagoPro1/ManzanilloAduanas)"
INICIO = "2021-01-01"


def ultima_fecha():
    fechas = [f for p in BRONCE.glob("*.json") for f in json.loads(p.read_text())["respuesta"]["rates"]]
    return max(fechas, default=INICIO)


def main():
    BRONCE.mkdir(parents=True, exist_ok=True)
    desde = ultima_fecha()
    url = API.format(desde)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        respuesta = json.load(r)
    nuevas = {f: v for f, v in respuesta["rates"].items() if f > desde or desde == INICIO}
    if not nuevas:
        print("sin fechas nuevas")
        return 0
    respuesta["rates"] = nuevas
    hoy = datetime.datetime.now(datetime.UTC)
    salida = {"fuente": "Frankfurter API (BCE)", "url": url,
              "capturado_utc": hoy.isoformat(timespec="seconds"), "respuesta": respuesta}
    destino = BRONCE / f"{hoy:%Y-%m-%d}.json"
    if destino.exists():  # segunda corrida del mismo día: se suma a la primera
        previo = json.loads(destino.read_text())
        previo["respuesta"]["rates"].update(nuevas)
        salida = previo
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=1))
    print(f"{len(nuevas)} fechas nuevas ({min(nuevas)} a {max(nuevas)})")
    return len(nuevas)


if __name__ == "__main__":
    from bitacora import registrar
    registrar("tipo_cambio", main)
