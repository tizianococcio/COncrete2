from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from typing import Optional, Dict, Any
import asyncio
from kafka import KafkaConsumer
import json
import config
from config import InputParameters
from model import load_model, predict_emissions
from optimizer import CO2Optimizer
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Access environment variables with defaults
host = os.getenv('KAFKA_HOST')
user = os.getenv('KAFKA_USER')
pwd = os.getenv('KAFKA_PWD')
sasl_mechanism = os.getenv('SASL_MECHANISM')
security_protocol = os.getenv('SECURITY_PROTOCOL')

app = FastAPI()
model = load_model()

def create_kafka_consumer() -> KafkaConsumer:
    """
    Create and configure a Kafka consumer.
    
    Returns:
        KafkaConsumer: Configured Kafka consumer.
    """
    return KafkaConsumer(
        'concrete_production_data',
        bootstrap_servers=host,
        sasl_mechanism=sasl_mechanism,
        security_protocol=security_protocol,
        sasl_plain_username=user,
        sasl_plain_password=pwd,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

async def kafka_event_generator(consumer: KafkaConsumer):
    """
    Generate events from Kafka consumer.
    
    Yields:
        dict: A dictionary containing the event type and data as a JSON string.
    """    
    try:
        for message in consumer:
            prediction = predict_emissions(model, message.value)
            message.value['predicted_co2'] = prediction
            yield {
                "event": "new_data",
                "data": json.dumps(message.value)
            }
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.error(f"Error in kafka_event_generator: {e}")
    finally:
        consumer.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connection and send data.
    
    Args:
        websocket (WebSocket): The WebSocket connection instance.
    """
    await websocket.accept()
    consumer = create_kafka_consumer()
    try:
        async for message in kafka_event_generator(consumer):
            await websocket.send_json(message)
    except WebSocketDisconnect:
        logger.info("WebSocket connection was disconnected")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")

@app.get("/units")
def get_units() -> Dict[str, Any]:
    return config.get_units()

@app.post("/predict")
def predict(params: InputParameters) -> Dict[str, Any]:
    """
    Predict CO2 emissions based on input parameters.
    
    Args:
        params (InputParameters): Input parameters for prediction.
        
    Returns:
        dict: A dictionary containing the predicted CO2 emissions.
        
    Raises:
        HTTPException: If prediction fails.
    """
    try:
        data = params.dict() # Check if order is preserved!
        prediction = predict_emissions(model, data)
        return {"predicted_co2_emissions": prediction}
    except Exception as e:
        logger.error(f"Error in /predict: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/getoptimal")
def get_optimal(temperature: Optional[float] = Query(None)) -> Dict[str, Any]:
    """
    Get optimal parameters for CO2 emissions.
    
    Args:
        temperature (Optional[float]): Optional temperature value to fix during optimization.
        
    Returns:
        dict: A dictionary containing the optimal parameters and expected CO2 emissions.
        
    Raises:
        HTTPException: If optimization fails.
    """
    try:
        optimizer = CO2Optimizer(model)
        if temperature:
            optimizer.set_fixed_param('temperature', temperature)
        optimal_inputs, co2_emissions = optimizer.optimize('differential_evolution')
        return {
            "optimal_parameters": optimal_inputs,
            "expected_co2_emissions": co2_emissions
        }
    except Exception as e:
        logger.error(f"Error in /getoptimal: {e}")
        raise HTTPException(status_code=400, detail=str(e))