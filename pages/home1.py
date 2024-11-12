import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
import base64
from streamlit_option_menu import option_menu

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to save uploaded files
def save_uploaded_file(uploaded_file):
    with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())

# Function to get list of uploaded files
def get_uploaded_files():
    files = os.listdir(UPLOAD_FOLDER)
    return files

# Function to generate download link using Streamlit's download_button
def get_download_link(file_path, file_name):
    with open(file_path, 'rb') as f:
        bytes_data = f.read()
    return st.download_button(
        label="Download",
        data=bytes_data,
        file_name=file_name,
        mime='application/octet-stream'
    )

# Report Section
def report():
    st.markdown("""
    <style>
        .report-section {
            background-color: #e3f2fd; /* Light blue background */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .report-title {
            font-size: 36px;
            color: #1976d2; /* Blue */
            text-align: center;
            margin-bottom: 15px;
        }
        .report-description {
            font-size: 18px;
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        .upload-card, .files-card {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .upload-card h3, .files-card h3 {
            font-size: 24px;
            color: #1976d2;
        }
        .files-table {
            margin-top: 10px;
            width: 100%;
            border-collapse: collapse;
        }
        .files-table th, .files-table td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }
        .files-table th {
            background-color: #f1f1f1;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="report-title">Upload and View Reports</h1>', unsafe_allow_html=True)
    st.markdown('<p class="report-description">Upload new reports and view previously uploaded ones. Ensure your reports are in PDF or CSV format.</p>', unsafe_allow_html=True)
    
    # File upload
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<h3>Upload New Report</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file (PDF/CSV)", type=['pdf', 'csv'])
    
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)
        st.success("File uploaded successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display previously uploaded files
    st.markdown('<div class="files-card">', unsafe_allow_html=True)
    st.markdown('<h3>Previous Reports</h3>', unsafe_allow_html=True)
    
    files = get_uploaded_files()
    
    if files:
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            st.markdown(f"**{file}**")
            get_download_link(file_path, file)
            st.markdown("---")
    else:
        st.write("No reports available.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Data Generation Functions
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

# Track Section
def track():
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
            flex-direction: column;
            gap: 20px;
        }
        @media (min-width: 768px) {
            .graph-and-table {
                flex-direction: row;
            }
            .table-container {
                width: 45%;
            }
            .chart-container {
                width: 55%;
            }
        }
    </style>
    """, unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

# Home Section
def home():
    st.markdown("""
    <style>
        .home-section {
            background-color: #f0f8ff; /* Light blue background */
            padding: 20px;
            border-radius: 10px;
        }
        .home-title {
            font-size: 36px;
            color: #0066cc; 
            text-align: center;
            margin-bottom: 15px;
            font-family: 'Roboto', sans-serif;
        }
        .home-description {
            font-size: 18px;
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            font-family: 'Roboto', sans-serif;
        }
        .stats-box {
            background-color: #e6f7ff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            color: #005580;
            font-size: 18px;
        }
        .section-header {
            font-size: 24px;
            color: #004d99;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="home-title">Welcome to HealthApp for Thyroid and Diabetics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="home-description">Your personalized healthcare companion for managing thyroid levels and diabetes. Track your health, get lifestyle tips, and consult with specialists to stay on top of your health journey.</p>', unsafe_allow_html=True)
    
    # Quick stats section
    st.markdown('<div class="section-header">Daily Health Insights</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    col1.markdown('<div class="stats-box">Blood Sugar: 120 mg/dL</div>', unsafe_allow_html=True)
    col2.markdown('<div class="stats-box">Thyroid Levels: 4.5 μIU/mL</div>', unsafe_allow_html=True)
    col3.markdown('<div class="stats-box">BMI: 24.3 kg/m²</div>', unsafe_allow_html=True)
    
    # Educational Tips
    st.markdown('<div class="section-header">Daily Tips for Better Health</div>', unsafe_allow_html=True)
    st.write("💡 **Tip of the day:** Incorporate more fiber into your meals to regulate blood sugar levels effectively.")
    
    # Graphs Section
    st.markdown('<div class="section-header">Track Your Health</div>', unsafe_allow_html=True)
    
    # Weight Tracking Graph
    st.write("### Weight Tracking Over Time")
    weight_data = generate_weight_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weight_data['Date'], y=weight_data['Weight'], 
                             mode='lines+markers', marker=dict(size=8, color='skyblue'),
                             line=dict(color='skyblue'), name='Weight',
                             hoverinfo='text', 
                             text=[f"Weight: {wt} kg" for wt in weight_data['Weight']]))
    fig.update_layout(title='Weight Tracking Over Time', xaxis_title='Date', yaxis_title='Weight (kg)', 
                      hovermode='x')
    st.plotly_chart(fig, use_container_width=True)
    
    # Food Calories Graph
    st.write("### Food Calories Over Time")
    calories_data = generate_calories_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=calories_data['Date'], y=calories_data['Calories'], 
                             mode='lines+markers', marker=dict(size=8, color='salmon'),
                             line=dict(color='salmon'), name='Calories',
                             hoverinfo='text', 
                             text=[f"Calories: {cal} kcal" for cal in calories_data['Calories']]))
    fig.update_layout(title='Food Calories Over Time', xaxis_title='Date', yaxis_title='Calories (kcal)', 
                      hovermode='x')
    st.plotly_chart(fig, use_container_width=True)

    # Share Information Button
    st.markdown('<div class="section-header">Share Your Information</div>', unsafe_allow_html=True)
    if st.button('Share Information'):
        # Display the link to share when button is clicked
        st.markdown("### Share Your Health Metrics")
        shareable_link = generate_dummy_link()  # Simulate the generation of a shareable link
        st.text_input("Copy this link to share:", value=shareable_link, readonly=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_weight_data():
    dates = pd.date_range(start="2023-01-01", periods=10, freq='W')
    weights = np.random.randint(60, 80, size=10)
    return pd.DataFrame({'Date': dates, 'Weight': weights})

def generate_calories_data():
    dates = pd.date_range(start="2023-01-01", periods=10, freq='W')
    calories = np.random.randint(1500, 2500, size=10)
    return pd.DataFrame({'Date': dates, 'Calories': calories})

def generate_dummy_link():
    return "https://your-app-url.com/shared-metrics"

# Main Navigation
def main():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Track", "Report"],
            icons=["house", "activity", "file-earmark-arrow-down"],  # Optional: Add icons
            menu_icon="cast",  # Optional: Menu icon
            default_index=0,
            #orientation="horizontal" ,  
        )
    
    if selected == "Home":
        home()
    elif selected == "Track":
        track()
    elif selected == "Report":
        report()

if __name__ == "__main__":
    main()
