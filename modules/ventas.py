import streamlit as st
import pandas as pd
from database.connection import get_connection

def mostrar_ventas():
    st.header("🧾 Gestión de Ventas")
    tab1, tab2 = st.tabs(["➕ Nueva Venta", "📋 Historial"])

    with tab1:
        conn = get_connection()
        if not conn:
            return

        clientes  = pd.read_sql("SELECT id, nombre FROM Clientes WHERE activo=1", conn)
        productos = pd.read_sql("SELECT id, nombre, precio, stock FROM Productos WHERE activo=1 AND stock>0", conn)
        conn.close()

        if clientes.empty or productos.empty:
            st.warning("Necesitas clientes y productos registrados.")
            return

        cliente  = st.selectbox("Cliente", clientes["nombre"].tolist())
        metodo   = st.selectbox("Método de pago", ["Efectivo", "Tarjeta", "Transferencia"])

        if "carrito" not in st.session_state:
            st.session_state.carrito = []

        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            prod_sel = st.selectbox("Producto", productos["nombre"].tolist())
        with col2:
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
        with col3:
            st.write("")
            st.write("")
            if st.button("➕ Agregar"):
                prod = productos[productos["nombre"] == prod_sel].iloc[0]
                st.session_state.carrito.append({
                    "producto_id": int(prod["id"]),
                    "nombre": prod["nombre"],
                    "precio": float(prod["precio"]),
                    "cantidad": cantidad
                })

        if st.session_state.carrito:
            df_carrito = pd.DataFrame(st.session_state.carrito)
            df_carrito["subtotal"] = df_carrito["precio"] * df_carrito["cantidad"]
            st.dataframe(df_carrito[["nombre","precio","cantidad","subtotal"]], hide_index=True)

            total = df_carrito["subtotal"].sum()
            st.metric("Total", f"RD$ {total:,.2f}")

            col4, col5 = st.columns(2)
            with col4:
                if st.button("🗑️ Limpiar"):
                    st.session_state.carrito = []
                    st.rerun()
            with col5:
                if st.button("✅ Confirmar Venta", type="primary"):
                    cliente_id = int(clientes[clientes["nombre"]==cliente].iloc[0]["id"])
                    conn = get_connection()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO Ventas (cliente_id, metodo_pago, subtotal, impuesto, total) OUTPUT INSERTED.id VALUES (?,?,?,?,?)",
                            cliente_id, metodo, total, 0, total
                        )
                        venta_id = cursor.fetchone()[0]
                        for item in st.session_state.carrito:
                            cursor.execute(
                                "INSERT INTO DetalleVentas (venta_id, producto_id, cantidad, precio_unit) VALUES (?,?,?,?)",
                                venta_id, item["producto_id"], item["cantidad"], item["precio"]
                            )
                            cursor.execute("UPDATE Productos SET stock=stock-? WHERE id=?", item["cantidad"], item["producto_id"])
                        conn.commit()
                        conn.close()
                        st.success(f"🎉 Venta #{venta_id} registrada por RD$ {total:,.2f}")
                        st.session_state.carrito = []

    with tab2:
        conn = get_connection()
        if conn:
            df = pd.read_sql(
                "SELECT v.id, c.nombre AS cliente, CONVERT(VARCHAR,v.fecha,103) AS fecha, v.total, v.metodo_pago FROM Ventas v JOIN Clientes c ON v.cliente_id=c.id ORDER BY v.fecha DESC",
                conn
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
            conn.close()