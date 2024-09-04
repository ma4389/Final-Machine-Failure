import streamlit as st
import pandas as pd

# Title and Header
st.markdown("<h1 style='text-align: center; color: #191970;'>Machine Failure Data Visualization Dashboard</h1>", unsafe_allow_html=True)

# Image related to machine failure
image_url = "https://gesrepair.com/wp-content/uploads/35DDEBA8-EA7C-4121-AC06-CEBA29C56D07-1024x592.jpeg"  # Replace with an actual image URL related to machine failure
st.image(image_url, use_column_width=True)

# Introduction and dataset description
st.markdown(''' 
            * This web application presents an Exploratory Data Analysis (EDA) visualization for a Machine Failure Dataset.
            * The data is obtained from [Kaggle](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020/data).
            * You can select one of the options from the sidebar to explore the data.''')

st.markdown("""
This Machine Failure Dashboard likely contains information about various machines and their failure instances. It may include columns such as:
* **UDI:** Unique identifier for each data entry.
* **Product ID:** Identifier for the product.
* **Type:** Type of product (e.g., M, L).
* **Air temperature [K]:** Air temperature during the process.
* **Process temperature [K]:** Temperature of the process.
* **Rotational speed [rpm]:** Speed of the machine.
* **Torque [Nm]:** Torque applied during the process.
* **Tool wear [min]:** Tool wear time.
* **Machine failure:** Whether there was a machine failure (1 = Yes, 0 = No).
* **TWF:** Tool wear failure.
* **HDF:** Heat dissipation failure.
* **PWF:** Power failure.
* **OSF:** Overstrain failure.
* **RNF:** Random failures.

**Additional characteristics:**

* The number of columns and their exact names might vary depending on the specific dataset.
* The code assumes the presence of a "Machine ID" column, which is used for visualizations based on machine failure trends (e.g., most frequent failure types).
* It's possible there are other columns containing additional machine-related information not explicitly mentioned in the code (e.g., machine location, usage hours).

**Overall, this dataset seems suitable for analyzing machine failures and identifying trends based on various factors like failure type, machine age, and maintenance cost.**
""")

# Load the machine failure dataset
machine_failure = pd.read_csv('ai4i2020.csv')  # Replace with the actual file name

machine_failure.dropna(inplace=True)
st.subheader('Here is a Sample of the Dataset')
if st.checkbox('Show Dataset'):
    st.dataframe(machine_failure.head(5))
