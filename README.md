# rainware_analysis

## Descripcion
Una empresa minorista de ropa para lluvia desea predecir ventas futuras y analizar tendencias de productos. El candidato debe implementar un flujo de datos que incluya ETL, almacenamiento en Postgres, respaldo en Supabase y un tablero interactivo.

## Esquema del Proyecto

```
sales_prediction_project/
├── data/                   # Archivos de entrada (CSV de ventas)
├── models/                 # Modelos de predicción entrenados y scripts asociados
├── utils/                  # Funciones auxiliares
│   ├── queries.sql         # Queries necesarias usadas en el proyecto principal
│   ├── toolbox.py          # Funciones usadas en el proyecto principal
├── draft_analysis.ipynb    # Exploración inicial y análisis preliminar
├── etl.log                 # Registro de ejecución del proceso ETL
├── etl.py                  # Script principal del pipeline ETL
├── README.md               # Documentación técnica del proyecto
├── requirements.txt        # Lista de dependencias del entorno virtual
└── .env.example            # Variables de entorno necesarias (API key, DB URL, etc.)```

## Como ejecutar el proyecto

### 1. Descomprimir la carpeta
Aqui encontrara el esquema anteriormente mencionado tambien puede descargar el repositorio de github https://github.com/Alphalejo/rainware_analysis

### 2. Crear y activar el entorno virtual
Cree y ejecute un entorno virtual


```python
python -m venv venv
source venv/bin/activate  # En Linux/Mac
.\venv\Scripts\activate   # En Windows```


### 3. Instalar Dependencias
El archivo requirement.txt contiene las librerias y archivos necesarion para el proyecto.

Con el siguiente codigo puede instalar todas las dependencias
```python
pip install -r requirements.txt```

### 4. Configurar variables de entorno
Crea un archivo .env basado en .env.example con las credenciales

### 5. Ejecutar el pipeline ETL
esto ejecutara la extraccion, procesamiento necesario de datos, hara la prediccion de ventas, se conectara, creara las tablas en PostgreSQL local y en Supabase y cargara los datos ya procesados.

```python
python etl.py```


## Notas:
- Algunas funciones necesarias, asi como los queries en SQL estan en archivos aparte en la carpeta toolbox para simplificar el codigo y facilitar la reutilizacion de estos recursos.
- El archivo draft_analysis.ipynb no es para produccion, se dejo unicamente con objetivos ilustrativos para ver el proceso que se siguio analizando variables y haciendo un EDA que no es necesario para el codigo final de ejecución.

## Dashboard
El dashboard generado en looker studio puede verlo en el siguiente link publico
https://lookerstudio.google.com/u/0/reporting/e0eec297-cb0c-4f13-98aa-4bd51893089f/page/EegUF