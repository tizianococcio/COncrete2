// frontend/src/components/RealTimeWebSocket.js
"use client";
import React, { useEffect, useState } from 'react';
import RealTimePlot from './RealTimePlot'

const RealTimeWebSocket = ({ onTemperatureUpdate, units }) => {
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
        <ul className="space-y-1 columns-2 font-mono">
          {Object.entries(data).map(([key, value]) => (
            units[key] !== undefined && (
            <li key={key} className="flex justify-between">
              <span>{key.replace(/_/g, ' ')}:</span>
              <span className="font-sans font-semibold text-red-800">{value.toFixed(2)} {units[key]}</span>
            </li>
            )
          ))}
        </ul>          
        <div className="p-4 bg-slate-600 rounded-lg shadow-md m-4 text-center">
          <h3 className='text-white'>Predicted CO2 Emissions: <span className='text-xl font-bold'>{data.predicted_co2.toFixed(2)} kg/m³</span></h3>
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
