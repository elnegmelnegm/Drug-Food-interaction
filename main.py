import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyCFPALEVIiwvWSREvVdBOzNd1VeyqQWt9o")

# Load the text generation model
@st.cache(allow_output_mutation=True)
def load_text_model() -> genai.GenerativeModel:
    model = genai.GenerativeModel('gemini-pro')
    return model

# Load the image generation model
@st.cache(allow_output_mutation=True)
def load_image_model() -> genai.GenerativeModel:
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

# Define input prompts for different health conditions
input_prompts = {
    "diabetes": """
               As an expert specializing in assessing the suitability of fruits and foods for individuals with diabetes, your task involves analyzing input images featuring various food items. Your first objective is to identify the type of fruit or food present in the image. Subsequently, you must determine the glycemic index of the identified item. Based on this glycemic index, provide recommendations on whether individuals with diabetes can include the detected food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use English and Arabic languages for the response.
               """,
    "hypertension": """
               As an expert specializing in assessing the suitability of fruits and foods for individuals with high blood pressure (hypertension), your task involves analyzing input images featuring various food items. Your first objective is to identify the type of fruit or food present in the image. Subsequently, provide recommendations on whether individuals with hypertension can include the detected food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use English and Arabic languages for the response.
               """,
    "hypercholesterolemia": """
               As an expert specializing in assessing the suitability of fruits and foods for individuals with hypercholesterolemia, your task involves analyzing input images featuring various food items. Your first objective is to identify the type of fruit or food present in the image. Subsequently, provide recommendations on whether individuals with hypercholesterolemia can include the detected food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use English and Arabic languages for the response.
               """,
}

def input_image_setup(uploaded_file):
    if not uploaded_file:
        st.error("No file uploaded.")
        return None

    try:
        # Read the content of the uploaded file as bytes
        image_parts = [
            {"mime_type": "image/jpeg", "data": uploaded_file.read()}
        ]
        return image_parts
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return None

def generate_gemini_text_response(text_model, condition, language):
    try:
        response = text_model.generate_content([input_prompts[condition], language])
        return response.text
    except Exception as e:
        st.error(f"Error generating text response: {e}")
        return None

def generate_gemini_image_response(image_model, uploaded_file, condition, language):
    image_prompt = input_image_setup(uploaded_file)
    if image_prompt:
        prompt_parts = [input_prompts[condition], image_prompt[0]]
        
        try:
            response = image_model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            st.error(f"Error generating image response: {e}")
            return None

    return None

# Display header
st.set_page_config(
    page_title="ُEDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

st.markdown('''
<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)

st.markdown('''
Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

# Choose health condition
health_condition = st.radio("Choose a health condition:", ("Diabetes", "Hypertension", "Hypercholesterolemia"))

# Choose language
language = st.radio("Choose a language:", ("English", "Arabic"))

# Choose method (text or image)
method = st.radio("Choose a method:", ("Text", "Image"))

# Load models based on the chosen method
if method == "Text":
    text_model = load_text_model()
    response = generate_gemini_text_response(text_model, health_condition.lower(), language.lower())
    st.text("Generated Response:")
    st.write(response)
else:
    image_model = load_image_model()
    uploaded_file = st.file_uploader(label="Upload an image of your food", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        response = generate_gemini_image_response(image_model, uploaded_file, health_condition.lower(), language.lower())
        st.text("Uploaded File: " + uploaded_file.name)
        st.text("Generated Response:")
        st.write(response)





