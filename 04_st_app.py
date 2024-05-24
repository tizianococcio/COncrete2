import streamlit as st
import joblib
import pandas as pd

# Load the model
model = joblib.load('model.pkl')

# Title and introduction
st.set_page_config(page_title='CO2 Emission Model')
st.title('Concrete CO2 Emissions Model')
st.write("""
This (demo) application helps optimize concrete production parameters to minimize CO2 emissions.
Adjust the sliders on th left, then push the button below to see the predicted CO2 emissions.
""")

# Sidebar for sliders
st.sidebar.header('Set Input Values')

# Define sliders for user input
temperature = st.sidebar.slider('Temperature (°C)', 0, 50, 25)
humidity = st.sidebar.slider('Humidity (%)', 0, 100, 60)
curing_time = st.sidebar.slider('Curing Time (hours)', 0, 48, 24)
energy_consumption = st.sidebar.slider('Energy Consumption (kWh)', 0, 1000, 300)
amount_produced_m3 = st.sidebar.slider('Amount Produced (m³)', 1, 100, 1)
dosing_events = st.sidebar.slider('Dosing Events', 1, 10, 5)
active_power_curve = st.sidebar.slider('Active Power Curve (W)', 0, 500, 250)
truck_drum_rotation_speed = st.sidebar.slider('Truck Drum Rotation Speed (rpm)', 0, 30, 15)
truck_drum_duration = st.sidebar.slider('Truck Drum Duration (minutes)', 0, 60, 30)
cement = st.sidebar.slider('Cement (kg)', 0, 1000, 350)
sand = st.sidebar.slider('Sand (kg)', 0, 1500, 700)
gravel = st.sidebar.slider('Gravel (kg)', 0, 2000, 1200)

# Placeholder for prediction results
st.session_state.result = None
prediction_placeholder = st.empty()
if st.session_state.result is not None:
    with prediction_placeholder.container():
        st.subheader('Predicted CO2 Emissions')
        st.write(st.session_state.result)

# Predict button
if st.button('Predict CO2 Emissions'):
    # Prepare input data
    X = pd.DataFrame([{
        'temperature': temperature,
        'humidity': humidity,
        'curing_time': curing_time,
        'energy_consumption': energy_consumption,
        'amount_produced_m3': amount_produced_m3,
        'dosing_events': dosing_events,
        'active_power_curve': active_power_curve,
        'truck_drum_rotation_speed': truck_drum_rotation_speed,
        'truck_drum_duration': truck_drum_duration,
        'cement': cement,
        'sand': sand,
        'gravel': gravel
    }])

    # Predict CO2 emissions
    prediction = model.predict(X)
    st.session_state.result = prediction
    if st.session_state.result is not None:
        with prediction_placeholder.container():
            st.subheader('Predicted CO2 Emissions')
            st.session_state.result = f"Predicted CO2 Emissions for {amount_produced_m3} m³: {prediction[0]:.2f} kg"
            st.write(st.session_state.result)    

st.header('Training data inspectation')
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv('data.csv')
# Compute the correlation matrix
corr_matrix = data.corr()

# Plot the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix of Features and CO2 Emissions')
plt.show()
st.pyplot(plt)

# About section
st.header('About')
st.write("""
This project demonstrates the use of machine learning to optimize concrete production and reduce carbon emissions.
Developed by Tiziano Cocciò.
""")
