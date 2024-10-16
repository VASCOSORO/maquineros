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

    # Cargar el archivo Excel sin especificar la hoja
    df = pd.read_excel(BytesIO(data), skiprows=2)

    # Limpiar y renombrar las columnas si es necesario
    df.columns = ['Unnamed', 'Precio', 'Cantidad', 'Bulto_x', 'Descripcion', 'Entrega', 'Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero']
    df = df[['Descripcion', 'Precio', 'Bulto_x']]  # Solo las columnas que nos interesan

    # Configurar la interfaz de Streamlit
    st.title("Catálogo de Promociones")

    # Mostrar los ítems del catálogo
    for index, row in df.iterrows():
        st.subheader(row['Descripcion'])
        st.write(f"Precio: ${row['Precio']}")
        st.write(f"Unidades por Bulto: {row['Bulto_x']}")
        st.write("---")
else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
