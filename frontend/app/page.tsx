// `app/page.tsx` is the UI for the `/` URL
import Head from 'next/head';
import PredictionForm from '../components/PredictionForm';

export default function Page() {
  return (
      <div>
          <Head>
              <title>CO2 Emissions Predictor</title>
              <meta name="description" content="Predict CO2 emissions based on input parameters" />
          </Head>
          <main>
              <h1>CO2 Emissions Predictor</h1>
              <PredictionForm />
          </main>
      </div>
  );
}