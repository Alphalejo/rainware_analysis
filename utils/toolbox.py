import requests
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def get_data():
    
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    
    # Suponiendo que la empresa esta ubicada en bogota
    params = {
        "latitude": 4.6097,
        "longitude": -74.0817,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "America/Bogota"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Acceder a los datos diarios
        daily_data = data["daily"]

        return daily_data

    except requests.RequestException as e:
        return {"error": f"Error al obtener datos: {e}"}
    


def preprocessing(df):
    
    # === Procesar columna date ===
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    # === Codificar category ===
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    category_encoded = encoder.fit_transform(df[["category"]])
    category_df = pd.DataFrame(category_encoded, columns=encoder.get_feature_names_out(["category"]))
    df = pd.concat([df, category_df], axis=1)

    # === Variables y target ===
    feature_cols = ["temperature", "price", "day_of_week", "month", "day_of_year"] + list(category_df.columns)
    X = df[feature_cols]

    return X