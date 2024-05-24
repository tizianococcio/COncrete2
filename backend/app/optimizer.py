import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

def optimize_parameters(model):
    def get_default_row(values):
        temperature, humidity, curing_time, energy_consumption, dosing_events, active_power_curve, truck_drum_rotation_speed, truck_drum_duration, cement, sand, gravel = values
        row = {
            'temperature': temperature,  # degrees Celsius
            'humidity': humidity,  # percentage (%), default 60
            'curing_time': curing_time,  # hours
            'energy_consumption': energy_consumption,  # kilowatt-hours (kWh)
            'amount_produced_m3': 1, # (m3)
            'dosing_events': dosing_events,  # Number of dosing events
            'active_power_curve': active_power_curve,  # watts (W)
            'truck_drum_rotation_speed': truck_drum_rotation_speed,  # rotations per minute (rpm)
            'truck_drum_duration': truck_drum_duration,  # minutes
            'cement': cement,  # kg
            'sand': sand,  # kg
            'gravel': gravel  # kg
        }
        return row

    def predict_co2_emissions(inputs):
        row = get_default_row(inputs)        
        input_data = pd.DataFrame([row])
        co2_emissions = model.predict(input_data)[0]
        return co2_emissions

    def objective_function(params):
       return predict_co2_emissions(params)

    # Define bounds for the parameters to optimize
    bounds = [
        (15, 30),  # temperature in degrees Celsius
        (30, 80),  # humidity in percentage (%)
        (12, 48),  # curing_time in hours
        (100, 500),  # energy_consumption in kilowatt-hours (kWh)
        (1, 10),  # dosing_events
        (100, 500),  # active_power_curve in watts (W)
        (10, 30),  # truck_drum_rotation_speed in rotations per minute (rpm)
        (10, 60),  # truck_drum_duration in minutes
        (300, 400),  # cement in kg
        (500, 1000),  # sand in kg
        (1000, 1500)  # gravel in kg
    ]

    # Run the optimization
    result = differential_evolution(objective_function, bounds)

    # Get the optimal values
    optimal_inputs = result.x
    optimal_co2_emissions = result.fun

    # Map to named dictionary
    row = get_default_row([0]*11)
    del row['amount_produced_m3']
    optimal_inputs = {k: optimal_inputs[i] for i, k in enumerate(row.keys())}

    return optimal_inputs, optimal_co2_emissions
