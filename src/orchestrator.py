# src/etl_extract.py
import geopandas as gpd

def extract_data(config: dict):
    """Carga el archivo GeoJSON desde la ruta especificada en la configuración."""
    
    try:
        # Extraer la ruta usando la clave 'data_file' de tu config.yaml
        geojson_path = config['data_file']
        
        # Cargar los datos geoespaciales
        gdf = gpd.read_file(geojson_path)
        
        print(f"Datos cargados exitosamente desde: {geojson_path}")
        print(f"Total de registros cargados: {len(gdf)}")
        return gdf
        
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado en la ruta: {geojson_path}")
        print("Asegúrese de que el archivo GeoJSON esté en el directorio correcto y el config.yaml sea correcto.")
        return None
    except Exception as e:
        print(f"ERROR durante la extracción: {e}")
        return None