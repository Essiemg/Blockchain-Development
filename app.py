import streamlit as st
import joblib
import pandas as pd

# Load the model
model = joblib.load('lgbm_energy_model.pkl')  # Ensure the model file is in your project folder

# Streamlit app UI
st.title("Smart Grid Guardians: Energy Consumption Predictor")

# Collect user inputs
temperature = st.number_input('Temperature (°C)')
humidity = st.number_input('Humidity (%)')
square_footage = st.number_input('Building Area (sq. ft.)')
occupancy = st.number_input('Occupancy (Number of People)')
hvac_usage = st.number_input('HVAC Usage (kWh)')
lighting_usage = st.number_input('Lighting Usage (kWh)')
renewable_energy = st.number_input('Renewable Energy Generated (kWh)')
day_of_week = st.selectbox('Day of Week', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
holiday = st.selectbox('Is it a Holiday?', ['Yes', 'No'])

# Prepare input data
input_data = pd.DataFrame({
    'Temperature': [temperature],
    'Humidity': [humidity],
    'SquareFootage': [square_footage],
    'Occupancy': [occupancy],
    'HVACUsage': [hvac_usage],
    'LightingUsage': [lighting_usage],
    'RenewableEnergy': [renewable_energy],
    'DayOfWeek': [day_of_week],
    'Holiday': [holiday]
})

# Encode categorical variables
input_data['DayOfWeek'] = input_data['DayOfWeek'].map({
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
})
input_data['Holiday'] = input_data['Holiday'].map({'Yes': 1, 'No': 0})

# Make predictions when the button is clicked
if st.button('Predict Energy Consumption'):
    try:
        prediction = model.predict(input_data)
        st.write(f"Predicted Energy Consumption: {prediction[0]:.2f} MWh")
    except ValueError as e:
        st.error(f"Prediction error: {e}")