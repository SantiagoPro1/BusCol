"""Suite de Pruebas Automatizadas: Linaje y Trazabilidad de Datos (Entrega E2)
Proyecto: BusCol - Observatorio de rutas suburbanas de Colima

Verifica que cada registro en la Capa Oro sea 100% rastreable hasta su origen
físico en la Capa Bronce y conserve su fecha de ingesta original.
"""
import json
import re
from pathlib import Path
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent
ORO_DIR = RAIZ / "data" / "oro"
BRONCE_DIR = RAIZ / "data" / "bronce"


def test_existencia_archivos_capa_oro():
    """Verifica que los artefactos de la Capa Oro hayan sido generados."""
    cobertura_parquet = ORO_DIR / "cobertura_rutas_paradas.parquet"
    factores_parquet = ORO_DIR / "factores_retraso_oro.parquet"
    
    assert cobertura_parquet.exists(), f"Falta archivo: {cobertura_parquet}"
    assert factores_parquet.exists(), f"Falta archivo: {factores_parquet}"


def test_columnas_obligatorias_linaje():
    """Verifica que existan las columnas de auditoría y linaje en Capa Oro."""
    df_cob = pd.read_parquet(ORO_DIR / "cobertura_rutas_paradas.parquet")
    columnas_esperadas = [
        "id_oro",
        "lineage_origen_bronce_fuente",
        "lineage_archivo_bronce_paradas",
        "lineage_fecha_ingesta_bronce_utc",
        "lineage_muestra_nodos_bronce",
        "lineage_hash_sha256",
        "pipeline_version"
    ]
    for col in columnas_esperadas:
        assert col in df_cob.columns, f"Columna de linaje faltante: {col}"
        assert df_cob[col].isnull().sum() == 0, f"Existen nulos en la columna {col}"


def test_trazabilidad_paradas_oro_hacia_bronce():
    """
    Auditoría estricta de procedencia:
    Cada registro en la Capa Oro debe apuntar a un archivo real en Capa Bronce,
    concordar con su fecha de captura UTC y validar que los nodos existan en Bronce.
    """
    df_cob = pd.read_parquet(ORO_DIR / "cobertura_rutas_paradas.parquet")
    
    for _, fila in df_cob.iterrows():
        rel_archivo = fila["lineage_archivo_bronce_paradas"]
        archivo_bronce = RAIZ / rel_archivo
        
        # 1. El archivo en Capa Bronce debe existir físicamente
        assert archivo_bronce.exists(), (
            f"Falla de trazabilidad: {fila['id_oro']} referencia un archivo inexistente en Bronce: {rel_archivo}"
        )
        
        # 2. La fecha de ingesta en Oro debe coincidir con la de Bronce
        with open(archivo_bronce, "r", encoding="utf-8") as f:
            datos_bronce = json.load(f)
            
        assert datos_bronce["capturado_utc"] == fila["lineage_fecha_ingesta_bronce_utc"], (
            f"Falla de fecha de ingesta en {fila['id_oro']}: "
            f"Oro dice {fila['lineage_fecha_ingesta_bronce_utc']} pero Bronce dice {datos_bronce['capturado_utc']}"
        )
        
        # 3. Los IDs de nodos reportados en la muestra de Oro deben existir en el payload crudo de Bronce
        nodos_en_bronce = {f"node/{elem['id']}" for elem in datos_bronce["respuesta"]["elements"] if elem.get("type") == "node"}
        
        # Extraer los IDs individuales de la muestra
        muestra_texto = fila["lineage_muestra_nodos_bronce"]
        ids_en_muestra = re.findall(r"node/\d+", muestra_texto)
        
        for id_nodo in ids_en_muestra:
            assert id_nodo in nodos_en_bronce, (
                f"Falla de integridad: El nodo {id_nodo} en {fila['id_oro']} no existe en el archivo crudo {rel_archivo}"
            )


def test_trazabilidad_viajes_factores_hacia_bronce():
    """Verifica que la tabla de factores analíticos provenga de los viajes de Bronce."""
    df_fac = pd.read_parquet(ORO_DIR / "factores_retraso_oro.parquet")
    
    assert "lineage_origen_bronce" in df_fac.columns
    assert "lineage_hash_sha256" in df_fac.columns
    
    directorio_viajes = RAIZ / df_fac["lineage_origen_bronce"].iloc[0]
    assert directorio_viajes.exists() and directorio_viajes.is_dir()
    
    # Comprobar que existen archivos de viajes en Bronce
    viajes_archivos = list(directorio_viajes.glob("*.csv"))
    assert len(viajes_archivos) >= 36, f"Se esperaban ≥36 periodos en Bronce, encontrados {len(viajes_archivos)}"


def test_firmas_criptograficas_sha256():
    """Verifica la validez formal del hash SHA-256 de linaje."""
    df_cob = pd.read_parquet(ORO_DIR / "cobertura_rutas_paradas.parquet")
    for _, fila in df_cob.iterrows():
        hash_val = fila["lineage_hash_sha256"]
        assert len(hash_val) == 64, f"Hash SHA-256 inválido (longitud {len(hash_val)}): {hash_val}"
        assert re.match(r"^[0-9a-f]{64}$", hash_val), f"Hash SHA-256 no hexadecimal: {hash_val}"
