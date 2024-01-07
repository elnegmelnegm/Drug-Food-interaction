import streamlit as st
import google.generativeai as genai

@st.cache_resource
def load_model() -> genai.GenerativeModel:
    """
    The function `load_model()` returns an instance of the `genai.GenerativeModel` class initialized with the model name
    'gemini-pro'.
    :return: an instance of the `genai.GenerativeModel` class.
    """
    model = genai.GenerativeModel('gemini-pro')
    return model

# Load the model
model = load_model()

# Input text
user_input_text = st.text_area("Enter text:", "")

# Generate Gemini response for text
if st.button("Generate Response"):
    try:
        # Define input prompt globally
        input_prompt = """
        As an expert specializing in assessing the suitability of fruits and foods for individuals with diabetes, your task involves analyzing input text featuring various food items. Your first objective is to identify the type of fruit or food present in the text. Subsequently, you must determine the glycemic index of the identified item. Based on this glycemic index, provide recommendations on whether individuals with diabetes can include the detected food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use English and Arabic languages for the response.
        """

        prompt_parts = [input_prompt, {"text": user_input_text}]
        response = model.generate_content(prompt_parts)
        
        st.text("Generated Response:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating response: {e}")
