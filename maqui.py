import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import urllib.parse

# URL del archivo Excel en GitHub
url = "https://github.com/VASCOSORO/maquineros/raw/main/Temporada25.xlsx"

# Descargar el archivo desde GitHub
response = requests.get(url)
if response.status_code == 200:
    data = response.content

    # Cargar el archivo Excel
    xls = pd.ExcelFile(BytesIO(data))

    # Renombrar las hojas
    sheet_names = {
        "Hoja1": "Para Maquinas",
        "Hoja2": "Peluches 24 cm",
        "Hoja3": "Relojes",
        "Hoja4": "Pelotas"
    }

    # Crear un desplegable para que el usuario seleccione una hoja
    selected_sheet_key = st.selectbox("Selecciona una hoja", list(sheet_names.keys()))
    selected_sheet = sheet_names[selected_sheet_key]

    # Cargar los datos de la hoja seleccionada
    df = pd.read_excel(xls, sheet_name=selected_sheet_key)

    # Limpiar los nombres de las columnas
    df.columns = df.columns.str.strip()

    # Inicializar el carrito para guardar los pedidos
    pedido = []

    # Base URL para las imágenes del repositorio (sin modificar los nombres de los productos)
    base_url = "https://github.com/VASCOSORO/maquineros/raw/main/"
    
    # Mostrar los productos de la hoja seleccionada
    st.title(f"Catálogo de {selected_sheet}")

    # Función para manejar el pedido de productos
    for index, row in df.iterrows():
        col1, col2 = st.columns([1, 3])

        # Construir el nombre de la imagen y mostrarla tal como está en el repositorio
        imagen_url = base_url + row['nombre'] + ".png"
        with col1:
            st.image(imagen_url, width=150)

        # Mostrar el nombre, precio y la opción de agregar al pedido
        with col2:
            st.subheader(row['nombre'])
            st.write(f"Precio: ${row['Precio']}")
            if 'Bulto x' in df.columns:
                st.write(f"Unidades por Bulto: {row['Bulto x']}")

            # Seleccionar la cantidad para pedir
            cantidad = st.number_input(f"Cantidad de {row['nombre']}", min_value=0, step=1, key=f"cantidad_{index}")
            if cantidad > 0:
                pedido.append(f"{row['nombre']} - Cantidad: {cantidad}, Precio por unidad: ${row['Precio']}")

    # Si hay productos en el pedido, mostrar el resumen y opción de enviar por WhatsApp
    if pedido:
        st.markdown("### Resumen del Pedido")
        for item in pedido:
            st.write(item)

        # Crear el mensaje de WhatsApp
        mensaje = "\n".join(pedido)
        whatsapp_url = f"https://wa.me/5491144042904?text={urllib.parse.quote(mensaje)}"

        # Botón para enviar el pedido por WhatsApp
        if st.button("Enviar pedido por WhatsApp"):
            st.markdown(f"[Enviar pedido por WhatsApp]({whatsapp_url})")

else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
