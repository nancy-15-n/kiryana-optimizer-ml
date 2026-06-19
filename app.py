import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# 1. Load the trained machine learning model and feature list
try:
    model = joblib.load('kiryana_model.pkl')
    model_features = joblib.load('model_features.pkl')
except FileNotFoundError:
    st.error("❌ Error: 'kiryana_model.pkl' or 'model_features.pkl' not found. Please run your machine learning training script first to generate these files!")

# 2. Set up the web page look and title
st.set_page_config(page_title="KiryanaOptimizer AI", layout="wide", page_icon="🏪")
st.title("🏪 KiryanaOptimizer AI: Predictive Stocking Dashboard")
st.markdown("Optimize stock levels, prevent waste, and predict weekly consumer demand using machine learning.")

st.write("---")

# 3. Create the input fields in the Sidebar
st.sidebar.header("Input Store Constraints")

# Dropdown matching your actual shop items
selected_product = st.sidebar.selectbox("Select Kiryana Product", [
    'Loose Basmati Rice 1kg', 'Wagh Bakri Tea 500g', 'Haldiram Bhujia 400g', 
    'Good Day Biscuits Choco', 'Dettol Liquid Soap Refill', 'Amul Masti Dahi 400g'
])

current_stock = st.sidebar.number_input("Current Stock Units in Shop", min_value=0, value=10, step=1)
is_weekend = st.sidebar.checkbox("Is an upcoming weekend/festival approaching?")

# 4. Process Inputs automatically into the format the Machine Learning model expects
current_month = datetime.now().month
day_of_week = datetime.now().weekday()

# Create a dictionary matching our trained features, filled with zeros initially
input_data = {feat: 0 for feat in model_features}

# Fill in the numerical details the user gave us
input_data['Price_Per_Unit'] = 100  # Default fallback placeholder price
input_data['Current_Stock'] = current_stock
input_data['Month'] = current_month
input_data['Day_of_Week'] = day_of_week
input_data['Is_Weekend'] = 1 if is_weekend else 0

# Set the matching one-hot encoded product column to 1 (this is how the model knows which item it is)
prod_col = f"Product_Name_{selected_product}"
if prod_col in input_data:
    input_data[prod_col] = 1

# Convert our inputs into a Pandas DataFrame row
input_df = pd.DataFrame([input_data])

# 5. The "Calculate" Button and Prediction Output
if st.button("🔮 Calculate Predictive Demand & Stock Action"):
    
    # Pass the user's inputs to the machine learning model to get the prediction
    predicted_demand = int(np.round(model.predict(input_df)[0]))
    
    # Business logic calculation: Check if we have enough stock
    stock_difference = predicted_demand - current_stock
    
    # Display neat visual summary blocks (Metrics)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Predicted Demand (Next 7 Days)", value=f"{predicted_demand} Units")
    with col2:
        st.metric(label="Current Inventory", value=f"{current_stock} Units")
    with col3:
        if stock_difference > 0:
            st.metric(label="Reorder Status", value=f"Buy {stock_difference} Units", delta="Stock Shortage", delta_color="inverse")
        else:
            st.metric(label="Reorder Status", value="Optimal", delta="Stock Sufficient")

    st.write("---")
    
    # 6. Automated Business Recommendation Banners
    st.write("### 📋 Recommended Actions for Your Shop:")
    if stock_difference > 0:
        st.warning(f"⚠️ **Action Needed:** Your current stock of **{selected_product}** ({current_stock} units) is lower than the predicted demand ({predicted_demand} units). Order at least **{stock_difference} more units** from your distributor immediately to avoid running out!")
    else:
        st.success(f"✅ **Action Optimal:** Your stock of **{selected_product}** is safe. You have sufficient inventory to cover the predicted demand for the coming week. No need to spend extra money stocking this right now.")