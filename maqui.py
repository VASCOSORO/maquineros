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

    # Cargar el archivo Excel y mostrar las primeras filas para inspeccionar la estructura
    df = pd.read_excel(BytesIO(data), skiprows=2)

    # Mostrar los nombres de las columnas
    st.write("Columnas en el archivo Excel:")
    st.write(df.columns)

    # Mostrar las primeras filas para inspección
    st.write(df.head())

else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
