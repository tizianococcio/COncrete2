// frontend/src/components/RealTimeWebSocket.js
"use client";
import React, { useEffect, useState } from 'react';
import RealTimePlot from './RealTimePlot'

const RealTimeWebSocket = ({ onTemperatureUpdate }) => {
  const [data, setData] = useState(null);
  const [emissionData, setEmissionData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001/ws');

    ws.onmessage = (event) => {
      const newData = JSON.parse(event.data).data;
      const parsed_data = JSON.parse(newData)
      onTemperatureUpdate(parsed_data.temperature);
      setData(parsed_data);
      setEmissionData(parsed_data.predicted_co2);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="p-4 bg-white rounded-lg shadow-md mt-4">
      <h1 className="text-2xl font-bold">Real-Time Sensor Data</h1>
      {data ? (
        <div>
          <ul>
            <li>Temperature: {data.temperature.toFixed(2)} °C</li>
            <li>Humidity: {data.humidity.toFixed(2)} %</li>
            <li>Energy Consumption: {data.energy_consumption.toFixed(2)} kWh</li>
            <li>Active Power Curve: {data.active_power_curve.toFixed(2)} W</li>
            <li>Truck Drum Rotation Speed: {data.truck_drum_rotation_speed.toFixed(2)} rpm</li>
            <li>Truck Drum Duration: {data.truck_drum_duration.toFixed(2)} minutes</li>
            <li>Cement: {data.cement.toFixed(2)} kg</li>
            <li>Sand: {data.sand.toFixed(2)} kg</li>
            <li>Gravel: {data.gravel.toFixed(2)} kg</li>
          </ul>
          <div className="p-4 bg-slate-600 rounded-lg shadow-md m-4">
            <h3 className='text-white font-bold'>Predicted CO2 Emissions: {data.predicted_co2.toFixed(2)} kg/m³</h3>
          </div>         
          <RealTimePlot newEmissionData={emissionData} /> 
        </div>
      ) : (
        <p>Waiting for data...</p>
      )}
    </div>
  );
};

export default RealTimeWebSocket;
