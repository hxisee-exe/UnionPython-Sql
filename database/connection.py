import pyodbc
import streamlit as st

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=SistemaVentas;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        return conn
    except Exception as e:
        st.error(f"Error de conexion: {e}")
        return None