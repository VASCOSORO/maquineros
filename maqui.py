import streamlit as st
import pandas as pd

# Cargar los datos desde el archivo Excel (ajusta la ruta según sea necesario)
file_path = 'Temporada 2025 maquinas mini y superbox.xlsx'
df = pd.read_excel(file_path, sheet_name='Mini y Superbox', skiprows=2)

# Limpiar y renombrar las columnas
df.columns = ['Unnamed', 'Precio', 'Cantidad', 'Bulto_x', 'Descripcion', 'Entrega', 'Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero']
df = df.drop(columns=['Unnamed'])

# Configurar la interfaz de Streamlit
st.title("Catálogo de Promociones")

# Mostrar los ítems del catálogo
for index, row in df.iterrows():
    st.subheader(row['Descripcion'])
    st.write(f"Precio: ${row['Precio']}")
    st.write(f"Bulto: {row['Bulto_x']}")
    st.write(f"Entrega: {row['Entrega']}")
    st.write("---")

# Agregar filtros adicionales si es necesario
