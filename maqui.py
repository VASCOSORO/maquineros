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

    # Mostrar los nombres de las columnas para verificar
    st.write("**Columnas en el archivo Excel después de limpiar:**")
    st.write(df.columns.tolist())

    # Seleccionar las columnas relevantes (ajusta los nombres según sea necesario)
    df = df[['Nombre', 'Precio', 'Bulto x']]

    # Configurar la interfaz de Streamlit
    st.title("Catálogo de Promociones")

    # Mostrar los ítems del catálogo
    for index, row in df.iterrows():
        st.subheader(row['Nombre'])
        st.write(f"Precio: ${row['Precio']}")
        st.write(f"Unidades por Bulto: {row['Bulto x']}")
        st.write("---")
else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
