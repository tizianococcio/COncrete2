from fastapi import FastAPI, HTTPException, WebSocket
import asyncio
from kafka import KafkaConsumer
import json

from pydantic import BaseModel
import numpy as np
from model import load_model, predict_emissions
from optimizer import optimize_parameters

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
host = os.getenv('KAFKA_HOST')
user = os.getenv('KAFKA_USER')
pwd = os.getenv('KAFKA_PWD')
sasl_mechanism = os.getenv('SASL_MECHANISM')
security_protocol = os.getenv('SECURITY_PROTOCOL')

app = FastAPI()

# Kafka consumer configuration
consumer = KafkaConsumer(
    'concrete_production_data',
    bootstrap_servers=host,
    sasl_mechanism=sasl_mechanism,
    security_protocol=security_protocol,
    sasl_plain_username=user,
    sasl_plain_password=pwd,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

async def kafka_event_generator():
    for message in consumer:
        yield {
            "event": "new_data",
            "data": json.dumps(message.value)
        }
        await asyncio.sleep(0.1)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for message in kafka_event_generator():
        await websocket.send_json(message)

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
        data = {
            'temperature': params.temperature,  # degrees Celsius
            'humidity': params.humidity,  # percentage (%), default 60
            'curing_time': params.curing_time,  # hours
            'energy_consumption': params.energy_consumption,  # kilowatt-hours (kWh)
            'amount_produced_m3': params.amount_produced_m3,
            'dosing_events': params.dosing_events,  # Number of dosing events
            'active_power_curve': params.active_power_curve,  # watts (W)
            'truck_drum_rotation_speed': params.truck_drum_rotation_speed,  # rotations per minute (rpm)
            'truck_drum_duration': params.truck_drum_duration,  # minutes
            'cement': params.cement,  # kg
            'sand': params.sand,  # kg
            'gravel': params.gravel  # kg
        }
        prediction = predict_emissions(model, data)
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