import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('ai4i2020.csv')

df = load_data()

if df is not None:
    st.title("Machine Failure Insights")

    # Calculate Power and Heat
    df['Power'] = df['Torque [Nm]'] * df['Rotational speed [rpm]']
    df['Heat'] = df['Air temperature [K]'] - df['Process temperature [K]']

    # 1. Top Product IDs by Machine Failure When it's 1 or Yes
    st.header("1. Top Product IDs by Machine Failure When there's a Machine Failure")
    failure_product_ids = df[df['Machine failure'] == 1]['Product ID'].value_counts().nlargest(5).reset_index()
    failure_product_ids.columns = ['Product ID', 'Failure Count']
    fig1 = px.bar(failure_product_ids, x='Product ID', y='Failure Count',
                  title='Top 5 Product IDs by Machine Failure',
                  labels={'Failure Count': 'Number of Failures'}, 
                  color='Product ID')
    st.plotly_chart(fig1)

    # 2. Top 3 Product Types by Failures
    st.header("2. Top 3 Product Types by Count of Machine Failure when it's 1 or Yes")
    top_types = df[df['Machine failure'] == 1]['Type'].value_counts().nlargest(3).reset_index()
    top_types.columns = ['Type', 'Failure Count']
    fig2 = px.bar(top_types, x='Type', y='Failure Count',
                  title='Top 3 Product Types by Failures',
                  labels={'Failure Count': 'Number of Failures'}, 
                  color='Type')
    st.plotly_chart(fig2)

    # 3. Distribution of Failure Types by Machine Type (Bar Chart)
    st.header("3. Distribution Types of Failures Count of Machine Failure when Machine Failure is Yes by Machine Type")
    failure_columns = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
    df['Failure Type'] = df[failure_columns].idxmax(axis=1)
    failures_by_type_machine = df[df['Machine failure'] == 1].groupby(['Type', 'Failure Type'])['UDI'].count().reset_index()
    failures_by_type_machine.columns = ['Type', 'Failure Type', 'Count']

    fig4 = px.bar(failures_by_type_machine, x='Type', y='Count', color='Failure Type',
                  title='Distribution of Failure Types by Machine Type',
                  labels={'Count': 'Number of Failures'},
                  barmode='group')
    st.plotly_chart(fig4)

    fig5 = px.pie(failures_by_type_machine, names='Failure Type', values='Count',
                  title='Distribution of Failure Types by Machine Type',
                  facet_col='Type', color='Failure Type')
    st.plotly_chart(fig5)

    # 4. Bar Comparison of Median Tool Wear [min] by Machine Type
    st.header("4. Bar Comparison of Median Tool Wear by Machine Type")
    median_tool_wear = df.groupby('Type')['Tool wear [min]'].median().reset_index()
    fig6 = px.bar(median_tool_wear, x='Type', y='Tool wear [min]',
                  title='Median Tool Wear by Machine Type',
                  labels={'Tool wear [min]': 'Median Tool Wear [min]'}, 
                  color='Type')
    st.plotly_chart(fig6)

    # 5. Top 5 Product IDs with the Highest Average Power
    st.header("5. Top 5 Product IDs with the Highest Average Power")
    power_product_ids = df.groupby('Product ID')['Power'].mean().nlargest(5).reset_index()
    power_product_ids.columns = ['Product ID', 'Average Power']
    fig7 = px.bar(power_product_ids, x='Product ID', y='Average Power',
                  title='Top 5 Product IDs by Average Power',
                  labels={'Average Power': 'Average Power (W)'}, 
                  color='Product ID')
    st.plotly_chart(fig7)

    # 6. Types of Machines with the Highest Median Heat
    st.header("6. Types of Machines with the Highest Median Heat")
    heat_by_type = df.groupby('Type')['Heat'].median().reset_index()
    heat_by_type.columns = ['Type', 'Median Heat']
    fig8 = px.bar(heat_by_type, x='Type', y='Median Heat',
                  title='Median Heat by Machine Type',
                  labels={'Median Heat': 'Median Heat (K)'}, 
                  color='Type')
    st.plotly_chart(fig8)

else:
    st.error("Data not loaded. Cannot proceed with analysis.")
