"""Generador Cartográfico Interactivo para BusCol (Entrega E2)
Genera el mapa interactivo en HTML con Folium mostrando:
- Central de Autobuses Suburbanos 'Los Rojos' (Colima)
- Trazos vectoriales de las 8 rutas (metropolitanas y foráneas)
- Paradas de autobús georreferenciadas desde OpenStreetMap con metadatos de linaje
"""
import json
from pathlib import Path
import folium
from folium.plugins import MarkerCluster, Fullscreen
import pandas as pd
import geopandas as gpd

RAIZ = Path(__file__).resolve().parent.parent
PLATA_DIR = RAIZ / "data" / "plata"
ORO_DIR = RAIZ / "data" / "oro"
DOCS_E2 = RAIZ / "docs" / "E2"
MAPA_SALIDA = DOCS_E2 / "mapa_observatorio_colima.html"

ROJOS_COORD = [19.24383, -103.74157]

COLORES_RUTAS = {
    "villa_de_alvarez": "#2b5c8f",
    "comala":           "#2a9d8f",
    "coquimatlan":      "#3a86ff",
    "cuauhtemoc":       "#0077b6",
    "ixtlahuacan":      "#e76f51",
    "tecoman":          "#e63946",
    "minatitlan":       "#9b5de5",
    "manzanillo":       "#d62828",
}


def construir_mapa():
    DOCS_E2.mkdir(parents=True, exist_ok=True)
    
    # 1. Cargar capas procesadas
    gdf_paradas = gpd.read_parquet(PLATA_DIR / "paradas_colima.parquet")
    gdf_rutas = gpd.read_parquet(PLATA_DIR / "rutas_trazos.parquet")
    df_cobertura = pd.read_parquet(ORO_DIR / "cobertura_rutas_paradas.parquet")
    
    # Crear diccionario rápido de cobertura por ruta
    cob_dict = df_cobertura.set_index("ruta").to_dict(orient="index")
    
    # 2. Inicializar mapa centrado en Colima
    mapa = folium.Map(
        location=ROJOS_COORD,
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True
    )
    Fullscreen().add_to(mapa)
    
    # 3. Marcador especial para la Central "Los Rojos"
    fg_central = folium.FeatureGroup(name="📍 Central 'Los Rojos' (Nodo Principal)")
    popup_rojos = """
    <div style='font-family: Arial; font-size: 13px; width: 230px;'>
        <b style='color: #b7094c; font-size: 14px;'>Central de Autobuses 'Los Rojos'</b><br>
        <i>Blvd. Rodolfo Chávez Carrillo, Colima</i><hr style='margin: 4px 0;'>
        Punto neurálgico de origen de las 8 rutas suburbanas e intermunicipales de BusCol.<br>
        <b>Coordenadas:</b> 19.24383, -103.74157
    </div>
    """
    folium.Marker(
        location=ROJOS_COORD,
        popup=folium.Popup(popup_rojos, max_width=260),
        tooltip="Central de Autobuses Suburbanos 'Los Rojos'",
        icon=folium.Icon(color="darkred", icon="bus", prefix="fa")
    ).add_to(fg_central)
    fg_central.add_to(mapa)
    
    # 4. Capa de Rutas Suburbanas (Vectorial LineStrings)
    fg_rutas_metro = folium.FeatureGroup(name="🚍 Rutas Metropolitanas (4 rutas)")
    fg_rutas_foraneas = folium.FeatureGroup(name="🛣️ Rutas Foráneas (4 rutas)")
    
    for _, r in gdf_rutas.iterrows():
        nombre = r["ruta"]
        tipo = r["tipo"]
        color = COLORES_RUTAS.get(nombre, "#333333")
        linea = r.geometry
        cob = cob_dict.get(nombre, {})
        
        # Puntos [lat, lon] para Folium
        coords = [[p[1], p[0]] for p in linea.coords]
        
        popup_html = f"""
        <div style='font-family: Arial; font-size: 12px; width: 240px;'>
            <b style='font-size: 13px; color: {color};'>Ruta {nombre.replace('_', ' ').title()}</b><br>
            <b>Tipo:</b> {tipo.title()}<br>
            <b>Destino:</b> {r['municipio_destino']}<br>
            <b>Distancia:</b> {cob.get('distancia_km', round(r['distancia_metros']/1000, 2))} km<br>
            <b>Tiempo base:</b> {cob.get('duracion_base_min', r['duracion_base_minutos'])} min<br>
            <b>Paradas en corredor:</b> {cob.get('paradas_en_corredor_300m', 'N/D')}<br>
            <b>Densidad:</b> {cob.get('densidad_paradas_por_km', 'N/D')} paradas/km<br>
            <hr style='margin: 4px 0;'>
            <small style='color: gray;'><b>Linaje:</b> {r['origen_referencia_archivo']}</small>
        </div>
        """
        
        pl = folium.PolyLine(
            locations=coords,
            color=color,
            weight=4 if tipo == "metropolitana" else 5,
            opacity=0.85,
            tooltip=f"Ruta: {nombre.title()} ({tipo})",
            popup=folium.Popup(popup_html, max_width=270)
        )
        
        if tipo == "metropolitana":
            pl.add_to(fg_rutas_metro)
        else:
            pl.add_to(fg_rutas_foraneas)
            
    fg_rutas_metro.add_to(mapa)
    fg_rutas_foraneas.add_to(mapa)
    
    # 5. Capa de Paradas de Autobús (OSM Overpass con Cluster)
    fg_paradas = folium.FeatureGroup(name="🚏 Paradas de Camión OSM (161 nodos)")
    cluster = MarkerCluster().add_to(fg_paradas)
    
    for _, p in gdf_paradas.iterrows():
        refugio_txt = "Sí" if p["tiene_refugio"] == 1 else "No"
        banca_txt = "Sí" if p["tiene_banca"] == 1 else "No"
        
        popup_parada = f"""
        <div style='font-family: Arial; font-size: 11px; width: 220px;'>
            <b style='color: #005f73; font-size: 12px;'>🚏 {p['nombre']}</b><br>
            <b>Operador:</b> {p['operador']}<br>
            <b>Refugio:</b> {refugio_txt} | <b>Banca:</b> {banca_txt}<br>
            <b>Coordenadas:</b> {round(p['latitud'], 5)}, {round(p['longitud'], 5)}<br>
            <hr style='margin: 4px 0;'>
            <small style='color: #6c757d;'>
                <b>Origen Bronce:</b> {p['origen_bronce_id']}<br>
                <b>Archivo:</b> {p['origen_bronce_archivo']}<br>
                <b>Ingesta UTC:</b> {p['fecha_ingesta_utc'][:19]}
            </small>
        </div>
        """
        
        folium.CircleMarker(
            location=[p["latitud"], p["longitud"]],
            radius=4,
            color="#005f73",
            fill=True,
            fill_color="#0a9396",
            fill_opacity=0.8,
            popup=folium.Popup(popup_parada, max_width=250),
            tooltip=f"Parada: {p['nombre']}"
        ).add_to(cluster)
        
    fg_paradas.add_to(mapa)
    
    # 6. Controles finales
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    mapa.save(MAPA_SALIDA)
    print(f"🗺️ [Cartografía E2] Mapa interactivo generado con éxito en: {MAPA_SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    construir_mapa()
