# Introduction
This is a demo application complementing my application for the (Senior Python Backend Engineer for ML-based Applications) position at Alcemy. It is a dockerized application that highlights several key aspects of my skill set:

- Tackling machine learning, statistics, and optimization challenges.
- Proficency in software engineering.
- Quickly adapting to new tools (most of which were new to me).

It uses Docker, FastAPI, Next.js, and Kafka. Full details about the architure are below. It implements a simple linear regression model, based on assumptions about the correlation between some factors (not all) involved in concrete production and the corresponding CO2 emission.

I've drawn insights from a variety of sources, including Alcemy's website, for example:
- https://alcemy.tech/en/produkt/beton
- https://en.wikipedia.org/wiki/Environmental_impact_of_concrete#Carbon_dioxide_emissions_and_climate_change

## TL;DR
- Link to the fully-fledged demo application: (password: )
- Link to the basic Streamlit application: 

# Data
I used this information to generate synthetic data points. This is done in the file [01_data.py](01_data.py). As an attempt to have somewhat realistic data, I calibrated the training set so that with the default input values (those in the `streamlit` form), the CO2 emission is about 410 kg/m3, as described in the Wikipedia article above.

# Model
What I report here is the second iteration of the model. My initial model was based on fewer input parameters, namely temperature, humidity, curing time, and energy consumption. With this simpler data set, a plain Linear Regression model was able to accurately fit the data. Adding more features, in particular dosing events, power curve, rotation speed and duration of the truck drum, the ratio of cement, sand, and gravel increased the complexity of the model, introducing nonlinear correlations. Taking this into account, I added degree-2 polynomials to the original Linear Regression model. The model is defined in the file [02_model.py](02_model.py).

## Model Evaluation
The residual plot clearly shows some heteroscedasticity (non-constant variance of residuals) and potential non-linearity that is not being fully captured by the model. Running out of time and wanting to focus on the bigger picture I decided to leave the model as is. The model evaluation analysis can be fully seen in the Jupyter Notebook [03_evaluation.ipynb](03_evaluation.ipynb).

# Demo Streamlit Application
A basic Streamlit frontend application provides a simple interface to the regression model. This is in [04_st_app.py](04_st_app.py). And can be seen online at [...].

# Fully-fledged Application Architecture
I created an API endpoint using FastAPI, the frontend uses Next.js with websockets to receive a constant datastream of sensor data from the server. Sensor data is simulated by random sampling from uniform distributions and submitted to a Kafka producer with the topic `concrete_production_data`. All the CO2 predictions are made using the linear model mentioned above, utility functions to access this model are to be found in [model.py](backend/app/model.py). Optimization to minimize CO2 emissions is performed by [Differential Evolution](https://en.wikipedia.org/wiki/Differential_evolution) in [optimizer.py](backend/app/optimizer.py) The whole application is bundled in a docker container, see [docker-compose.yml](docker-compose.yml).

## Kafka Simulated Sensor Data Producer
[data_source/producer.py](data_source/producer.py) publishes simulated sensor data every second to a Kafka Producer topic. To achieve a slightly realistic experience I decided to only simulate data which could realistically be measured. Additionally, I made sure that the simulated data is somewhat between realistic ranges. As an experimental approach, I tried simulating the temperature in a more realistic way by adding a temperature drift across time with random noise sampled from a normal distribution.

## FastAPI Backend
Is implemented in [backend/app/main.py](backend/app/main.py). This exposes the following endpoints:
- `/ws`: websocket sending data consumed from the Kafka Producer.
- `/predict`: accepts POST requests, responds with a CO2 prediction value.
- `/getoptimal`: accepts GET requests and uses the CO2 optimizer to return optimal values to minimize CO2 emissions. GET query parameters can be used to set input values which should be held constant during optimization. For the sake of this demo this is only implemented for the `temperature` parameter.
This is perhaps the most refined code example in terms of code comments, and use of best-practices.

## Next.JS Frontend
Provides a simple dashboard based on the default application built with the Next.js (TypeScript) `create-next-js` CLI tool. It features:
- A [prediction form](frontend/components/PredictionForm.js) allowing to manually predict CO2 emissions using the aforementioned linear model.
- [Real-time data view](frontend/components/RealTimeWebSocket.js). This shows the simulated data published to Kafka, consumed by the API and sent to the frontend via websockets. This view is updated every second, as new data becomes available.
- The [optimal values](frontend/components/OptimalValues.js) that would achieve the lower possible CO2 emissions, given the current (simulated) temperature value. These are updated every 5 seconds. 
- A [real-time plot](frontend/components/RealTimePlot.js) of predicted CO2 emissions.

I used TailwindCSS for basic styling.

# Improvements/What's missing
- Documentation!
- Add extensive tests
- Store sensor data in a DB for analysis
- CO2Optimizer
    - inject default bounds from a config file
    - add logging/error handling
    - Improve in speed (maybe caching?)
- ML Model
    - Use real-world data and build a proper model

# Disclaimer
I used LLMs for mechanical tasks, like writing docstring comments.