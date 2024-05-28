import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, TimeScale } from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

const RealTimePlot = ({ newEmissionData }) => {
  const chartRef = useRef(null);
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Predicted CO2 Emissions',
        data: [],
        fill: false,
        borderColor: 'rgba(75,192,192,1)',
        tension: 0.1,
      },
    ],
  });

  useEffect(() => {
    if (newEmissionData !== null) {
      const currentTime = new Date();
      setData((prevData) => {
        const updatedLabels = [...prevData.labels, currentTime];
        const updatedData = [...prevData.datasets[0].data, newEmissionData];

        if (updatedLabels.length > 60) {
          updatedLabels.shift();
          updatedData.shift();
        }

        return {
          ...prevData,
          labels: updatedLabels,
          datasets: [
            {
              ...prevData.datasets[0],
              data: updatedData,
            },
          ],
        };
      });
    }
  }, [newEmissionData]);

  return (
    <div className='mt-10'>
      <h3 className='text-xl font-semibold p-4 pb-6'>Predicted CO2 emissions according to received sensor readings of the past 60 seconds:</h3>
      <Line
        ref={chartRef}
        data={data}
        options={{
          responsive: true,
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'second',
                tooltipFormat: 'PPpp',
                displayFormats: {
                  second: 'HH:mm:ss',
                },
              },
              title: {
                display: true,
                text: 'Time (seconds)',
              },
            },
            y: {
              title: {
                display: true,
                text: 'Predicted CO2 Emissions',
              },
            },
          },
        }}
      />
    </div>
  );
};

export default RealTimePlot;
