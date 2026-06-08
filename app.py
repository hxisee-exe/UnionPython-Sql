import streamlit as st
from modules.clientes import mostrar_clientes
from modules.inventario import mostrar_inventario
from modules.ventas import mostrar_ventas

st.set_page_config(page_title="Sistema de Ventas", page_icon="🛒", layout="wide")

with st.sidebar:
    st.title("🛒 SistemaVentas")
    st.caption("Versión 1.0")
    st.divider()
    pagina = st.radio("Menu", ["🏠 Inicio", "👥 Clientes", "📦 Inventario", "🧾 Ventas"], label_visibility="collapsed")
    st.divider()
    st.caption("Python + SQL Server")

if pagina == "🏠 Inicio":
    st.title("🏠 Panel Principal")
    st.markdown("Bienvenido al **Sistema de Ventas**.")

    from database.connection import get_connection
    import pandas as pd

    conn = get_connection()
    if conn:
        col1, col2, col3 = st.columns(3)
        ventas = pd.read_sql("SELECT COUNT(*) AS n, ISNULL(SUM(total),0) AS t FROM Ventas WHERE CAST(fecha AS DATE)=CAST(GETDATE() AS DATE)", conn).iloc[0]
        clientes = pd.read_sql("SELECT COUNT(*) AS n FROM Clientes WHERE activo=1", conn).iloc[0]
        productos = pd.read_sql("SELECT COUNT(*) AS n FROM Productos WHERE activo=1 AND stock<=stock_minimo", conn).iloc[0]
        col1.metric("Ventas hoy", int(ventas["n"]))
        col2.metric("Ingresos hoy", f"RD$ {float(ventas['t']):,.2f}")
        col3.metric("⚠️ Stock bajo", int(productos["n"]))
        conn.close()

elif pagina == "👥 Clientes":
    mostrar_clientes()

elif pagina == "📦 Inventario":
    mostrar_inventario()

elif pagina == "🧾 Ventas":
    mostrar_ventas()