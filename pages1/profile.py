import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
import base64
from streamlit_option_menu import option_menu

def home1():
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

