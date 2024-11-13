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

def est2():
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
    st.title("Nutrify Sync - Your Personal Nutrition Tracker")
    st.write("Add multiple food items with quantities to get their total calorie and nutrition details.")

    # Initialize a session state to store the list of foods
    if "food_list" not in st.session_state:
        st.session_state.food_list = []

    # Initialize session state to track daily progress
    if "total_calories" not in st.session_state:
        st.session_state.total_calories = 0
        st.session_state.total_protein = 0
        st.session_state.total_fat = 0
        st.session_state.total_carbs = 0
        st.session_state.total_fibre = 0

    # Function to add food to the list
    def add_food_to_list(food_name, quantity, unit):
        if food_name and quantity:
            calories, protein, fat, carbs, fibre = get_nutrition_info(food_name)
            
            # Adjust values based on quantity and unit (assuming quantity is in grams or bowls)
            if unit == "grams":
                # If the unit is in grams, calculate nutrition based on the entered quantity
                calories = calories * (quantity / 100)
                protein = protein * (quantity / 100)
                fat = fat * (quantity / 100)
                carbs = carbs * (quantity / 100)
                fibre = fibre * (quantity / 100)
            elif unit == "bowls":
                # Assume 1 bowl = 200 grams (adjust this based on your preference)
                quantity_in_grams = quantity * 200
                calories = calories * (quantity_in_grams / 100)
                protein = protein * (quantity_in_grams / 100)
                fat = fat * (quantity_in_grams / 100)
                carbs = carbs * (quantity_in_grams / 100)
                fibre = fibre * (quantity_in_grams / 100)
            elif unit == "count":
                # Assume 1 count = 100 grams for simplicity (you can adjust this as needed)
                calories = calories * (quantity / 1)
                protein = protein * (quantity / 1)
                fat = fat * (quantity / 1)
                carbs = carbs * (quantity / 1)
                fibre = fibre * (quantity / 1)
            
            st.session_state.food_list.append({"food": food_name, "quantity": quantity, "unit": unit, "calories": calories, 
                                            "protein": protein, "fat": fat, "carbs": carbs, "fibre": fibre})
            st.session_state.total_calories += calories
            st.session_state.total_protein += protein
            st.session_state.total_fat += fat
            st.session_state.total_carbs += carbs
            st.session_state.total_fibre += fibre
            st.success(f"Added {quantity} {unit} of {food_name} to the list!")

    # Function to delete a specific food entry
    def delete_food_entry(index):
        food = st.session_state.food_list[index]
        st.session_state.food_list.pop(index)
        st.session_state.total_calories -= food["calories"]
        st.session_state.total_protein -= food["protein"]
        st.session_state.total_fat -= food["fat"]
        st.session_state.total_carbs -= food["carbs"]
        st.session_state.total_fibre -= food["fibre"]
        st.success(f"Deleted {food['food']} from the list.")

    # Function to reset all entries
    def reset_all():
        st.session_state.food_list = []
        st.session_state.total_calories = 0
        st.session_state.total_protein = 0
        st.session_state.total_fat = 0
        st.session_state.total_carbs = 0
        st.session_state.total_fibre = 0
        st.success("All data has been reset!")

    # Input for food name and quantity
    food_name = st.text_input("Enter a Food Item:")
    quantity = st.number_input("Enter the Quantity:", min_value=1, step=1)
    unit = st.selectbox("Select the Unit of Quantity:", ["grams", "bowls", "count"])

    # Add food when "+" button is clicked
    if st.button("Add Food (+)"):
        add_food_to_list(food_name, quantity, unit)

    # Reset button for all entries
    if st.button("Reset All Data"):
        reset_all()

    # Display the list of entered foods with quantities and nutrition
    if st.session_state.food_list:
        st.subheader("Foods Entered:")
        for i, food in enumerate(st.session_state.food_list, 1):
            st.write(f"{i}. {food['food']} - {food['quantity']} {food['unit']}")
            st.write(f"   Calories: {food['calories']} kcal, Protein: {food['protein']} g, Fat: {food['fat']} g, Carbs: {food['carbs']} g, Fibre: {food['fibre']} g")
            
            # Add a delete button for each individual entry
            if st.button(f"Delete {food['food']}"):
                delete_food_entry(i - 1)

    # Show daily progress
    st.subheader("Daily Progress")
    st.write(f"**Total Calories**: {st.session_state.total_calories} kcal")
    st.write(f"**Total Protein**: {st.session_state.total_protein} g")
    st.write(f"**Total Fat**: {st.session_state.total_fat} g")
    st.write(f"**Total Carbs**: {st.session_state.total_carbs} g")
    st.write(f"**Total Fibre**: {st.session_state.total_fibre} g")

    # Plot the total macronutrient distribution
    plot_nutrient_distribution(st.session_state.total_protein, st.session_state.total_fat, st.session_state.total_carbs, st.session_state.total_fibre)

    # Option to upload an image
    uploaded_file = st.file_uploader("Or upload a food image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        # Load and display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)

        # Ensure the image is in RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess the image for MobileNetV2
        image = image.resize((224, 224))  # Resize image to 224x224 pixels
        img_array = np.array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Make prediction with MobileNetV2
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        st.write("Predictions from Image:")
        for _, label, prob in decoded_predictions:
            st.write(f"{label}: {prob*100:.2f}%")

        # Get nutrition info for the predicted food item
        predicted_food = decoded_predictions[0][1]
        calories, protein, fat, carbs, fibre = get_nutrition_info(predicted_food)
        if calories > 0:
            st.write(f"Predicted Food: {predicted_food}")
            st.write(f"Calories: {calories} kcal")
            st.write(f"Protein: {protein} g")
            st.write(f"Fat: {fat} g")
            st.write(f"Carbs: {carbs} g")
            st.write(f"Fibre: {fibre} g")
        else:
            st.warning("Nutrition info not found for the predicted food.")
