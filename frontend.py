import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

#input
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (KG)", min_value=1.0, value=50.0)
height = st.number_input('Height (m)', min_value=0.0, max_value=3.0, value=1.6)
income_lpa = st.number_input('Annual Income ', min_value=0.0, value=2.0)
smoker = st.selectbox('Are you a smoker?', options=[True, False])
city = st.text_input('City', value='Mumbai')
occupation = st.selectbox(
    'Occupation',
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
    )
if st.button('Predict'):
    input_data = {
        'age': age,
        'weight': weight,
        'height': height,
        'income_lpa': income_lpa,
        'smoker': smoker,
        'city': city,
        'occupation': occupation
    }
    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        print(result)

        if response.status_code == 200 and "Prediction status" in result:
            predict = result['Prediction status']
            # st.success(f"Predicted Insurance Premium Category: **{result['Prediction status']}**")
            st.success(result['Prediction status'])


        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error('Failed to connect to fast api server')


