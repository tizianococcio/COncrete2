// components/OptimalValues.js
"use client";

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const OptimalValues = ({ temperature, units }) => {
  const [optimalValues, setOptimalValues] = useState(null);
  const [loading, setLoading] = useState(true);
  const [msg, setMessage] = useState("");
  const [error, setError] = useState(null);
  const temperatureRef = useRef(temperature);
  const [countdown, setCountdown] = useState(null);

  useEffect(() => {
    temperatureRef.current = temperature;
  }, [temperature]);

  useEffect(() => {
    const refreshInterval = 60_000;
    const fetchOptimalValues = async () => {
      if (temperatureRef.current !== null) {
        try {
          setMessage("Computing optimal parameters...")
          const response = await axios.get(`/api/getoptimal?temperature=${temperatureRef.current}`).then(function (response) {
            setMessage("");
            return response;
          });
          setOptimalValues(response.data);
          setLoading(false);
        } catch (err) {
          setError(err.message);
          setLoading(false);
        }
      }
    };
    fetchOptimalValues();
    const intervalId = setInterval(() => {
      fetchOptimalValues();
      setCountdown(refreshInterval/1000);  // Reset countdown after fetching data
    }, refreshInterval);

    const countdownInterval = setInterval(() => {
      setCountdown(prevCountdown => prevCountdown > 0 ? prevCountdown - 1 : refreshInterval/1000);
    }, 1000);
    
    return () => {
      clearInterval(intervalId);
      clearInterval(countdownInterval);
    };
  }, []);

  if (loading) return <div className="p-4 mt-2.5 bg-white rounded-lg shadow-md">Loading optimizer (may take a while)...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="p-4 mt-2.5 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold">Optimal Input Parameters for 1m³ of concrete (@ <span className='text-red-800'>{optimalValues.optimal_parameters.temperature.toFixed(2)} °C</span>)</h2>
      <p className='mb-4 text-slate-500'><div>{msg ? msg : `Next update in ${countdown} seconds...`}</div></p>
      {optimalValues.optimal_parameters ? (
        <>        <ul className="space-y-1 columns-2 font-mono">
          {Object.entries(optimalValues.optimal_parameters).map(([key, value]) => (
            <li key={key} className="flex justify-between">
              <span>{key.replace(/_/g, ' ')}:</span>
              <span className="font-sans font-semibold text-red-800">{value.toFixed(2)} {units[key]}</span>
            </li>
          ))}
        </ul>
        <div className="p-4 bg-slate-600 rounded-lg shadow-md m-4 text-center">
          <h3 className='text-white'>Predicted CO2 Emissions: <span className='text-xl font-bold'>{optimalValues.expected_co2_emissions.toFixed(2)} kg/m³</span></h3>
        </div>
        </>
      ) : (
        <p>No optimal values found.</p>
      )}
    </div>
  );
};

export default OptimalValues;
