"""Bitácora de ejecuciones de la captura: una fila por corrida y fuente (data/bronce/bitacora.csv)."""
import csv, datetime, time
from pathlib import Path

BITACORA = Path(__file__).resolve().parent.parent / "data" / "bronce" / "bitacora.csv"


def registrar(fuente, fn):
    """Ejecuta fn() (que devuelve registros nuevos) y anota inicio, duración, estado y error."""
    inicio, t0 = datetime.datetime.now(datetime.UTC), time.monotonic()
    estado, registros, error = "ok", 0, ""
    try:
        registros = fn()
    except Exception as e:
        estado, error = "error", f"{type(e).__name__}: {e}"[:300]
        raise
    finally:
        nuevo = not BITACORA.exists()
        with BITACORA.open("a", newline="") as f:
            w = csv.writer(f)
            if nuevo:
                w.writerow(["inicio_utc", "fuente", "estado", "registros_nuevos", "segundos", "error"])
            w.writerow([inicio.isoformat(timespec="seconds"), fuente, estado, registros,
                        round(time.monotonic() - t0, 1), error])
