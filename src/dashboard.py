import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import yaml
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Incidentes Puebla")

# --- FUNCIONES ---
def load_config():
    """Carga la configuración del proyecto."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

# Función para crear el motor de BD
def create_db_engine():
    config = load_config()
    db_name = config['database']['db_name']
    return create_engine(f'sqlite:///{db_name}')

# Función para cargar datos (Usando caché, ignorando el motor con '_engine')
@st.cache_data
def load_data_from_database(_engine): 
    """Carga los datos desde SQLite usando el motor."""
    
    query = text("SELECT * FROM road_incidents")
    df = pd.read_sql(query, _engine)
    
    # Limpiar tipos de datos
    df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
    df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
    
    # Conversión a datetime para ordenamiento y gráficos
    df['fecha'] = pd.to_datetime(df['fecha']) 
    df['fecha_corta'] = df['fecha'].dt.strftime('%d/%m/%Y')
    
    return df

# --- APLICACIÓN PRINCIPAL ---
try:
    st.title("🚗 Incidentes de Tránsito en Puebla (Junio 2021)")
    st.markdown("Datos cargados desde la base de datos SQLite.")

    # 1. Cargar Datos
    engine = create_db_engine()
    df = load_data_from_database(engine)

    # Manejo de datos si están vacíos
    if df.empty:
        st.warning("⚠️ La base de datos está vacía. Ejecute el pipeline ETL primero:")
        st.code("python src/orchestrator.py")
        st.stop()
    
    # --- SIDEBAR FILTROS ---
    st.sidebar.header("🔍 Filtros")
    
    tipos = sorted(df['tipo_incidente'].unique().tolist())
    
    tipo_seleccionado = st.sidebar.multiselect(
        "Tipo de Incidente", 
        tipos, 
        default=[] # <--- FILTRO INICIA VACÍO
    )
    
    # Aplicar filtros
    if tipo_seleccionado:
        df_filtrado = df[df['tipo_incidente'].isin(tipo_seleccionado)]
    else:
        # Si no hay nada seleccionado, usamos el DataFrame completo
        df_filtrado = df.copy() 
    
    st.success(f"📊 Mostrando {len(df_filtrado):,} de {len(df):,} incidentes.")

    # --- MÉTRICAS ---
    st.header("📈 Estadísticas Clave")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Incidentes", f"{len(df_filtrado):,}")
    col2.metric("Lesionados", f"{int(df_filtrado['lesionados'].sum()):,}")
    col3.metric("Muertos", f"{int(df_filtrado['muertos'].sum()):,}")
    
    st.divider()
    
    # --- MAPA ---
    st.header("🗺️ Localización de Incidentes")
    
    df_mapa = df_filtrado.dropna(subset=['latitud', 'longitud']).copy()
    
    if not df_mapa.empty:
        map_data = df_mapa[['latitud', 'longitud']].rename(
            columns={'latitud': 'lat', 'longitud': 'lon'}
        )
        st.map(map_data, zoom=11)
        st.caption(f"📍 Mostrando {len(df_mapa):,} incidentes con coordenadas válidas")
    else:
        st.warning("No hay datos geográficos disponibles con los filtros actuales.")
        
    st.divider()
        
    # --- GRÁFICOS ---
    st.header("📊 Análisis de Distribución")
    # Dividimos en dos columnas (50/50)
    col_left, col_right = st.columns(2)
    
    # Gráfico 1: Top Colonias (Ocupa la columna izquierda, 50% del ancho)
    with col_left:
        st.subheader("Top 10 Colonias")
        top_colonias = df_filtrado['colonia'].value_counts().head(10).sort_values(ascending=True)
        
        if not top_colonias.empty:
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            top_colonias.plot(kind='barh', ax=ax1, color='teal')
            ax1.set_title('Incidentes por Colonia', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Número de Incidentes')
            plt.tight_layout()
            st.pyplot(fig1)
        else:
            st.info("No hay datos disponibles.")
            
    # --- TABLA DE DATOS ---
    st.divider()
    st.header("📋 Datos Detallados")
    
    if st.checkbox("Mostrar tabla de datos"):
        
        # Ordenamiento por fecha descendente (más recientes primero)
        df_ordenado = df_filtrado.sort_values(by='fecha', ascending=False)

        # Definir columnas a mostrar
        cols_display = [
            'estado', 
            'tipo_enerv', 
            'tipo_incidente', 
            'colonia', 
            'calle', 
            'lesionados', 
            'muertos'
        ] 
        
        # Mostrar DataFrame
        st.dataframe(
            df_ordenado[cols_display].head(100), 
            use_container_width=True,
            hide_index=True,
            column_config={
                "tipo_enerv": "Agravante",
                "estado": "Estado del Caso"
            }
        )
        st.caption(f"Mostrando primeras 100 filas de {len(df_ordenado):,} registros (Ordenado por fecha más reciente).")
        
except Exception as e:
    st.error(f"❌ Ocurrió un error. Detalle: {str(e)}")
    st.info("Asegúrese de haber ejecutado 'python src/orchestrator.py' para cargar los datos más recientes.")