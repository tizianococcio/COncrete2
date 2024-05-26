# kafka_producer.py
from kafka import KafkaProducer
import json
import numpy as np
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'concrete_production_data'

step = 0
num_steps = 1000
while True:
    # Parameters
    initial_temperature = 20
    drift_per_step = np.random.uniform(0.01, 0.05)
    noise_scale = 0.05
    if step == num_steps:
        step = 0

    # Generate time steps
    temperature_drift = initial_temperature + drift_per_step * step
    random_noise = np.random.normal(scale=noise_scale)
    temperature_with_noise = temperature_drift + random_noise

    data = {
        'temperature': temperature_with_noise,
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