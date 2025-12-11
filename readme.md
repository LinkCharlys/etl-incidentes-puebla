
# 📄 README.md: Proyecto ETL y Dashboard de Incidentes de Tránsito

## 🚗 Análisis de Incidentes de Tránsito en Puebla, México

### Descripción del Proyecto

Este proyecto implementa un *pipeline* de Extracción, Transformación y Carga (**ETL**) para procesar datos **geoespaciales** de incidentes de tránsito en la ciudad de Puebla, correspondientes a junio de 2021. Los datos son limpiados, normalizados y cargados en una base de datos **SQLite**. Posteriormente, se utiliza una aplicación interactiva desarrollada con **Streamlit** para visualizar las métricas clave, la distribución geográfica (mapa) y el análisis de los incidentes por colonia.

**Tecnologías Clave:** Python, Pandas, **GeoPandas**, SQLAlchemy, Streamlit.

-----

## 📦 Estructura del Repositorio y Entregables

El repositorio está organizado profesionalmente para separar el código, la configuración y los datos fuente.

| Carpeta/Archivo | Contenido |
| :--- | :--- |
| `src/` | Contiene el código fuente de Python (ETL y Dashboard). |
| `config/` | Contiene el archivo de configuración (`config.yaml`).|
| `data/` | Contiene el archivo GeoJSON de la fuente de datos.|
| `requirements.txt` | Lista de dependencias necesarias.|
| `incidents.db` | Base de datos SQLite (Generada por el pipeline).|
| `README.md` | Este documento.|

### Código Fuente (Detalle)

  * `src/orchestrator.py`: Script principal para la ejecución del pipeline.
  * `src/etl_extract.py`: Función para cargar los datos GeoJSON.
  * `src/etl_transform.py`: Lógica de limpieza, normalización y creación de campos de análisis.
  * `src/etl_load.py`: Función para cargar el DataFrame transformado a la base de datos.
  * `src/dashboard.py`: Aplicación Streamlit para la visualización de datos.

-----

## 🚀 Instrucciones de Uso

Para replicar y ejecutar el proyecto, siga los siguientes pasos:

### 1\. Preparación del Entorno

Asegúrese de tener Python (versión 3.8+) instalado. Clone el repositorio y navegue al directorio raíz.

#### ⚠️ Instalación y Activación del Entorno Geoespacial

Este proyecto utiliza **GeoPandas**. Si ya tienes el entorno Conda llamado `etl-geo`, ¡actívalo primero\!

```bash
conda activate etl-geo
```

Si aún no has creado el entorno, la forma más estable de instalar las dependencias geoespaciales es:

```bash
conda create -n etl-geo python=3.9
conda activate etl-geo
conda install -c conda-forge geopandas
```

Una vez que el entorno esté activo, instale el resto de las librerías del proyecto:

```bash
# Instalar dependencias restantes (pandas, streamlit, sqlalchemy, etc.)
pip install -r requirements.txt
```

### 2\. Crear y Configurar la Base de Datos

La base de datos se crea automáticamente al ejecutar el pipeline por primera vez.

#### Esquema de la Tabla (SQL)

La tabla `road_incidents` en la base de datos `incidents.db` utiliza el siguiente esquema:

```sql
-- Esquema de la tabla road_incidents
CREATE TABLE IF NOT EXISTS road_incidents (
    id_incidente TEXT PRIMARY KEY,
    fecha DATETIME,
    hora TEXT,
    dia_semana TEXT,
    tipo_incidente TEXT,
    longitud REAL,
    latitud REAL,
    delegacion TEXT,
    colonia TEXT,
    calle TEXT,
    tipo_hecho TEXT,
    tipo_enerv TEXT,
    estado TEXT,
    lesionados INTEGER,
    muertos INTEGER,
    vehiculos_involucrados INTEGER
);
```

### 3\. Correr el Pipeline (ETL)

Con el entorno `(etl-geo)` activo, ejecute el orquestador:

```bash
python src/orchestrator.py
```

### 4\. Lanzar el Dashboard

Con el entorno activo:

```bash
streamlit run src/dashboard.py
```

-----

## 🖼️ Capturas de Pantalla del Dashboard

### Vista General y Filtros

El dashboard inicia con los filtros vacíos y muestra las métricas clave, el mapa de incidentes y el gráfico de colonias.

### Análisis de Distribución

El gráfico de Top 10 Colonias se muestra con un ancho considerable, permitiendo una fácil identificación de las zonas con mayor concentración de incidentes.

-----
