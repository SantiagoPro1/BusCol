"""Extractor Bronce: clima horario en la Central "Los Rojos" (Colima) desde Open-Meteo
(sin token). La lluvia es un factor candidato de retrasos en las rutas.

Primera corrida: historia horaria desde 2022 (API de archivo). Después: solo horas nuevas
(API de pronóstico con past_days). Guarda la respuesta cruda con metadatos en
data/bronce/clima/AAAA-MM-DD.json.
"""
import datetime, json, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRONCE = RAIZ / "data" / "bronce" / "clima"
VARS = "temperature_2m,precipitation,rain,weather_code,wind_speed_10m"
PUNTO = "latitude=19.24383&longitude=-103.74157&timezone=America%2FMexico_City"
ARCHIVO = "https://archive-api.open-meteo.com/v1/archive?" + PUNTO + "&hourly=" + VARS + "&start_date={}&end_date={}"
RECIENTE = "https://api.open-meteo.com/v1/forecast?" + PUNTO + "&hourly=" + VARS + "&past_days=7&forecast_days=0"
UA = "ObservatorioRutasColima/1.0 (proyecto escolar; github.com/SantiagoPro1/ManzanilloAduanas)"


def ultima_hora():
    horas = [h for p in BRONCE.glob("*.json") for h in json.loads(p.read_text())["respuesta"]["hourly"]["time"]]
    return max(horas, default=None)


def main():
    BRONCE.mkdir(parents=True, exist_ok=True)
    desde = ultima_hora()
    hoy = datetime.date.today()
    url = RECIENTE if desde else ARCHIVO.format("2022-01-01", hoy - datetime.timedelta(days=6))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        respuesta = json.load(r)
    h = respuesta["hourly"]
    nuevas = [i for i, t in enumerate(h["time"]) if (desde is None or t > desde) and h["temperature_2m"][i] is not None]
    if not nuevas:
        print("sin horas nuevas")
        return 0
    respuesta["hourly"] = {k: [v[i] for i in nuevas] for k, v in h.items()}
    ahora = datetime.datetime.now(datetime.UTC)
    destino = BRONCE / f"{ahora:%Y-%m-%d}.json"
    if destino.exists():  # otra corrida el mismo día: se suma a la anterior
        previo = json.loads(destino.read_text())
        for k, v in respuesta["hourly"].items():
            previo["respuesta"]["hourly"][k] += v
        salida = previo
    else:
        salida = {"fuente": "Open-Meteo", "url": url, "capturado_utc": ahora.isoformat(timespec="seconds"),
                  "respuesta": respuesta}
    destino.write_text(json.dumps(salida, ensure_ascii=False))
    print(f"{len(nuevas)} horas nuevas ({respuesta['hourly']['time'][0]} a {respuesta['hourly']['time'][-1]})")
    return len(nuevas)


if __name__ == "__main__":
    from bitacora import registrar
    registrar("clima", main)
