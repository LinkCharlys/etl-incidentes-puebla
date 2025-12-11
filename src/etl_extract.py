
import geopandas as gpd
import yaml
import os

def load_config():
    """Carga la configuración desde config.yaml."""
    
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def extract_data(config):
    """Lee el GeoJSON local en un GeoDataFrame."""
    source_file = config['data_source']
    
    os.makedirs('data', exist_ok=True) # Crea la carpeta data/ si no existe
    
    print(f"Leyendo datos desde: {source_file}")
    try:
        # 1. Lectura del GeoJSON en GeoDataFrame
        gdf = gpd.read_file(source_file)
        print(f"Datos extraídos: {len(gdf)} registros.")
        return gdf
    except Exception as e:
        print(f"Error durante la extracción: {e}")
        return None