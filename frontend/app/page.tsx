// `app/page.tsx` is the UI for the `/` URL
import Head from 'next/head';
import PredictionForm from '../components/PredictionForm';
import OptimalValues from '../components/OptimalValues';
import RealTimeWebSocket from '../components/RealTimeWebSocket'

export default function Page() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-3xl">CO2 Emissions Dashboard</h1>
      </header>
      <main className="min-h-screen bg-gray-100 p-4">
        <div className="container mx-auto flex flex-col lg:flex-row">
          <div className="w-full lg:w-1/3 p-4">
            <PredictionForm />
          </div>
          <div className="w-full lg:w-2/3 p-4">
            <div className="bg-white rounded-lg shadow-md p-4 h-full">
              {/*<h2 className="text-2xl font-bold mb-4">Other Content</h2>*/}
              <OptimalValues />
              <RealTimeWebSocket />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}