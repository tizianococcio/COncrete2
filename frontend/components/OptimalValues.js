// components/OptimalValues.js
"use client";

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const OptimalValues = ({ temperature }) => {
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
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Optimal Input Parameters for 1m³ of concrete (@ {optimalValues.temperature.toFixed(2)} °C)</h2>
      {optimalValues ? (
        <ul className="space-y-2">
          {Object.entries(optimalValues).map(([key, value]) => (
            <li key={key} className="flex justify-between">
              <span className="font-medium">{key.replace(/_/g, ' ')}:</span>
              <span>{value.toFixed(2)}</span>
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
