import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# URL del archivo Excel en GitHub
url = "https://github.com/VASCOSORO/maquineros/raw/main/Catalogo_Limpio_Mini_Superbox.xlsx"

# Descargar el archivo desde GitHub
response = requests.get(url)
if response.status_code == 200:
    data = response.content

    # Cargar el archivo Excel sin especificar la hoja
    xls = pd.ExcelFile(BytesIO(data))
    
    # Mostrar los nombres de las hojas para asegurarnos del correcto
    st.write("Nombres de las hojas en el archivo Excel:")
    st.write(xls.sheet_names)

    # Puedes elegir una hoja después de verificar el nombre correcto
    df = pd.read_excel(BytesIO(data), sheet_name=xls.sheet_names[0], skiprows=2)  # Cambia la hoja si es necesario

    # Limpiar y renombrar las columnas
    df.columns = ['Unnamed', 'Precio', 'Cantidad', 'Bulto_x', 'Descripcion', 'Entrega', 'Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero']
    df = df.drop(columns=['Unnamed'])

    # Agregar las rutas de las imágenes desde el repositorio en GitHub
    base_url = "https://github.com/VASCOSORO/maquineros/raw/main/"
    df['Imagen'] = df['Descripcion'].apply(lambda x: base_url + x.lower().replace(" ", "_") + ".png")

    # Configurar la interfaz de Streamlit
    st.title("Catálogo de Promociones")

    # Mostrar los ítems del catálogo con imágenes
    for index, row in df.iterrows():
        st.image(row['Imagen'], width=150)
        st.subheader(row['Descripcion'])
        st.write(f"Precio: ${row['Precio']}")
        st.write(f"Bulto: {row['Bulto_x']}")
        st.write(f"Entrega: {row['Entrega']}")
        st.write("---")
else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
