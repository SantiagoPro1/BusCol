"""GPS SIMULADO de las rutas que salen de la Central "Los Rojos" (Colima).

⚠️ Datos sintéticos: sustituyen al GPS real de la concesionaria hasta que dé acceso.
Cada fila lleva simulado=1. Cuando llegue el GPS real, este módulo se reemplaza por su extractor
y se conservan los mismos archivos y columnas.

- Trazos de ruta: calles reales de OpenStreetMap vía OSRM (se descargan una vez a data/referencia/).
- Viajes: horario por ruta; duración = tiempo OSRM × factor de autobús + paradas, más hora pico,
  fin de semana, ruido e incidentes ocasionales. Es determinista: mismo día y ruta, mismos viajes.
- Salidas: data/bronce/gps_simulado/viajes/AAAA-MM-DD.csv (un viaje por fila, historia desde 2026-08-01)
           data/bronce/gps_simulado/pings/AAAA-MM-DD.csv  (posición de cada unidad cada 5 min)
"""
import csv, datetime as dt, json, math, random, sys, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "bronce" / "gps_simulado"
TRAZOS = RAIZ / "data" / "referencia" / "trazos_osrm.json"
UA = "BusCol/1.0 (proyecto escolar; github.com/SantiagoPro1/BusCol)"
OSRM = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=simplified&geometries=geojson"
COLIMA = dt.timezone(dt.timedelta(hours=-6))  # Colima no tiene horario de verano desde 2022
INICIO = dt.date(2026, 8, 1)
ROJOS = (19.24383, -103.74157)
# ruta: (lat, lon, tipo, minutos entre salidas, primera salida, última salida, unidades)
RUTAS = {
    "villa_de_alvarez": (19.26514, -103.73600, "metropolitana", 15, "05:30", "21:30", 6),
    "comala":           (19.32279, -103.75840, "metropolitana", 20, "05:30", "21:00", 5),
    "coquimatlan":      (19.20129, -103.81050, "metropolitana", 20, "05:30", "21:00", 5),
    "cuauhtemoc":       (19.32855, -103.60150, "metropolitana", 30, "06:00", "20:30", 4),
    "ixtlahuacan":      (19.00119, -103.73790, "foranea", 60, "06:00", "19:00", 3),
    "tecoman":          (18.91091, -103.87340, "foranea", 30, "05:00", "20:00", 6),
    "minatitlan":       (19.38627, -104.04940, "foranea", 90, "06:00", "18:00", 2),
    "manzanillo":       (19.05062, -104.31590, "foranea", 60, "05:00", "19:00", 5),
}
COLS_VIAJE = ["fecha", "ruta", "tipo", "unidad", "salida_programada", "salida_real", "llegada_real",
              "minutos", "minutos_base", "retraso_min", "incidente", "simulado"]
COLS_PING = ["ts", "unidad", "ruta", "lat", "lon", "progreso", "simulado"]


def trazos():
    """Trazo y duración base de cada ruta. Solo consulta OSRM la primera vez."""
    if TRAZOS.exists():
        return json.loads(TRAZOS.read_text())
    datos = {"fuente": "OSRM demo (router.project-osrm.org), datos © OpenStreetMap contributors (ODbL)", "rutas": {}}
    for ruta, (lat, lon, *_) in RUTAS.items():
        req = urllib.request.Request(OSRM.format(ROJOS[1], ROJOS[0], lon, lat), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            ruta_osrm = json.load(r)["routes"][0]
        datos["rutas"][ruta] = {"minutos": ruta_osrm["duration"] / 60, "metros": ruta_osrm["distance"],
                                "coordenadas": ruta_osrm["geometry"]["coordinates"]}  # [lon, lat]
    TRAZOS.parent.mkdir(parents=True, exist_ok=True)
    TRAZOS.write_text(json.dumps(datos))
    return datos


def es_pico(h):
    return 7 <= h < 10 or 13 <= h < 16 or 18 <= h < 20


def viajes_del_dia(ruta, fecha, base):
    lat, lon, tipo, cada, primera, ultima, unidades = RUTAS[ruta]
    rnd = random.Random(f"{ruta}|{fecha}")
    paradas = base["metros"] / (1500 if tipo == "metropolitana" else 5000)
    minutos_base = base["minutos"] * 1.35 + paradas * 0.5
    t = dt.datetime.combine(fecha, dt.time.fromisoformat(primera), COLIMA)
    fin = dt.datetime.combine(fecha, dt.time.fromisoformat(ultima), COLIMA)
    viajes, n = [], 0
    while t <= fin:
        factor = 1.0
        if es_pico(t.hour):
            factor *= 1.25 if tipo == "metropolitana" else 1.12
        if fecha.weekday() >= 5:
            factor *= 0.9
        factor *= rnd.lognormvariate(0, 0.08)
        incidente = rnd.random() < 0.02
        minutos = minutos_base * factor + (rnd.uniform(10, 40) if incidente else 0)
        salida = t + dt.timedelta(minutes=abs(rnd.gauss(0, 2.5)))
        viajes.append({"fecha": fecha.isoformat(), "ruta": ruta, "tipo": tipo,
                       "unidad": f"SIM-{ruta[:3].upper()}-{n % unidades + 1:02d}",
                       "salida_programada": t.isoformat(timespec="minutes"),
                       "salida_real": salida.isoformat(timespec="seconds"),
                       "llegada_real": (salida + dt.timedelta(minutes=minutos)).isoformat(timespec="seconds"),
                       "minutos": round(minutos, 1), "minutos_base": round(minutos_base, 1),
                       "retraso_min": round(minutos - minutos_base, 1), "incidente": int(incidente), "simulado": 1})
        t += dt.timedelta(minutes=cada)
        n += 1
    return viajes


def posicion(coords, f):
    """Punto a la fracción f (0–1) de la distancia de una polilínea [lon, lat]."""
    tramos = [math.dist(a, b) for a, b in zip(coords, coords[1:])]
    falta = f * sum(tramos)
    for (a, b), d in zip(zip(coords, coords[1:]), tramos):
        if falta <= d and d > 0:
            k = falta / d
            return a[1] + (b[1] - a[1]) * k, a[0] + (b[0] - a[0]) * k
        falta -= d
    return coords[-1][1], coords[-1][0]


def escribir(destino, cols, filas, agregar=False):
    destino.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not destino.exists() or not agregar
    with destino.open("a" if agregar else "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        if nuevo:
            w.writeheader()
        w.writerows(filas)


def main():
    t = trazos()["rutas"]
    ahora = dt.datetime.now(COLIMA)
    hoy, filas = ahora.date(), 0
    # viajes: días completos que falten desde INICIO y el día de hoy hasta los viajes ya terminados
    d = INICIO
    while d <= hoy:
        destino = SALIDA / "viajes" / f"{d}.csv"
        if d == hoy or not destino.exists():
            viajes = [v for r in RUTAS for v in viajes_del_dia(r, d, t[r])]
            if d == hoy:
                viajes = [v for v in viajes if dt.datetime.fromisoformat(v["llegada_real"]) <= ahora]
            escribir(destino, COLS_VIAJE, viajes)
            filas += len(viajes) if d != hoy else 0
        d += dt.timedelta(days=1)
    # pings: la hora completa anterior, cada 5 minutos
    hora = ahora.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=1)
    destino = SALIDA / "pings" / f"{hora.date()}.csv"
    if destino.exists() and hora.isoformat(timespec="minutes") in destino.read_text():
        print(f"{filas} viajes nuevos; pings de {hora:%H}:00 ya capturados")
        return filas
    viajes = [v for r in RUTAS for v in viajes_del_dia(r, hora.date(), t[r])]
    pings = []
    for m in range(0, 60, 5):
        ts = hora + dt.timedelta(minutes=m)
        for v in viajes:
            s, l = dt.datetime.fromisoformat(v["salida_real"]), dt.datetime.fromisoformat(v["llegada_real"])
            if s <= ts <= l:
                f = (ts - s) / (l - s)
                lat, lon = posicion(t[v["ruta"]]["coordenadas"], f)
                pings.append({"ts": ts.isoformat(timespec="minutes"), "unidad": v["unidad"], "ruta": v["ruta"],
                              "lat": round(lat, 6), "lon": round(lon, 6), "progreso": round(f, 3), "simulado": 1})
    escribir(destino, COLS_PING, pings, agregar=True)
    print(f"{filas} viajes nuevos; {len(pings)} pings de {hora:%Y-%m-%d %H}:00")
    return filas + len(pings)


if __name__ == "__main__":
    if "--test" in sys.argv:
        base = {"minutos": 20.0, "metros": 9000}
        lunes = dt.date(2026, 11, 9)
        a, b = viajes_del_dia("comala", lunes, base), viajes_del_dia("comala", lunes, base)
        assert a == b, "no es determinista"
        prom = lambda vs: sum(v["minutos"] for v in vs) / len(vs)
        pico = [v for v in a if es_pico(int(v["salida_programada"][11:13]))]
        valle = [v for v in a if not es_pico(int(v["salida_programada"][11:13]))]
        assert prom(pico) > prom(valle), "la hora pico debería tardar más"
        assert all(v["simulado"] == 1 for v in a)
        linea = [[0, 0], [0, 1], [0, 3]]
        assert posicion(linea, 0) == (0, 0) and posicion(linea, 1) == (3, 0) and posicion(linea, 0.5) == (1.5, 0)
        print("ok")
    else:
        from bitacora import registrar
        registrar("gps_simulado", main)
