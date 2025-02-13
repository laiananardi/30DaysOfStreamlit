import streamlit as st
import pandas as pd
import altair as alt

# https://www.kaggle.com/datasets/yasserh/titanic-dataset

# App Title
st.title(":bar_chart: Interactive Data Explorer")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    # Show progress bar while loading the file
    progress_bar = st.progress(0)
    df = pd.read_csv(uploaded_file)
    progress_bar.progress(100)
    st.success("File uploaded successfully!")

    # Show raw data
    with st.expander(":page_facing_up: View Raw Data"):
        st.write(df)

    # Show summary statistics
    st.subheader(":memo: Summary Statistics")
    st.write(df.describe())

    
    # Select Columns to Display
    st.header(":wrench: Data Exploration")
    selected_columns = st.multiselect("Select columns to display", df.columns, default=df.columns.tolist())
    df_filtered = df[selected_columns]
    st.write(df_filtered)

    # Categorical Filter
    categorical_columns = df_filtered.select_dtypes(include=['object']).columns.tolist()
    if categorical_columns:
        st.subheader(":mag_right: Categorical Filters")
        selected_category = st.selectbox("Filter by a categorical column", ["No Filter"] + categorical_columns)
        
        if selected_category != "No Filter":
            unique_values = df_filtered[selected_category].unique()
            selected_value = st.selectbox("Select a value", ["No Filter"] + list(unique_values))
            
            if selected_value != "No Filter":
                df_filtered = df_filtered[df_filtered[selected_category] == selected_value]
        
        st.write(df_filtered)

    # Numerical Filter
    numerical_columns = df_filtered.select_dtypes(include=['number']).columns.tolist()
    if numerical_columns:
        st.subheader(":mag_right: Numerical Filters")
        apply_numeric_filter = st.checkbox("Enable Numerical Filter")
        
        if apply_numeric_filter:
            selected_numeric = st.selectbox("Filter by a numerical column", numerical_columns)
            min_val, max_val = df_filtered[selected_numeric].min(), df_filtered[selected_numeric].max()
            numeric_range = st.slider("Select range", min_val, max_val, (min_val, max_val))
            
            df_filtered = df_filtered[(df_filtered[selected_numeric] >= numeric_range[0]) & 
                                    (df_filtered[selected_numeric] <= numeric_range[1])]
        
        st.write(df_filtered)


    # Outlier Detection Section
    st.subheader(":rotating_light: Outlier Detection (IQR Method)")
    if numerical_columns:
        selected_outlier_column = st.selectbox("Select a numerical column for outlier detection", numerical_columns)
        
        # Calculate Q1, Q3, and IQR
        Q1 = df_filtered[selected_outlier_column].quantile(0.25)
        Q3 = df_filtered[selected_outlier_column].quantile(0.75)
        IQR = Q3 - Q1

        # Determine the outliers based on IQR
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df_filtered[(df_filtered[selected_outlier_column] < lower_bound) | (df_filtered[selected_outlier_column] > upper_bound)]
        
        # Display outliers if they exist
        if not outliers.empty:
            st.write(f"Outliers detected in {selected_outlier_column}:")
            st.write(outliers)
        else:
            st.write(f"No outliers detected in {selected_outlier_column}.")


    # Visualization Section
    st.subheader(":chart_with_upwards_trend: Data Visualization")

    if numerical_columns or categorical_columns:
        chart_type = st.radio("Select chart type", ["Bar Chart", "Line Chart", "Scatter Plot"])
        
        if chart_type == "Bar Chart":
            x_options = numerical_columns + categorical_columns  # Allow both types
            chart_column_x = st.selectbox("Select X-axis", x_options)

            y_options = ["Count"] + numerical_columns  # Allow count for categorical
            chart_column_y = st.selectbox("Select Y-axis", y_options)

            # Define chart encoding
            chart = alt.Chart(df_filtered).mark_bar().encode(
                x=chart_column_x,
                y="count()" if chart_column_y == "Count" else chart_column_y,
                tooltip=[chart_column_x, chart_column_y] if chart_column_y != "Count" else [chart_column_x]
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

        elif chart_type == "Line Chart":
            x_options = numerical_columns + categorical_columns
            y_options = numerical_columns
            chart_column_x = st.selectbox("Select X-axis", x_options)
            chart_column_y = st.selectbox("Select Y-axis", y_options)

            chart = alt.Chart(df_filtered).mark_line().encode(
                x=chart_column_x,
                y=chart_column_y,
                tooltip=[chart_column_x, chart_column_y]
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

        elif chart_type == "Scatter Plot":
            x_options = numerical_columns
            y_options = numerical_columns
            color_options = numerical_columns + categorical_columns  # Allow categorical for coloring

            chart_column_x = st.selectbox("Select X-axis", x_options)
            chart_column_y = st.selectbox("Select Y-axis", y_options)
            chart_column_color = st.selectbox("Select Color", color_options)

            chart = alt.Chart(df_filtered).mark_point().encode(
                x=chart_column_x,
                y=chart_column_y,
                color=chart_column_color,
                tooltip=[chart_column_x, chart_column_y, chart_column_color]
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("No columns available for visualization.")

else:
    st.info("Please upload a CSV file to get started.")