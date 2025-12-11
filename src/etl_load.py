# src/etl_load.py
from sqlalchemy import create_engine
import pandas as pd
import yaml

def load_config():
    """Carga la configuración desde config.yaml."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def create_db_engine(config):
    """Crea la conexión de la DB usando SQLAlchemy (SQLite)."""
    db_name = config['database']['db_name']
    engine = create_engine(f'sqlite:///{db_name}')
    return engine

def load_data(df: pd.DataFrame, config):
    """Carga el DataFrame transformado a la base de datos."""
    engine = create_db_engine(config)
    table_name = 'road_incidents'
    
    print(f"Iniciando Carga a la tabla '{table_name}' en SQLite...")
    try:
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Carga completada. {len(df)} registros cargados.")
    except Exception as e:
        print(f"Error durante la carga a la base de datos: {e}")