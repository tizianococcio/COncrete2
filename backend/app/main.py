from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from model import load_model, predict_emissions
from optimizer import optimize_parameters

app = FastAPI()

class InputParameters(BaseModel):
    temperature: float  # degrees Celsius
    humidity: float  # percentage (%)
    curing_time: float  # hours
    energy_consumption: float  # kilowatt-hours (kWh)
    amount_produced_m3: float  # cubic meters (m³)
    dosing_events: int  # Number of dosing events
    active_power_curve: float  # watts (W)
    truck_drum_rotation_speed: float  # rotations per minute (rpm)
    truck_drum_duration: float  # minutes
    cement: float  # kg
    sand: float  # kg
    gravel: float  # kg

model = load_model()

@app.post("/predict")
def predict(params: InputParameters):
    try:
        input_data = np.array([[params.temperature, params.humidity, params.curing_time, params.energy_consumption,
                                params.amount_produced_m3, params.dosing_events, params.active_power_curve,
                                params.truck_drum_rotation_speed, params.truck_drum_duration, params.cement,
                                params.sand, params.gravel]])
        prediction = predict_emissions(model, input_data)
        return {"predicted_co2_emissions": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/getoptimal")
def get_optimal():
    try:
        optimal_params, co2_emissions = optimize_parameters(model)
        return {
            "optimal_parameters": optimal_params,
            "expected_co2_emissions": co2_emissions
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
