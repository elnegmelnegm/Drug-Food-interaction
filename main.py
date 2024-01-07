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

# Set page configuration
st.set_page_config(
    page_title="ُEDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

# Display header
st.markdown('''
<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)

# Additional information
st.markdown('''
Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

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
