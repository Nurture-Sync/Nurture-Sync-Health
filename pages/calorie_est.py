import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import requests
import matplotlib.pyplot as plt

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
            calories = food_item.get("nf_calories", 0)
            protein = food_item.get("nf_protein", 0)
            fat = food_item.get("nf_total_fat", 0)
            carbs = food_item.get("nf_total_carbohydrate", 0)
            fibre = food_item.get("nf_dietary_fiber", 0)
            return calories, protein, fat, carbs, fibre
    return 0, 0, 0, 0, 0

# Function to plot macronutrient distribution
def plot_nutrient_distribution(protein, fat, carbs, fibre):
    labels = ["Protein", "Fat", "Carbs", "Fibre"]
    values = [protein, fat, carbs, fibre]
    
    # Handle NaN values and ensure no division errors occur
    values = [0 if value is None or np.isnan(value) else value for value in values]
    
    # Check if all values are zero to avoid an empty pie chart
    if all(value == 0 for value in values):
        st.write("No valid nutrient data available to display.")
        return
    
    colors = ["#4CAF50", "#FFC107", "#FF5722", "#8BC34A"]

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title("Macronutrient Distribution")
    st.pyplot(plt)

# Streamlit UI
st.title("Nutrify Sync - Food Calorie & Nutrition Estimator")
st.write("Enter a food name or upload an image to get calorie and nutrition details.")

# Option to enter food name
food_name = st.text_input("Enter Food Name:")
if food_name:
    calories, protein, fat, carbs, fibre = get_nutrition_info(food_name)
    st.write(f"Calories: {calories} kcal")
    st.write(f"Protein: {protein} g")
    st.write(f"Fat: {fat} g")
    st.write(f"Carbs: {carbs} g")
    st.write(f"Fibre: {fibre} g")
    plot_nutrient_distribution(protein, fat, carbs, fibre)

# Option to upload an image
uploaded_file = st.file_uploader("Or upload a food image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Load and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Preprocess the image for MobileNetV2
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    # Make prediction
    predictions = model.predict(image_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    top_prediction = decoded_predictions[0][1]

    st.write(f"Predicted Food: {top_prediction}")
    calories, protein, fat, carbs, fibre = get_nutrition_info(top_prediction)
    st.write(f"Calories: {calories} kcal")
    st.write(f"Protein: {protein} g")
    st.write(f"Fat: {fat} g")
    st.write(f"Carbs: {carbs} g")
    st.write(f"Fibre: {fibre} g")
    plot_nutrient_distribution(protein, fat, carbs, fibre)
