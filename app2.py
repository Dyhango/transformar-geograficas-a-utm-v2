import streamlit as st
import geopandas as gpd
import os
import zipfile

st.title("🌍 Conversor GIS Profesional")

# Selector de Zona
zona = st.selectbox("Selecciona la Zona UTM:", ["17S", "18S", "19S"])
epsg_psad = {"17S": "24891", "18S": "24891", "19S": "24891"} 
epsg_wgs = {"17S": "32717", "18S": "32718", "19S": "32719"}

uploaded_files = st.file_uploader("Sube los archivos de tu SHP (SHP, DBF, SHX, PRJ)", accept_multiple_files=True)

if uploaded_files:
    # Guardar archivos subidos
    for f in uploaded_files:
        with open(f.name, "wb") as buffer: buffer.write(f.getvalue())
    
    shp_file = [f.name for f in uploaded_files if f.name.endswith(".shp")][0]
    
    if st.button("Procesar Archivos"):
        gdf = gpd.read_file(shp_file)
        
        # Procesamiento
        gdf = gdf.set_crs("EPSG:4248", allow_override=True)
        gdf_utm_psad = gdf.to_crs(f"EPSG:{epsg_psad[zona]}")
        gdf_utm_wgs84 = gdf_utm_psad.to_crs(f"EPSG:{epsg_wgs[zona]}")
        
        # Guardar en disco
        gdf_utm_psad.to_file("UTM_PSAD56.shp")
        gdf_utm_wgs84.to_file("UTM_WGS84.shp")
        
        # Función para crear el ZIP que incluye todos los archivos necesarios para los atributos
        def crear_zip(base_name, zip_name):
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                for ext in ['.shp', '.dbf', '.shx', '.prj']:
                    file_path = base_name + ext
                    if os.path.exists(file_path):
                        zipf.write(file_path, arcname=os.path.basename(file_path))
        
        crear_zip("UTM_PSAD56", "PSAD56_Completo.zip")
        crear_zip("UTM_WGS84", "WGS84_Completo.zip")
        
        st.session_state['procesado'] = True

# Botones de descarga siempre visibles tras procesar
if 'procesado' in st.session_state:
    st.success("¡Transformación exitosa! Descarga tus archivos completos (con tabla de atributos):")
    
    with open("PSAD56_Completo.zip", "rb") as f1: 
        st.download_button("Descargar PSAD56 (Zip)", f1, "PSAD56_Completo.zip")
    with open("WGS84_Completo.zip", "rb") as f2: 
        st.download_button("Descargar WGS84 (Zip)", f2, "WGS84_Completo.zip")
