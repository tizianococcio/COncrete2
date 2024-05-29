"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ApiTest = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        var temperature = Math.random() * 100;
        const response = await axios.get(`/api/getoptimal?temperature=${temperature}`);
        setData(response.data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 5000);

    return () => clearInterval(intervalId);
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Optimal Values</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default ApiTest;
