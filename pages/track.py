import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Sample data generation functions
def generate_activity_data():
    dates = pd.date_range(start="2023-01-01", periods=10, freq='D')
    steps = np.random.randint(5000, 15000, size=10)
    sleep_hours = np.random.uniform(5, 9, size=10)
    hydration_liters = np.random.uniform(1.5, 3.5, size=10)
    data = pd.DataFrame({
        'Date': dates,
        'Steps': steps,
        'Sleep (hours)': sleep_hours,
        'Hydration (liters)': hydration_liters
    })
    data['Day'] = data['Date'].dt.day_name()
    return data

def generate_diabetic_data():
    dates = pd.date_range(start="2023-01-01", periods=10, freq='D')
    glucose_levels = np.random.randint(70, 180, size=10)
    data = pd.DataFrame({
        'Date': dates,
        'Blood Glucose (mg/dL)': glucose_levels
    })
    data['Day'] = data['Date'].dt.day_name()
    return data

def generate_thyroid_data():
    dates = pd.date_range(start="2023-01-01", periods=10, freq='D')
    medication_doses = np.random.uniform(0.5, 1.5, size=10)
    data = pd.DataFrame({
        'Date': dates,
        'Thyroid Medication (mg)': medication_doses
    })
    data['Day'] = data['Date'].dt.day_name()
    return data

# Custom CSS for styling
st.markdown("""
<style>
    .track-section {
        background-color: #f1f8e9; /* Light green background */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .track-title {
        font-size: 36px;
        color: #388e3c; /* Dark green */
        text-align: center;
        margin-bottom: 15px;
    }
    .track-description {
        font-size: 18px;
        color: #333;
        text-align: center;
        margin-bottom: 20px;
    }
    .track-card {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .track-card h3 {
        font-size: 24px;
        color: #388e3c;
    }
    .graph-and-table {
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }
    .table-container {
        width: 45%;
    }
</style>
""", unsafe_allow_html=True)

# Track Section
def track():
    st.markdown('<div class="track-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="track-title">Track Your Activities</h1>', unsafe_allow_html=True)
    st.markdown('<p class="track-description">Monitor your daily activities, including steps, sleep, hydration, blood glucose levels, and thyroid medication. Visualize your progress over time and check detailed daily records.</p>', unsafe_allow_html=True)
    
    # Generate sample data
    activity_data = generate_activity_data()
    diabetic_data = generate_diabetic_data()
    thyroid_data = generate_thyroid_data()

    # Steps Tracking
    st.markdown('<div class="track-card">', unsafe_allow_html=True)
    st.markdown('<h3>Steps Tracking</h3>', unsafe_allow_html=True)
    st.markdown('<div class="graph-and-table">', unsafe_allow_html=True)
    
    # Graph for Steps
    fig_steps = px.line(activity_data, x='Date', y='Steps', 
                        title='Daily Steps Tracking',
                        labels={'Steps': 'Steps'},
                        markers=True,
                        line_shape='spline',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_steps.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_steps, use_container_width=True)
    
    # Table for Steps
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.write(activity_data[['Day', 'Date', 'Steps']])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sleep Tracking
    st.markdown('<div class="track-card">', unsafe_allow_html=True)
    st.markdown('<h3>Sleep Tracking</h3>', unsafe_allow_html=True)
    st.markdown('<div class="graph-and-table">', unsafe_allow_html=True)

    # Graph for Sleep
    fig_sleep = px.line(activity_data, x='Date', y='Sleep (hours)', 
                        title='Daily Sleep Tracking',
                        labels={'Sleep (hours)': 'Sleep (hours)'},
                        markers=True,
                        line_shape='spline',
                        color_discrete_sequence=px.colors.qualitative.Set1)
    fig_sleep.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_sleep, use_container_width=True)
    
    # Table for Sleep
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.write(activity_data[['Day', 'Date', 'Sleep (hours)']])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Hydration Tracking
    st.markdown('<div class="track-card">', unsafe_allow_html=True)
    st.markdown('<h3>Hydration Tracking</h3>', unsafe_allow_html=True)
    st.markdown('<div class="graph-and-table">', unsafe_allow_html=True)

    # Graph for Hydration
    fig_hydration = px.line(activity_data, x='Date', y='Hydration (liters)', 
                            title='Daily Hydration Tracking',
                            labels={'Hydration (liters)': 'Hydration (liters)'},
                            markers=True,
                            line_shape='spline',
                            color_discrete_sequence=px.colors.qualitative.Dark2)
    fig_hydration.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_hydration, use_container_width=True)
    
    # Table for Hydration
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.write(activity_data[['Day', 'Date', 'Hydration (liters)']])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Blood Glucose Tracking
    st.markdown('<div class="track-card">', unsafe_allow_html=True)
    st.markdown('<h3>Blood Glucose Tracking</h3>', unsafe_allow_html=True)
    st.markdown('<div class="graph-and-table">', unsafe_allow_html=True)

    # Graph for Blood Glucose
    fig_diabetes = px.line(diabetic_data, x='Date', y='Blood Glucose (mg/dL)', 
                           title='Daily Blood Glucose Levels',
                           labels={'Blood Glucose (mg/dL)': 'Blood Glucose (mg/dL)'},
                           markers=True,
                           line_shape='spline',
                           color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_diabetes.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_diabetes, use_container_width=True)
    
    # Table for Blood Glucose
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.write(diabetic_data[['Day', 'Date', 'Blood Glucose (mg/dL)']])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Thyroid Medication Tracking
    st.markdown('<div class="track-card">', unsafe_allow_html=True)
    st.markdown('<h3>Thyroid Medication Doses Tracking</h3>', unsafe_allow_html=True)
    st.markdown('<div class="graph-and-table">', unsafe_allow_html=True)

    # Graph for Thyroid Medication
    fig_thyroid = px.line(thyroid_data, x='Date', y='Thyroid Medication (mg)', 
                          title='Daily Thyroid Medication Doses',
                          labels={'Thyroid Medication (mg)': 'Thyroid Medication (mg)'},
                          markers=True,
                          line_shape='spline',
                          color_discrete_sequence=px.colors.qualitative.Prism)
    fig_thyroid.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_thyroid, use_container_width=True)
    
    # Table for Thyroid Medication
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.write(thyroid_data[['Day', 'Date', 'Thyroid Medication (mg)']])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Calling the track section
track()
