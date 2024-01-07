import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyCFPALEVIiwvWSREvVdBOzNd1VeyqQWt9o")

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Define input prompt globally
input_prompt = """
               As an expert specializing in assessing the suitability of food items in the context of potential interactions with drugs, your task involves analyzing input text describing various food items. Provide recommendations on whether individuals, particularly those with specific health conditions, can include the mentioned food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use English and Arabic languages for the response.
               """

def generate_gemini_response(input_text):
    prompt_parts = [input_prompt, {"text": input_text, "lang": "en"}]
        
    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")

# Display header
st.set_page_config(
    page_title="Food-Drug Interaction Advisor",
    layout="wide",
)

st.markdown('''
Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

# Text input and response display
input_text = st.text_area("Enter text describing a food item:")
if input_text:
    try:
        response = generate_gemini_response(input_text)
        st.text("Generated Response:")
        st.write(response)
    except Exception as e:
        st.error(f"Error processing text: {e}")
