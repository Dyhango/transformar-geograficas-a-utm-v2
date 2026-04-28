import streamlit as st
import geopandas as gpd
import os

st.title("🌍 Conversor GIS Profesional")

# Selector de Zona
zona = st.selectbox("Selecciona la Zona UTM:", ["17S", "18S", "19S"])
# Mapeo de códigos EPSG para PSAD56 y WGS84 según zona
epsg_psad = {"17S": "24891", "18S": "24891", "19S": "24891"} 
epsg_wgs = {"17S": "32717", "18S": "32718", "19S": "32719"}

uploaded_files = st.file_uploader("Sube los archivos de tu SHP", accept_multiple_files=True)

if st.button("Procesar Archivos"):
    if uploaded_files:
        # Guardar archivos
        for f in uploaded_files:
            with open(f.name, "wb") as buffer: buffer.write(f.getvalue())
        
        shp_file = [f.name for f in uploaded_files if f.name.endswith(".shp")][0]
        gdf = gpd.read_file(shp_file)
        
        # Proceso
        gdf = gdf.set_crs("EPSG:4248", allow_override=True)
        gdf_utm_psad = gdf.to_crs(f"EPSG:{epsg_psad[zona]}")
        gdf_utm_wgs84 = gdf_utm_psad.to_crs(f"EPSG:{epsg_wgs[zona]}")
        
        # Guardar formatos
        gdf_utm_psad.to_file("UTM_PSAD56.shp")
        gdf_utm_wgs84.to_file("UTM_WGS84.shp")
        # Exportar a DXF para AutoCAD
        gdf_utm_wgs84.to_file("UTM_WGS84.dxf", driver="DXF")
        
        st.success("¡Transformación exitosa!")
        
        # Botones de descarga
        with open("UTM_PSAD56.shp", "rb") as f1: 
            st.download_button("Descargar PSAD56", f1, "UTM_PSAD56.shp")
        with open("UTM_WGS84.shp", "rb") as f2: 
            st.download_button("Descargar WGS84", f2, "UTM_WGS84.shp")
        with open("UTM_WGS84.dxf", "rb") as f3: 
            st.download_button("Descargar para AutoCAD (.dxf)", f3, "UTM_WGS84.dxf")