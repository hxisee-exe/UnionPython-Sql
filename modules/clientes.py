import streamlit as st
import pandas as pd
from database.connection import get_connection

def mostrar_clientes():
    st.header("👥 Gestión de Clientes")
    tab1, tab2 = st.tabs(["📋 Lista", "➕ Nuevo Cliente"])

    with tab1:
        conn = get_connection()
        if conn:
            df = pd.read_sql("SELECT id, nombre, telefono, email FROM Clientes WHERE activo=1", conn)
            st.dataframe(df, use_container_width=True, hide_index=True)
            conn.close()

    with tab2:
        with st.form("nuevo_cliente", clear_on_submit=True):
            nombre   = st.text_input("Nombre *")
            telefono = st.text_input("Teléfono")
            email    = st.text_input("Email")
            if st.form_submit_button("💾 Guardar"):
                if nombre:
                    conn = get_connection()
                    if conn:
                        conn.cursor().execute(
                            "INSERT INTO Clientes (nombre, telefono, email) VALUES (?,?,?)",
                            nombre, telefono, email
                        )
                        conn.commit()
                        conn.close()
                        st.success("✅ Cliente guardado")
                else:
                    st.error("El nombre es obligatorio")