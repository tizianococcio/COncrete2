"use client";

import React, { useState } from 'react';
import axios from 'axios';

const labels = {
  temperature: 'Temperature (°C)',
  humidity: 'Humidity (%)',
  curing_time: 'Curing Time (hours)',
  energy_consumption: 'Energy Consumption (kWh)',
  amount_produced_m3: 'Amount Produced (m³)',
  dosing_events: 'Dosing Events',
  active_power_curve: 'Active Power Curve (W)',
  truck_drum_rotation_speed: 'Truck Drum Rotation Speed (rpm)',
  truck_drum_duration: 'Truck Drum Duration (minutes)',
  cement: 'Cement (kg)',
  sand: 'Sand (kg)',
  gravel: 'Gravel (kg)'
};

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    temperature: 25,
    humidity: 60,
    curing_time: 24,
    energy_consumption: 300,
    amount_produced_m3: 1,
    dosing_events: 5,
    active_power_curve: 250,
    truck_drum_rotation_speed: 15,
    truck_drum_duration: 30,
    cement: 350,
    sand: 700,
    gravel: 1200
  });

  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/predict', formData);
      setPrediction(response.data.predicted_co2_emissions);
      console.log('Prediction:', response.data);
    } catch (error) {
      console.error('Error making prediction:', error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-2 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-2">Manual CO2 Emissions Prediction</h2>

      <div className="p-4 bg-slate-600 rounded-lg shadow-md m-4 text-center">
        <h3 className='text-white'>Predicted CO2 Emissions: <span className='text-xl font-bold'>{prediction !== null ? `${prediction.toFixed(2)} kg/m³` : '---'}</span></h3>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {Object.keys(formData).map((key) => (
          <div key={key} className="flex flex-col">
            <label className="text-sm font-medium mb-1">{labels[key]}</label>
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              className="px-3 py-2 border rounded-md"
            />
          </div>
        ))}
        <div className="flex justify-center">
          <button type="submit" className="px-6 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700">
            Predict CO2 Emissions
          </button>
        </div>
      </form>
    </div>
  );
};

export default PredictionForm;
