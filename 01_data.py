import pandas as pd
import numpy as np
import joblib

# Generate synthetic data
def calculate_co2_emissions(row):
    # Base emissions per cubic meter of concrete produced (in kg CO2 per m³)
    base_emission_per_m3 = 0  # kg CO2/m³
    
    # Calculate the factors contributing to emissions
    temperature_factor = 0.4 * row['temperature']  # kg CO2/°C
    humidity_factor = 0.3 * row['humidity']  # kg CO2/%
    curing_time_factor = 0.2 * row['curing_time']  # kg CO2/hour
    energy_consumption_factor = 0.1 * row['energy_consumption']  # kg CO2/kWh
    
    # New factors based on additional data
    dosing_events_factor = 0.05 * row['dosing_events']  # kg CO2 per event
    active_power_curve_factor = 0.2 * row['active_power_curve']  # kg CO2/W
    truck_drum_rotation_factor = 0.1 * row['truck_drum_rotation_speed']  # kg CO2/rpm
    truck_drum_duration_factor = 0.05 * row['truck_drum_duration']  # kg CO2/minute
    
    # Composition mix factors
    cement_factor = 0.8 * row['cement']  # kg CO2 per kg of cement
    sand_factor = 0.008 * row['sand']  # kg CO2 per kg of sand
    gravel_factor = 0.005 * row['gravel']  # kg CO2 per kg of gravel
    
    # Add some noise to simulate real-world variations
    noise = np.random.normal(0, 5)  # kg CO2
    
    # Total CO2 emissions based on the amount of concrete produced in cubic meters
    co2_emissions = row['amount_produced_m3'] * (
        base_emission_per_m3 + temperature_factor + humidity_factor +
        curing_time_factor + energy_consumption_factor + dosing_events_factor +
        active_power_curve_factor + truck_drum_rotation_factor + truck_drum_duration_factor +
        cement_factor + sand_factor + gravel_factor + noise
    )
    
    return co2_emissions


np.random.seed(42)
n = 100000
data = pd.DataFrame({
    'temperature': np.random.uniform(15, 30, n),  # degrees Celsius
    'humidity': np.random.uniform(30, 80, n),  # percentage (%)
    'curing_time': np.random.uniform(12, 48, n),  # hours
    'energy_consumption': np.random.uniform(100, 500, n),  # kilowatt-hours (kWh)
    'amount_produced_m3': np.random.uniform(0.5, 2, n),  # cubic meters (m³)
    'dosing_events': np.random.randint(1, 10, n),  # Number of dosing events
    'active_power_curve': np.random.uniform(50, 300, n),  # watts (W)
    'truck_drum_rotation_speed': np.random.uniform(10, 20, n),  # rotations per minute (rpm)
    'truck_drum_duration': np.random.uniform(20, 40, n),  # minutes
    'cement': np.random.uniform(200, 400, n),  # kg
    'sand': np.random.uniform(500, 1000, n),  # kg
    'gravel': np.random.uniform(1000, 1500, n),  # kg
})

# Calculate CO2 emissions using the defined function
data['co2_emissions'] = data.apply(calculate_co2_emissions, axis=1)

# Normalize numerical variables
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler = scaler.fit(
    data[['temperature', 'humidity', 'curing_time', 'energy_consumption', 'amount_produced_m3', 
          'dosing_events', 'active_power_curve', 'truck_drum_rotation_speed', 
          'truck_drum_duration', 'cement', 'sand', 'gravel']]
)

# Save the scaler
joblib.dump(scaler, 'model/scaler.joblib')

# Save to CSV
data.to_csv('model/data.csv', index=False)
