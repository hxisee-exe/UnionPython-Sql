import streamlit as st
import pandas as pd
from database.connection import get_connection

def mostrar_inventario():
    st.header("📦 Gestión de Inventario")
    tab1, tab2 = st.tabs(["📋 Productos", "➕ Nuevo Producto"])

    with tab1:
        conn = get_connection()
        if conn:
            df = pd.read_sql("SELECT id, nombre, precio, stock FROM Productos WHERE activo=1", conn)
            st.dataframe(df, use_container_width=True, hide_index=True)
            conn.close()

    with tab2:
        with st.form("nuevo_producto", clear_on_submit=True):
            nombre  = st.text_input("Nombre *")
            precio  = st.number_input("Precio", min_value=0.0, step=0.50)
            stock   = st.number_input("Stock", min_value=0, step=1)
            if st.form_submit_button("💾 Guardar"):
                if nombre:
                    conn = get_connection()
                    if conn:
                        conn.cursor().execute(
                            "INSERT INTO Productos (nombre, precio, stock, stock_minimo) VALUES (?,?,?,5)",
                            nombre, precio, stock
                        )
                        conn.commit()
                        conn.close()
                        st.success("✅ Producto guardado")
                else:
                    st.error("El nombre es obligatorio")