// components/PredictionForm.js
"use client";
import React, { useState } from 'react';
import axios from 'axios';

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
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/predict', formData);
            setPrediction(response.data.predicted_co2_emissions);
        } catch (error) {
            console.error('Error making prediction:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                {Object.keys(formData).map((key) => (
                    <div key={key}>
                        <label htmlFor={key}>{key.replace(/_/g, ' ')}:</label>
                        <input
                            type="number"
                            id={key}
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                        />
                    </div>
                ))}
                <div style={{ textAlign: 'center' }}>
                    <button type="submit">Predict CO2 Emissions</button>
                </div>
            </form>
            {prediction !== null && (
                <div>
                    <h3>Predicted CO2 Emissions: {prediction}</h3>
                </div>
            )}
        </div>
    );
};

export default PredictionForm;
