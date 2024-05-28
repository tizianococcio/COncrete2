"use client";
import React, { useState, useEffect } from 'react';
import OptimalValues from './OptimalValues';
import RealTimeWebSocket from './RealTimeWebSocket';

const RealTimeMonitor = () => {
  const [temperature, setTemperature] = useState(null);
  const [units, setUnits] = useState(null);

  useEffect(() => {
    fetch('/api/units')
      .then((res) => res.json())
      .then((response) => {
        setUnits(response);
      })
  }, [])  

  const handleTemperatureUpdate = (newTemperature) => {
    setTemperature(newTemperature);
  };

  // Render components only when units is not null
  if (units === null) {
    return <div>Loading...</div>; // or any loading indicator you prefer
  }  

  return (
    <>
      <RealTimeWebSocket onTemperatureUpdate={handleTemperatureUpdate} units={units} />
      <OptimalValues temperature={temperature} units={units} />
    </>
  );
};

export default RealTimeMonitor;
