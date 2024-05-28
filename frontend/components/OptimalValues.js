// components/OptimalValues.js
"use client";

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const OptimalValues = ({ temperature, units }) => {
  const [optimalValues, setOptimalValues] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const temperatureRef = useRef(temperature);

  useEffect(() => {
    temperatureRef.current = temperature;
  }, [temperature]);

  useEffect(() => {
    const fetchOptimalValues = async () => {
      if (temperatureRef.current !== null) {
        try {
          const response = await axios.get(`/api/getoptimal?temperature=${temperatureRef.current}`);
          setOptimalValues(response.data.optimal_parameters);
          setLoading(false);
        } catch (err) {
          setError(err.message);
          setLoading(false);
        }
      }
    };
    fetchOptimalValues();
    const intervalId = setInterval(fetchOptimalValues, 5000);
    
    return () => clearInterval(intervalId);
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="p-4 mt-2.5 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold">Optimal Input Parameters for 1m³ of concrete (@ <span className='text-red-800'>{optimalValues.temperature.toFixed(2)} °C</span>)</h2>
      <p className='mb-4 text-slate-500'>Optimal values are computed and updated every 5 seconds.</p>
      {optimalValues ? (
        <ul className="space-y-1 columns-2 font-mono">
          {Object.entries(optimalValues).map(([key, value]) => (
            <li key={key} className="flex justify-between">
              <span>{key.replace(/_/g, ' ')}:</span>
              <span className="font-sans font-semibold text-red-800">{value.toFixed(2)} {units[key]}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No optimal values found.</p>
      )}
    </div>
  );
};

export default OptimalValues;
