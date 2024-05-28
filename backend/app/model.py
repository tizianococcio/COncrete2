import os
import joblib
import pandas as pd
from typing import Optional, Dict, Any
from config import get_default_parameters
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model() -> Optional[Any]:
    """
    Load the pre-trained model from a .pkl file.
    
    Returns:
        Optional[Any]: The loaded model, or None if the model file does not exist.
    """
    model_path = os.path.join(os.getcwd(), "model", "model.pkl")
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            logger.error("Error loading model: %s", e)
            return None
    else:
        logger.warning("Model file not found at %s", model_path)
        return None

def predict_emissions(model: Any, input_data: Dict[str, Any]) -> float:
    """
    Predict CO2 emissions based on input data using the loaded model.
    
    Args:
        model (Any): The pre-trained model.
        input_data (Dict[str, Any]): A dictionary with input parameters for the prediction.
        
    Returns:
        float: The predicted CO2 emissions.
    """
    if model is None:
        logger.error("No model is loaded. Prediction cannot be performed.")
        raise ValueError("Model not loaded")    
    data = get_default_parameters()
    data.update(input_data)

    try:
        input_data = pd.DataFrame([data])    
        prediction = model.predict(input_data)[0]
        return prediction
    except Exception as e:
        logger.error("Error making prediction: %s", e)
        raise