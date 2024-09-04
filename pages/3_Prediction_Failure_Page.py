import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.model_selection import GridSearchCV

# Load pre-trained model (replace with the actual model path)
model = joblib.load('xgb_grid.pkl')

# Load and prepare initial dataset to determine preprocessing requirements
ai = pd.read_csv('ai4cleaned.csv')

# Separate features and target
X = ai.drop('Machine failure', axis=1)
y = ai['Machine failure']

# Streamlit App
st.title('Machine Failure Prediction')

# Manual inputs for each feature
st.header('Input Data Manually')

manual_input = {}

# Define mapping for 'L', 'M', 'H' to 1, 2, 3
mapping = {'L': 1, 'M': 2, 'H': 3}

# Generate input fields based on column types
for col in X.columns:
    if col == "Type":  # Assuming 'Type' is the column you want to map
        type_input = st.selectbox(f"Enter value for {col}", ['L', 'M', 'H'])
        manual_input[col] = mapping[type_input]
    elif col in ["TWF", "HDF", "PWF", "OSF", "RNF"]:  # Set these columns as int inputs
        manual_input[col] = st.number_input(f"Enter integer value for {col}", min_value=0, step=1, value=int(X[col].mean()))
    else:
        manual_input[col] = st.number_input(f"Enter value for {col}", value=float(X[col].mean()))

# Convert the manual input into a DataFrame
manual_input_df = pd.DataFrame([manual_input])

# Display input data
st.write("Manual Input Data:", manual_input_df)

# Fit the scaler on the entire dataset (X) and transform the manual input data
scaler = StandardScaler()
scaler.fit(X)
manual_input_df_scaled = scaler.transform(manual_input_df)

# Add a button to trigger prediction
if st.button('Predict'):
    # Make predictions using the preprocessed input data
    prediction = model.predict(manual_input_df_scaled)

    # Convert the prediction to text and assign color
    if prediction[0] == 1:
        prediction_text = "<span style='color: green;'>Yes, there's a machine failure</span>"
    else:
        prediction_text = "<span style='color: red;'>No, there's not a machine failure</span>"

    # Display prediction result with markdown to support HTML
    st.markdown(f"**Prediction:** {prediction_text}", unsafe_allow_html=True)
