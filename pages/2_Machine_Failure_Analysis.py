import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset and drop the 'Unnamed: 0' column if it exists
df = pd.read_csv('ai4i2020.csv')
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Drop 'UDI' column
df = df.drop(columns='UDI', errors='ignore')

# Excluded columns where 1 and 0 will be replaced with 'Yes' and 'No'
excluded_columns = ['Machine failure', 'OSF', 'TWF', 'PWF', 'RNF', 'HDF']

# Replace 1 and 0 with 'Yes' and 'No' in the excluded columns
df[excluded_columns] = df[excluded_columns].replace({1: 'Yes', 0: 'No'})

# Calculate new features
df['Power'] = df['Torque [Nm]'] * df['Rotational speed [rpm]']
df['Heat'] = df['Air temperature [K]'] - df['Process temperature [K]']
df['OverStrain'] = df['Tool wear [min]'] * df['Torque [Nm]']

# Sidebar for visualization type
st.sidebar.header("Visualization Type")
chart_type = st.sidebar.selectbox("Choose a chart type", ["Bar", "Line", "Pie"])

# Univariate Analysis
st.header("Univariate Analysis")

# Filter out 'Product ID' from the selectable columns
univariate_columns = [col for col in df.columns if col != 'Product ID']
univariate_col = st.selectbox("Select a column for univariate analysis", univariate_columns)

if univariate_col in df.columns:
    # Filter the top 20 for univariate analysis
    univariate_data = df[univariate_col].value_counts().reset_index().head(20)
    univariate_data.columns = [univariate_col, 'Count']

    # Sorting the univariate data correctly based on the selected column
    if chart_type == "Bar":
        fig = px.bar(univariate_data, x=univariate_col, y='Count', color=univariate_col)
        st.plotly_chart(fig)
    elif chart_type == "Line":
        univariate_data = univariate_data.sort_values(by=univariate_col)
        fig = px.line(univariate_data, x=univariate_col, y='Count')
        st.plotly_chart(fig)
    elif chart_type == "Pie":
        fig = px.pie(univariate_data, names=univariate_col, values='Count')
        st.plotly_chart(fig)
else:
    st.warning(f"Column '{univariate_col}' does not exist in the dataset.")

# Bivariate Analysis
st.header("Bivariate Analysis")
bivariate_col1 = st.selectbox("Select first column for bivariate analysis (categorical)", df.select_dtypes(include=['object', 'category']).columns)

# Exclude specified columns from the dropdown
numeric_cols = df.select_dtypes(include=['number']).columns
filtered_columns = [col for col in numeric_cols if col not in excluded_columns]

bivariate_col2 = st.selectbox("Select second column for bivariate analysis (numeric)", filtered_columns, index=1)

# Columns for median analysis (including Heat and OverStrain)
median_columns = ['Process temperature [K]', 'Air temperature [K]', 'Torque [Nm]', 'Tool wear [min]', 'Heat', 'OverStrain']

if bivariate_col2 in numeric_cols and bivariate_col1 in df.columns:
    if bivariate_col2 in median_columns:
        bivariate_data = df.groupby([bivariate_col1])[bivariate_col2].median().reset_index()
    else:
        bivariate_data = df.groupby([bivariate_col1])[bivariate_col2].mean().reset_index()
    bivariate_data = bivariate_data.sort_values(by=bivariate_col2, ascending=False).head(10)

    if chart_type == "Bar":
        fig = px.bar(bivariate_data, x=bivariate_col1, y=bivariate_col2, color=bivariate_col1)
        st.plotly_chart(fig)
    elif chart_type == "Line":
        fig = px.line(bivariate_data, x=bivariate_col1, y=bivariate_col2)
        st.plotly_chart(fig)
    elif chart_type == "Pie":
        fig = px.pie(bivariate_data, names=bivariate_col1, values=bivariate_col2)
        st.plotly_chart(fig)
else:
    st.warning(f"Selected column '{bivariate_col2}' is not numeric or '{bivariate_col1}' does not exist in the dataset.")

# Multivariate Analysis
st.header("Multivariate Analysis")
multivariate_col1 = st.selectbox("Select first column for analysis (categorical)", df.select_dtypes(include=['object', 'category']).columns)

# Filter out categorical columns and the excluded columns for multivariate_col2
filtered_multivariate_columns = [col for col in numeric_cols if col not in excluded_columns]
multivariate_col2 = st.selectbox("Select second column for analysis (numeric)", filtered_multivariate_columns, index=1)

color_col = st.selectbox("Optional: Select a column for color (categorical)", [None] + list(df.select_dtypes(include=['object', 'category']).columns), index=0)

# Ensure only numeric columns are considered for aggregation
if multivariate_col2 in numeric_cols and multivariate_col1 in df.columns:
    try:
        # Check if the selected color column is the same as multivariate_col2
        if color_col and color_col == multivariate_col2:
            st.warning(f"Column '{color_col}' is already selected as the second column for analysis.")
        else:
            if color_col:
                if multivariate_col2 in median_columns:
                    multivariate_data = df.groupby([multivariate_col1, color_col])[multivariate_col2].median().reset_index()
                else:
                    multivariate_data = df.groupby([multivariate_col1, color_col])[multivariate_col2].mean().reset_index()

                multivariate_data = multivariate_data.sort_values(by=multivariate_col2, ascending=False).head(10)

                if chart_type == "Bar":
                    fig = px.bar(multivariate_data, x=multivariate_col1, y=multivariate_col2, color=color_col)
                elif chart_type == "Line":
                    fig = px.line(multivariate_data, x=multivariate_col1, y=multivariate_col2, color=color_col)
                elif chart_type == "Pie":
                    fig = px.pie(multivariate_data, names=multivariate_col1, values=multivariate_col2, color=color_col)
                st.plotly_chart(fig)
            else:
                st.warning("Please select a color column for multivariate analysis.")
    except ValueError as e:
        if "already exists" in str(e):
            st.error(f"ValueError: {e}. The column '{multivariate_col2}' cannot be used as a color column because it already exists in the DataFrame.")
        else:
            st.error(f"An unexpected error occurred: {e}")
else:
    st.warning(f"Selected column '{multivariate_col2}' is not numeric or '{multivariate_col1}' does not exist in the dataset.")
