"use client";
import React, { useState } from 'react';
import OptimalValues from './OptimalValues';
import RealTimeWebSocket from './RealTimeWebSocket';

const RealTimeMonitor = () => {
  const [temperature, setTemperature] = useState(null);

  const handleTemperatureUpdate = (newTemperature) => {
    setTemperature(newTemperature);
  };

  return (
    <>
      <RealTimeWebSocket onTemperatureUpdate={handleTemperatureUpdate} />
      <OptimalValues temperature={temperature} />
    </>
  );
};

export default RealTimeMonitor;
