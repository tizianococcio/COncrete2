from typing import Dict, Any
from pydantic import BaseModel

class InputParameters(BaseModel):
    """
    Schema for input parameters.
    """
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

def get_units() -> Dict[str, Any]:
    return {
        'temperature': '°C',  # degrees Celsius
        'humidity': '%',  # percentage (%), default 60
        'curing_time': 'hours',  # hours
        'energy_consumption': 'kWh',  # kilowatt-hours (kWh)
        'amount_produced_m3': 'm³',
        'dosing_events': '',  # Number of dosing events
        'active_power_curve': 'W',  # watts (W)
        'truck_drum_rotation_speed': 'rpm',  # rotations per minute (rpm)
        'truck_drum_duration': 'minutes',  # minutes
        'cement': 'kg',  # kg
        'sand': 'kg',  # kg
        'gravel': 'kg'  # kg
    }

def get_default_parameters() -> Dict[str, Any]:
    """
    Get default input parameters for the model prediction.

    Returns:
        Dict[str, Any]: A dictionary with default values for the input parameters.
    """
    return InputParameters.parse_obj({
        'temperature': 15,  # degrees Celsius
        'humidity': 30,  # percentage (%), default 60
        'curing_time': 18,  # hours
        'energy_consumption': 105,  # kilowatt-hours (kWh)
        'amount_produced_m3': 1,  # cubic meters (m³)
        'dosing_events': 2,  # Number of dosing events
        'active_power_curve': 105,  # watts (W)
        'truck_drum_rotation_speed': 11,  # rotations per minute (rpm)
        'truck_drum_duration': 22,  # minutes
        'cement': 300,  # kg
        'sand': 580,  # kg
        'gravel': 1020  # kg
    }).dict()
