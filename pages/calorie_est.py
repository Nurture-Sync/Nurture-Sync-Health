import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.applications import MobileNetV2, preprocess_input, decode_predictions
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Set a consistent style for matplotlib using Seaborn's theme
sns.set_theme(style="whitegrid")

# Load the pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

# Nutritionix API credentials
app_id = "be2cc170"
app_key = "94c0787b3419a34286acf0552848d866"

# Function to get nutrition information from Nutritionix API
def get_nutrition_info(food_name):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": app_id,
        "x-app-key": app_key,
        "Content-Type": "application/json"
    }
    data = {"query": food_name}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        nutrition_data = response.json()
        if "foods" in nutrition_data and len(nutrition_data["foods"]) > 0:
            food_item = nutrition_data["foods"][0]
            return (
                food_item.get("nf_calories", 0),
                food_item.get("nf_protein", 0),
                food_item.get("nf_total_fat", 0),
                food_item.get("nf_total_carbohydrate", 0),
                food_item.get("nf_dietary_fiber", 0)
            )
    return 0, 0, 0, 0, 0

# Function to plot macronutrient distribution with professional styling
def plot_nutrient_distribution(protein, fat, carbs, fibre):
    labels = ["Protein", "Fat", "Carbs", "Fibre"]
    values = [protein, fat, carbs, fibre]
    values = [0 if value is None else value for value in values]
    
    if all(value == 0 for value in values):
        st.write("No valid nutrient data available to display.")
        return
    
    colors = ["#6DAEDB", "#FDB927", "#FF6B6B", "#4ECDC4"]  # Professional healthcare-inspired colors

    fig, ax = plt.subplots(figsize=(5, 5), facecolor="white")
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90,
        textprops=dict(color="black"), pctdistance=0.85
    )
    
    # Circle for 'donut' appearance
    center_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig.gca().add_artist(center_circle)
    
    # Title and style adjustments
    ax.set_title("Macronutrient Distribution", fontsize=16, color="#3E5C76")
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=11)
    st.pyplot(fig)

# Streamlit UI with professional styling
st.markdown("""
    <style>
        .stApp {
            background-color: #F0F4F8;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 32px;
            color: #3E5C76;
            font-weight: bold;
        }
        .subtitle {
            font-size: 18px;
            color: #6DAEDB;
        }
        .stButton>button {
            background-color: #3E5C76;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
        .stTextInput, .stFileUploader {
            background-color: #ffffff;
            color: #3E5C76;
            border: 1px solid #B0BEC5;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Nutrify Sync - Calorie & Nutrition Estimator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A smart and reliable way to understand your food's nutrition profile</p>", unsafe_allow_html=True)

# Option to enter food name
food_name = st.text_input("Enter Food Name:")
if food_name:
    calories, protein, fat, carbs, fibre = get_nutrition_info(food_name)
    st.write(f"**Calories:** {calories} kcal")
    st.write(f"**Protein:** {protein} g")
    st.write(f"**Fat:** {fat} g")
    st.write(f"**Carbs:** {carbs} g")
    st.write(f"**Fibre:** {fibre} g")
    plot_nutrient_distribution(protein, fat, carbs, fibre)

# Option to upload an image
uploaded_file = st.file_uploader("Or upload a food image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    top_prediction = decoded_predictions[0][1]

    st.write(f"**Predicted Food:** {top_prediction}")
    calories, protein, fat, carbs, fibre = get_nutrition_info(top_prediction)
    st.write(f"**Calories:** {calories} kcal")
    st.write(f"**Protein:** {protein} g")
    st.write(f"**Fat:** {fat} g")
    st.write(f"**Carbs:** {carbs} g")
    st.write(f"**Fibre:** {fibre} g")
    plot_nutrient_distribution(protein, fat, carbs, fibre)
