import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load pickle files
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Page Title and Description
st.title("🏠 RealEase: Your Property Price Estimator")
st.markdown("""
Welcome to **RealEase**! This platform uses advanced Machine Learning to estimate property prices based on your inputs.  
Whether you're buying or selling, get an accurate estimate instantly.  
""")

st.divider()

# Sidebar for Tips
with st.sidebar:
    st.header("🔍 How It Works")
    st.markdown("""
    1. Fill in the property details in the form below.
    2. Click **Predict Price** to see the estimated price range.
    3. Adjust your inputs to explore different scenarios!
    """)
    st.info("💡 *Tip*: Accurate inputs give better predictions.")

# Inputs
st.header('Enter Property Details')

property_type = st.selectbox('Property Type', ['flat', 'house'], help="Choose whether the property is a flat or a house.")
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()), help="Select the sector where the property is located.")
bedrooms = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()))
bathrooms = st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist()))
balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
property_age = st.selectbox('Property Age (Years)', sorted(df['agePossession'].unique().tolist()))
built_up_area = st.number_input('Built-up Area (sqft)', min_value=100.0, step=50.0, help="Enter the built-up area in square feet.")
servant_room = st.selectbox('Servant Room', [0, 1], help="Specify if there is a servant room (0 = No, 1 = Yes).")
store_room = st.selectbox('Store Room', [0, 1], help="Specify if there is a store room (0 = No, 1 = Yes).")
with st.expander("Select Furnishing Type"):
    furnishing_type = st.radio(
        "Choose from the options below:",
        options=sorted(df['furnishing_type'].unique().tolist()),
        help="Select the furnishing type of the property."
    )

with st.expander("Select Luxury Category"):
    luxury_category = st.radio(
        "Choose from the options below:",
        options=sorted(df['luxury_category'].unique().tolist()),
        help="Select the luxury category of the property."
    )

with st.expander("Select Floor Category"):
    floor_category = st.radio(
        "Choose the floor category from the options below:",
        options=sorted(df['floor_category'].unique().tolist()),
        help="Select the floor category of the property (e.g., Low, Medium, High)."
    )

# Predict Button
if st.button('Predict Price'):
    with st.spinner('Calculating the price range...'):
        # Create DataFrame
        data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room,
                 store_room, furnishing_type, luxury_category, floor_category]]
        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area',
                   'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']
        one_df = pd.DataFrame(data, columns=columns)

        # Predict
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22

        # Display Results
        st.success(f"🏡 The estimated price range is between **₹{round(low, 2)} Cr** and **₹{round(high, 2)} Cr**")
        st.markdown("This prediction is based on the inputs provided and the ML model's confidence margin.")
st.divider()