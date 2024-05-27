import joblib
import os
import pandas as pd

def load_model():
    # Load the pre-trained model
    model_path = os.path.join(os.getcwd(), "model", "model.pkl")
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        return None
    return model

def get_default():
    return {
        'temperature': 15,  # degrees Celsius
        'humidity': 30,  # percentage (%), default 60
        'curing_time': 18,  # hours
        'energy_consumption': 105,  # kilowatt-hours (kWh)
        'amount_produced_m3': 1,
        'dosing_events': 2,  # Number of dosing events
        'active_power_curve': 105,  # watts (W)
        'truck_drum_rotation_speed': 11,  # rotations per minute (rpm)
        'truck_drum_duration': 22,  # minutes
        'cement': 300,  # kg
        'sand': 580,  # kg
        'gravel': 1020  # kg
    }    

def predict_emissions(model, input_data):
    data = get_default()
    data.update(input_data)
    input_data = pd.DataFrame([data])    
    return model.predict(input_data)[0]