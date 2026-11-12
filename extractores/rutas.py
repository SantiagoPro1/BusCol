"""Extractor Bronce: tiempo de recorrido con tráfico de las rutas que salen de la
Central de Autobuses Suburbanos "Los Rojos" (Colima), vía TomTom Routing API.

Cada corrida (cada hora) agrega una línea JSON por ruta a data/bronce/rutas/AAAA-MM-DD.jsonl
con la respuesta resumida de la API tal cual (tiempo, retraso por tráfico, distancia) y metadatos.
Necesita la variable de entorno TOMTOM_KEY (secret de GitHub; nunca en el código).
"""
import datetime, json, os, sys, time, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRONCE = RAIZ / "data" / "bronce" / "rutas"
API = ("https://api.tomtom.com/routing/1/calculateRoute/{o}:{d}/json"
       "?key={k}&traffic=true&travelMode=bus&departAt=now&routeType=fastest")
UA = "ObservatorioRutasColima/1.0 (proyecto escolar; github.com/SantiagoPro1/ManzanilloAduanas)"
ROJOS = "19.24383,-103.74157"  # Central "Los Rojos", Blvd. Rodolfo Chávez Carrillo (OpenStreetMap)
# shortcut: destinos = cabeceras municipales (OSM); cambiar por las paradas reales cuando la empresa pase sus rutas
DESTINOS = {
    "villa_de_alvarez": "19.26514,-103.73600",
    "comala": "19.32279,-103.75840",
    "coquimatlan": "19.20129,-103.81050",
    "cuauhtemoc": "19.32855,-103.60150",
    "minatitlan": "19.38627,-104.04940",
    "ixtlahuacan": "19.00119,-103.73790",
    "tecoman": "18.91091,-103.87340",
    "manzanillo": "19.05062,-104.31590",
}


def resumir(destino, respuesta):
    s = respuesta["routes"][0]["summary"]
    return {"ruta": f"rojos-{destino}", "salida": s["departureTime"], "llegada": s["arrivalTime"],
            "segundos": s["travelTimeInSeconds"], "retraso_trafico_s": s["trafficDelayInSeconds"],
            "metros": s["lengthInMeters"], "segundos_sin_trafico": s.get("noTrafficTravelTimeInSeconds")}


def main():
    clave = os.environ.get("TOMTOM_KEY")
    if not clave:
        raise RuntimeError("falta TOMTOM_KEY")
    BRONCE.mkdir(parents=True, exist_ok=True)
    ahora = datetime.datetime.now(datetime.UTC)
    filas = []
    for destino, coord in DESTINOS.items():
        url = API.format(o=ROJOS, d=coord, k=clave)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            fila = resumir(destino, json.load(r))
        fila |= {"fuente": "TomTom Routing API", "capturado_utc": ahora.isoformat(timespec="seconds")}
        filas.append(fila)
        time.sleep(1)
    with (BRONCE / f"{ahora:%Y-%m-%d}.jsonl").open("a") as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in filas)
    print(f"{len(filas)} rutas medidas")
    return len(filas)


if __name__ == "__main__":
    if "--test" in sys.argv:
        r = {"routes": [{"summary": {"departureTime": "a", "arrivalTime": "b", "travelTimeInSeconds": 900,
                                     "trafficDelayInSeconds": 60, "lengthInMeters": 9000}}]}
        f = resumir("comala", r)
        assert f["ruta"] == "rojos-comala" and f["segundos"] == 900 and f["retraso_trafico_s"] == 60, f
        print("ok")
    else:
        from bitacora import registrar
        registrar("rutas", main)
