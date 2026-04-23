from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("catboost_model.pkl")
columns = joblib.load("model_columns.pkl")

class InputData(BaseModel):
    battery_kwh: float
    range_km: float
    charging_time_hr: float
    motor_power_kw: float
    weight_kg: float
    top_speed_kmph: float
    load_carrying_capacity: float
    underseat_storage: str        # "yes" or "no"
    usb_charging_port: str        # "yes" or "no"
    anti_theft_alarm: str         # "yes" or "no"

@app.post("/predict")
def predict(data: InputData):
    d = data.dict()

    # Derived features
    d["performance_score"] = round(
        d["range_km"] * 0.4 + d["motor_power_kw"] * 20 + d["top_speed_kmph"] * 0.3, 2
    )
    d["power_to_weight"] = d["motor_power_kw"] / d["weight_kg"] if d["weight_kg"] else 0
    d["price_per_km"] = 0  # circular — unknown at prediction time

    # usage_type
    if d["motor_power_kw"] > 6:
        d["usage_type"] = 1
    elif d["range_km"] < 100:
        d["usage_type"] = 2
    elif d["range_km"] < 180:
        d["usage_type"] = 3
    else:
        d["usage_type"] = 4

    # One-hot: underseat_storage, usb, alarm
    d["underseat_storage_yes"] = 1 if d["underseat_storage"] == "yes" else 0
    d["usb_charging_port_yes"] = 1 if d["usb_charging_port"] == "yes" else 0
    d["anti_theft_alarm_yes"]  = 1 if d["anti_theft_alarm"] == "yes" else 0

    # One-hot: rating (e.g. rating_4.2 = 1)

    # Remove raw string fields not in model columns
    for key in ["underseat_storage", "usb_charging_port", "anti_theft_alarm"]:
        d.pop(key)

    df = pd.DataFrame([d])

    # Set rating one-hot

    # Align to model columns
    df = df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(df)[0]
    return {"predicted_price": float(prediction)}