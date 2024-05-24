import joblib
import numpy as np

def load_model():
    # Load the pre-trained model
    model = joblib.load("../../model.pkl")
    return model

def predict_emissions(model, input_data):
    return model.predict(input_data)[0]