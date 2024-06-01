# kafka_producer.py
from kafka import KafkaProducer
import json
import numpy as np
import time
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

producer = KafkaProducer(
    bootstrap_servers=host,
    sasl_mechanism=sasl_mechanism,
    security_protocol=security_protocol,
    sasl_plain_username=user,
    sasl_plain_password=pwd,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'concrete_production_data'

step = 0
num_steps = 1000
sine_fluctuation = np.sin(10 * np.pi * np.linspace(0, 1, num_steps))

while True:
    if step == num_steps:
        step = 0
    temperature = np.random.uniform(18, 22) + sine_fluctuation[step]
    data = {
        'temperature': temperature,
        'humidity': np.random.uniform(30, 80),
        'energy_consumption': np.random.uniform(100, 500),
        'active_power_curve': np.random.uniform(100, 300),
        'truck_drum_rotation_speed': np.random.uniform(10, 20),
        'truck_drum_duration': np.random.uniform(10, 60),
        'cement': np.random.uniform(300, 400),
        'sand': np.random.uniform(600, 800),
        'gravel': np.random.uniform(1000, 1400)
    }
    producer.send(topic, data)
    print(f'Sent data: {data}')
    time.sleep(1)
    step += 1
