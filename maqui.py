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
    df = pd.read_excel(BytesIO(data))

    # Limpiar los nombres de las columnas
    df.columns = df.columns.str.strip()

    # Reemplazar NaN en 'Bulto x' con 0 antes de convertir a enteros
    df['Bulto x'] = df['Bulto x'].fillna(0).astype(int)

    # Agregar la URL de las imágenes desde el repositorio en GitHub
    base_url = "https://github.com/VASCOSORO/maquineros/raw/main/"
    df['Imagen'] = df['nombre'].apply(lambda x: base_url + x.lower().replace(" ", "_") + ".png")

    # Configurar la interfaz de Streamlit
    st.title("Catálogo de Promociones")

    # Mostrar los ítems del catálogo con imágenes
    for index, row in df.iterrows():
        st.image(row['Imagen'], width=150)
        st.subheader(row['nombre'])
        st.write(f"Precio: ${row['Precio']}")
        st.write(f"Unidades por Bulto: {row['Bulto x']}")
        st.write("---")
else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
