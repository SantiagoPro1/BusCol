"""Extractor Bronce: paradas de camión (y rutas, si existen) de Colima desde OpenStreetMap,
vía Overpass API (sin clave, ODbL). Sirve para unificar las paradas de las distintas empresas.

Captura una vez al día (las paradas cambian poco): si ya existe el archivo de hoy, no consulta.
Guarda la respuesta cruda con metadatos en data/bronce/paradas/AAAA-MM-DD.json.
"""
import datetime, json, sys, urllib.parse, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRONCE = RAIZ / "data" / "bronce" / "paradas"
URL = "https://overpass-api.de/api/interpreter"
UA = "BusCol/1.0 (proyecto escolar; github.com/SantiagoPro1/BusCol)"
CAJA = "18.85,-104.40,19.45,-103.55"  # estado de Colima, de Manzanillo a Cuauhtémoc
CONSULTA = (f'[out:json][timeout:60];(node["highway"="bus_stop"]({CAJA});'
            f'node["public_transport"="platform"]({CAJA});relation["route"="bus"]({CAJA}););out tags center qt;')


def contar(respuesta):
    tipos = [e["type"] for e in respuesta["elements"]]
    return {"paradas": tipos.count("node"), "rutas": tipos.count("relation")}


def main():
    BRONCE.mkdir(parents=True, exist_ok=True)
    ahora = datetime.datetime.now(datetime.UTC)
    destino = BRONCE / f"{ahora:%Y-%m-%d}.json"
    if destino.exists():
        print("ya capturado hoy")
        return 0
    datos = urllib.parse.urlencode({"data": CONSULTA}).encode()
    req = urllib.request.Request(URL, data=datos, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        respuesta = json.load(r)
    destino.write_text(json.dumps({"fuente": "OpenStreetMap vía Overpass API", "url": URL, "consulta": CONSULTA,
                                   "capturado_utc": ahora.isoformat(timespec="seconds"),
                                   "licencia": "ODbL, © OpenStreetMap contributors", "respuesta": respuesta},
                                  ensure_ascii=False))
    c = contar(respuesta)
    print(f"{c['paradas']} paradas, {c['rutas']} rutas")
    return c["paradas"] + c["rutas"]


if __name__ == "__main__":
    if "--test" in sys.argv:
        assert contar({"elements": [{"type": "node"}, {"type": "node"}, {"type": "relation"}]}) == {"paradas": 2, "rutas": 1}
        print("ok")
    else:
        from bitacora import registrar
        registrar("paradas", main)
