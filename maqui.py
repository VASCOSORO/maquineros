import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# URL del archivo Excel en GitHub
url = "https://github.com/VASCOSORO/maquineros/raw/main/Temporada25.xlsx"

# Descargar el archivo desde GitHub
response = requests.get(url)
if response.status_code == 200:
    data = response.content

    # Cargar el archivo Excel
    xls = pd.ExcelFile(BytesIO(data))

    # Obtener los nombres de las hojas
    sheet_names = xls.sheet_names

    # Crear un desplegable para que el usuario seleccione una hoja
    selected_sheet = st.selectbox("Selecciona una hoja", sheet_names)

    # Cargar los datos de la hoja seleccionada
    df = pd.read_excel(xls, sheet_name=selected_sheet)

    # Limpiar los nombres de las columnas
    df.columns = df.columns.str.strip()

    # Reemplazar NaN en 'Bulto x' con 0 para las hojas que lo necesiten
    if 'Bulto x' in df.columns:
        df['Bulto x'] = df['Bulto x'].fillna(0).astype(int)

    # Agregar la URL de las imágenes desde el repositorio en GitHub (sin transformar el nombre)
    base_url = "https://github.com/VASCOSORO/maquineros/raw/main/"
    df['Imagen'] = df['nombre'].apply(lambda x: base_url + x + ".png")

    # Configurar la interfaz de Streamlit
    st.title(f"Catálogo de {selected_sheet}")

    # Mostrar los ítems del catálogo con imagen a la izquierda y texto a la derecha
    for index, row in df.iterrows():
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="{row['Imagen']}" width="150" style="margin-right: 20px;">
            <div>
                <h3>{row['nombre']}</h3>
                <p>Precio: ${row['Precio']}</p>
                {"<p>Unidades por Bulto: {row['Bulto x']}</p>" if 'Bulto x' in df.columns else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
