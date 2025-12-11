import pandas as pd
import geopandas as gpd
from datetime import datetime

def transform_data(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Limpia, normaliza y prepara los datos para la carga."""
    print("Iniciando Transformación...")
    
    df = gdf.copy()
    
    # Normalizar nombres de columnas a minúsculas
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Mapeo de columnas y creación de ID
    df['id_incidente'] = df.get('objectid', df.get('id', df.index)).astype(str)
    
    # Manejo de Fecha/Hora
    if 'fecha' in df.columns and 'hora' in df.columns:
        
        # Combina FECHA y HORA
        temp_dt = df['fecha'].astype(str) + ' ' + df['hora'].astype(str)

        # Limpieza de hora (eliminar sufijos y puntos)
        temp_dt = temp_dt.str.lower()
        temp_dt = temp_dt.str.replace(' p. m.', '', regex=False)
        temp_dt = temp_dt.str.replace(' a. m.', '', regex=False)
        temp_dt = temp_dt.str.replace('.', '', regex=False) 
        temp_dt = temp_dt.str.strip()
        
        # Conversión a Datetime
        df['fecha_creacion'] = pd.to_datetime(
            temp_dt, 
            format='%Y-%m-%d %H:%M:%S', 
            errors='coerce' 
        )
        
        valid_dates = df['fecha_creacion'].notna()
        
        df.loc[valid_dates, 'fecha'] = df.loc[valid_dates, 'fecha_creacion'].dt.normalize()
        df.loc[valid_dates, 'hora'] = df.loc[valid_dates, 'fecha_creacion'].dt.time
        
        # Mapeo a Español para el día de la semana
        day_map = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        df.loc[valid_dates, 'dia_semana'] = df.loc[valid_dates, 'fecha_creacion'].dt.day_name().map(day_map)
        
    else:
        df['fecha'] = None
        df['hora'] = None
        df['dia_semana'] = None


    # Limpieza y Conversión de campos numéricos
    df['lesionados'] = pd.to_numeric(df.get('heridos', pd.Series(0)), errors='coerce').fillna(0).astype(int)
    df['muertos'] = pd.to_numeric(df.get('muertos', pd.Series(0)), errors='coerce').fillna(0).astype(int)
    df['vehiculos_involucrados'] = 0 
    
    # Limpieza de texto y mapeo de nombres
    df['tipo_incidente'] = df.get('tipo', pd.Series('SIN ESPECIFICAR')).fillna('SIN ESPECIFICAR').str.strip().str.upper()
        
    # Creación de la columna 'calle' 
    df['calle_1'] = df.get('calle_1', pd.Series('')).fillna('').astype(str).str.strip()
    df['calle_2'] = df.get('calle_2', pd.Series('')).fillna('').astype(str).str.strip()
    
    df['calle'] = df.apply(
        lambda row: f"{row['calle_1']} y {row['calle_2']}" if row['calle_2'] else row['calle_1'],
        axis=1
    ).str.strip().replace('', 'SIN DATOS') 
    
    # Extracción de Coordenadas
    df['longitud'] = df.geometry.x
    df['latitud'] = df.geometry.y
    
    # Crear placeholders y Seleccionar
    df['delegacion'] = df.get('delegacion', pd.Series('SIN DATOS')).fillna('SIN DATOS').astype(str)
    df['colonia'] = df.get('colonia', pd.Series('SIN DATOS')).fillna('SIN DATOS').astype(str)
    df['tipo_hecho'] = df.get('tipo_hecho', df['tipo_incidente']).astype(str) 

    # Columna ESTADO
    df['estado'] = df.get('estado', pd.Series('DESCONOCIDO')).fillna('DESCONOCIDO').astype(str).str.strip().str.upper() 

    # Columna TIPO_ENERV (AGRAVANTE)
    df['tipo_enerv'] = df.get('tipo_enerv', pd.Series('NINGUNO')).fillna('NINGUNO').astype(str).str.strip().str.upper() 
    
    # Seleccionar y ordenar las columnas finales
    cols_to_select = [
        'id_incidente', 'fecha', 'hora', 'dia_semana', 'tipo_incidente',
        'longitud', 'latitud', 'delegacion', 'colonia', 'calle', 
        'tipo_hecho', 'tipo_enerv', 'estado', 
        'lesionados', 'muertos', 'vehiculos_involucrados'
    ]
    
    final_df = df[cols_to_select].copy()

    print(f"Transformación completada. Filas procesadas: {len(final_df)}.")
    return final_df
