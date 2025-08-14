# rainware_analysis

## Descripcion
Una empresa minorista de ropa para lluvia desea predecir ventas futuras y analizar tendencias de productos. El candidato debe implementar un flujo de datos que incluya ETL, almacenamiento en Postgres, respaldo en Supabase y un tablero interactivo.

## Esquema del Proyecto

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
└── .env.example            # Variables de entorno necesarias (API key, DB URL, etc.)

## Como ejecutar el proyecto

### 1. Descomprimir la carpeta
Aqui encontrara el esquema anteriormente mencionado

### 2. Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate  # En Linux/Mac
.\venv\Scripts\activate   # En Windows