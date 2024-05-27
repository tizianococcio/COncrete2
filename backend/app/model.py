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

def predict_emissions(model, input_data):
    input_data = pd.DataFrame([input_data])    
    return model.predict(input_data)[0]