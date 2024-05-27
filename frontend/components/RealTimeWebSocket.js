// frontend/src/components/RealTimeWebSocket.js
"use client";
import React, { useEffect, useState } from 'react';

const RealTimeWebSocket = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001/ws');

    ws.onmessage = (event) => {
      const newData = JSON.parse(event.data).data;
      setData(JSON.parse(newData));
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="p-4 bg-white rounded-lg shadow-md mt-4">
      <h1 className="text-2xl font-bold">Real-Time Data</h1>
      {data ? (
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
      ) : (
        <p>Waiting for data...</p>
      )}
    </div>
  );
};

export default RealTimeWebSocket;
