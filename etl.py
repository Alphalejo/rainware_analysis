import os
import pandas as pd
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine, text
from sklearn.metrics import mean_absolute_error
import joblib

import utils.toolbox as toolbox


if __name__ == "__main__":

    # ===== 0. Configuracion logging =====
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='etl.log',  # Guarda los logs en el archivo etl.log
    filemode='w'         # 'w' para sobrescribir
    )


    # ===== 1. Cargar variables de entorno =====
    load_dotenv()

    LOCAL_USER = os.getenv("PG_USER")
    LOCAL_PASSWORD = os.getenv("PG_PASSWORD")
    LOCAL_HOST = os.getenv("PG_HOST")
    LOCAL_PORT = os.getenv("PG_PORT")
    LOCAL_DB = os.getenv("PG_DB")

    SUPA_USER = os.getenv("SUPABASE_USER")
    SUPA_PASSWORD = os.getenv("SUPABASE_PASSWORD")
    SUPA_HOST = os.getenv("SUPABASE_HOST")
    SUPA_PORT = os.getenv("SUPABASE_PORT", 5432)
    SUPA_DB = os.getenv("SUPABASE_DB")

    # ===== 2. Crear conexión a Supabase/PostgreSQL =====
    logging.info("[INFO] Conectando a la base de datos Local y Supabase...")
    try:
        engine_local = create_engine(
            f"postgresql+psycopg2://{LOCAL_USER}:{LOCAL_PASSWORD}@{LOCAL_HOST}:{LOCAL_PORT}/{LOCAL_DB}"
        )
        logging.info("[OK] Conectado a la base de datos Local de forma exitosam.")
    except Exception as e:
        logging.error(f"[ERROR] No se pudo conectar a la base de datos local: {e}")
        raise

    try:
        # Crear conexión a PostgreSQL en Supabase usando IPv4
        engine_supabase = create_engine(
            f"postgresql+psycopg2://{SUPA_USER}:{SUPA_PASSWORD}@{SUPA_HOST}:{SUPA_PORT}/{SUPA_DB}"
        )
        logging.info("[OK] Conectado a la base de datos SupaBase de forma exitosa.")
    except Exception as e:
        logging.error(f"[ERROR] No se pudo conectar a la base de datos SupaBase: {e}")
        

    # ===== 3. Cargar datos de entrada =====
    logging.info("[INFO] Cargando datos de entrada...")
    
    try:
        df_sales = pd.read_csv("./data/sales.csv")
    except FileNotFoundError:
        logging.error("[ERROR] No se encontró el archivo sales.csv.")
        raise

    # Llamamos la toolbox de Open-Meteo para obtener los datos de las temperaturas diarias
    temperatures = toolbox.get_data()

    # Convirtiendo la data en un dataframe
    df_weather= pd.DataFrame({
        "date": pd.to_datetime(temperatures["time"]),
        "temp_max": temperatures["temperature_2m_max"],
        "temp_min": temperatures["temperature_2m_min"]
    })

    # Creando una columna para la temperatura promedio del dia
    df_weather["temperature"] = ((df_weather["temp_max"] + df_weather["temp_min"]) / 2).round(1)


    # ===== 4. Procesando datos de entrada =====
    # Convirtiendo la columna date en tipo datetime
    logging.info("[INFO] Procesando datos de entrada...")
    df_sales["date"] = pd.to_datetime(df_sales["date"])
    df_weather["date"] = pd.to_datetime(df_weather["date"])

    # Formateando la fecha en df_weather
    df_weather["date"] = df_weather["date"].dt.strftime("%m/%d/%Y")
    df_weather["date"] = pd.to_datetime(df_weather["date"])

    # Unir ventas + clima
    df_final = pd.merge(df_sales, df_weather[["date", "temperature"]], on="date", how="left")

    df_modelo = toolbox.preprocessing(df_final.copy()) 
    X = df_modelo
    y = df_final["sales"]

    # ===== 4. Cargar modelos entrenados =====
    logging.info("[INFO] Cargando modelos...")

    try:
        xgb_model = joblib.load("./models/xgb_model.joblib")
        lr_model = joblib.load("./models/lr_model.joblib")
    except FileNotFoundError as e:
        logging.error(f"[ERROR] No se encontró el archivo del modelo: {e}")
        raise

    # ===== 5. Evaluar modelos =====
    logging.info("[INFO] Evaluando modelos...")
    mae_xgb = mean_absolute_error(y, xgb_model.predict(X))
    mae_lr = mean_absolute_error(y, lr_model.predict(X))

    logging.info(f"MAE XGBoost: {mae_xgb:.4f}")
    logging.info(f"MAE Linear Regression: {mae_lr:.4f}")

    # ===== 6. Seleccionar mejor modelo y generar predicciones =====
    logging.info("[INFO] Seleccionando mejor modelo...")
    if mae_xgb < mae_lr:
        logging.info("[OK] Usando XGBoost para predicciones finales.")
        df_final["sales_prediction"] = xgb_model.predict(X)
    else:
        logging.info("[OK] Usando Regresión Lineal para predicciones finales.")
        df_final["sales_prediction"] = lr_model.predict(X)

    # ===== 7. Leer queries SQL =====
    logging.info("[INFO] Leyendo queries.sql...")
    with open("./utils/queries.sql", "r", encoding="utf-8") as f:
        queries = [q.strip() for q in f.read().split(";") if q.strip()]

    # queries[0] = CREATE TABLE
    # queries[1] = Error Medio
    create_table_query = queries[0]

    # ===== 8. Crear tabla en la base de datos =====
    logging.info("[INFO] Creando tabla si no existe...")

    try:
        with engine_local.begin() as conn:
            conn.execute(text(create_table_query))
        logging.info("[OK] tabla creada en PostgreSQL local exitosamente.")
    except Exception as e:
        logging.error(f"[ERROR] No se pudo crear la tabla en PostgreSQL local: {e}")

    try:
        with engine_supabase.begin() as conn2:
            conn2.execute(text(create_table_query))
        logging.info("[OK] tabla creada en PostgreSQL SupaBase exitosamente.")
    except Exception as e:
        logging.error(f"[ERROR] No se pudo crear la tabla en PostgreSQL SuPabase: {e}")


    # ===== 9. Subir predicciones a la base de datos =====
    logging.info("[INFO] Subiendo predicciones a la base de datos...")
    df_final.to_sql("sales_predictions", engine_local, if_exists="append", index=False)
    logging.info("[OK] Predicciones subidas a PostgreSQL local.")

    df_final.to_sql("sales_predictions", engine_supabase, if_exists="append", index=False)
    logging.info("[OK] Predicciones subidas a PostgreSQL SupaBase.")

    # ===== 10. (Opcional) Verificar subida =====
    logging.info("[INFO] Verificando registros en la tabla...")
    with engine_local.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM sales_predictions"))
        logging.info(f"[OK] Registros en tabla local: {result.scalar()}")

    with engine_supabase.connect() as conn2:
        result = conn2.execute(text("SELECT COUNT(*) FROM sales_predictions"))
        logging.info(f"[OK] Registros en tabla respaldo: {result.scalar()}")

    logging.info("[OK] Proceso finalizado.")
