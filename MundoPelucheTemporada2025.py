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

    # Nombres descriptivos para cada hoja
    sheet_names = {
        "Hoja1": "Para Maquinas",
        "Hoja2": "Peluches 24 cm",
        "Hoja3": "Relojes",
        "Hoja4": "Pelotas"
    }

    # Inicializar `st.session_state` para el pedido si no está ya inicializado
    if "pedido" not in st.session_state:
        st.session_state.pedido = {}
    if "total_pedido" not in st.session_state:
        st.session_state.total_pedido = 0

    # Crear un desplegable para que el usuario seleccione una hoja, usando los nombres descriptivos
    selected_sheet_title = st.selectbox("Selecciona una hoja", list(sheet_names.values()))
    selected_sheet_key = [key for key, value in sheet_names.items() if value == selected_sheet_title][0]

    # Cargar los datos de la hoja seleccionada
    df = pd.read_excel(xls, sheet_name=selected_sheet_key)

    # Limpiar los nombres de las columnas
    df.columns = df.columns.str.strip()

    # Base URL para las imágenes del repositorio
    base_url = "https://github.com/VASCOSORO/maquineros/raw/main/"
    
    # Mostrar los productos de la hoja seleccionada
    st.title(f"Catálogo de {selected_sheet_title}")

    # Función para manejar el pedido de productos
    for index, row in df.iterrows():
        col1, col2 = st.columns([1, 3])

        # Codificar correctamente los nombres de los archivos de imágenes
        nombre_producto = row['nombre'].strip()  # Asegurarse de que no haya espacios adicionales
        nombre_producto_codificado = urllib.parse.quote(nombre_producto)

        # Construir la URL de la imagen
        imagen_url = base_url + nombre_producto_codificado + ".png"

        with col1:
            st.image(imagen_url, width=150)

        # Mostrar el nombre, precio y la opción de agregar al pedido
        with col2:
            st.subheader(row['nombre'])
            st.write(f"Precio por unidad: ${row['Precio']:.2f}")
            
            # Verificar si la columna "Bulto x" existe antes de intentar usarla
            if 'Bulto x' in df.columns:
                # Verificar si el valor de "Bulto x" es numérico y no nulo antes de convertirlo
                if pd.notnull(row['Bulto x']) and isinstance(row['Bulto x'], (int, float)):
                    st.write(f"Unidades por Bulto: {int(row['Bulto x'])}")
                else:
                    st.write(f"Unidades por Bulto: N/A")

            # Seleccionar la cantidad para pedir, almacenando en session_state
            cantidad = st.number_input(f"Cantidad de {row['nombre']}", min_value=0, step=1, key=f"cantidad_{index}")
            
            # Actualizar el pedido en session_state para evitar duplicados
            if cantidad > 0:
                subtotal = cantidad * row['Precio']  # Calcular el subtotal del producto
                st.session_state.pedido[row['nombre']] = {'cantidad': cantidad, 'precio_unitario': row['Precio'], 'subtotal': subtotal}
            elif row['nombre'] in st.session_state.pedido:
                del st.session_state.pedido[row['nombre']]  # Eliminar del pedido si la cantidad es 0

    # Calcular el total del pedido actualizado
    st.session_state.total_pedido = sum(item['subtotal'] for item in st.session_state.pedido.values())

    # Mostrar el resumen del pedido acumulado en todas las hojas
    if st.session_state.pedido:
        st.markdown("### Resumen del Pedido")
        for producto, detalles in st.session_state.pedido.items():
            # Mostrar el precio unitario, cantidad seleccionada y el subtotal con formato de moneda
            st.write(f"**{producto}**")
            st.write(f"Precio unitario: ${detalles['precio_unitario']:.2f} — Cantidad: {detalles['cantidad']} — Subtotal: ${detalles['subtotal']:.2f}")
        
        # Mostrar el total del pedido
        st.markdown(f"**Total del Pedido: ${st.session_state.total_pedido:.2f}**")

        # Crear el mensaje de WhatsApp
        mensaje = "\n".join([f"{producto} - Precio unitario: ${detalles['precio_unitario']:.2f} - Cantidad: {detalles['cantidad']} - Subtotal: ${detalles['subtotal']:.2f}"
                             for producto, detalles in st.session_state.pedido.items()])
        mensaje += f"\nTotal del Pedido: ${st.session_state.total_pedido:.2f}"
        whatsapp_url = f"https://wa.me/5491144042904?text={urllib.parse.quote(mensaje)}"

        # Botón para enviar el pedido por WhatsApp
        if st.button("Enviar pedido por WhatsApp"):
            st.markdown(f"[Enviar pedido por WhatsApp]({whatsapp_url})")

else:
    st.error("No se pudo descargar el archivo Excel. Verifica la URL.")
