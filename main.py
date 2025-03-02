import streamlit as st
import google.generativeai as genai

# Configure page settings - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="ُEDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

# **IMPORTANT: Configure the API key - DOUBLE CHECK THIS!**
API_KEY = "AIzaSyDlBv9Br45qcfbzGyr3AlcScyWQo3eSOPU"  # <--- REPLACE WITH YOUR ACTUAL API KEY HERE
if not API_KEY or API_KEY == "YOUR_API_KEY":
    st.error("API key is missing or not configured. Please set your API key in the code.")
    st.stop()
genai.configure(api_key=API_KEY)

# Display header and logos
st.markdown('''<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)
st.markdown('''Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

# Find available models but only show the selector, not the full list
try:
    # Get available models without displaying them
    available_models = genai.list_models()
    gemini_models = []

    # Filter for Gemini 1.5 or 2.0 models that are likely to support text generation
    for model in available_models:
        model_name = model.name
        if ("gemini-1.5" in model_name or "gemini-2.0" in model_name) and not "vision" in model_name:
            gemini_models.append(model_name)

    if not gemini_models:
        # If no Gemini models found, use all available models
        for model in available_models:
            gemini_models.append(model.name)

    # Create a model selector if models are available
    if gemini_models:
        # Default to a newer model if available, otherwise use first in list
        default_index = 0
        for i, model in enumerate(gemini_models):
            # Prioritize Gemini 2.0 Flash or Gemini 1.5 Flash
            if "gemini-2.0-flash" in model or "gemini-1.5-flash" in model:
                default_index = i
                break

        st.subheader("Model Selection")
        selected_model_name = st.selectbox(
            "Select a model to use:",
            gemini_models,
            index=default_index
        )
        st.success(f"Using model: {selected_model_name}")
    else:
        st.error("No models available with your API key/project.")
        st.stop()
except Exception as e:
    st.error(f"Error listing models: {e}")
    st.error("Please check your API key and Google Cloud project configuration.")
    st.stop()

# Define input prompt for hyperglycemia - KEPT FROM THE SECOND CODE
input_prompt = """
                As an expert specializing in assessing the suitability of food items in the context of potential interactions with drugs, your task involves analyzing input text describing various food items. Provide recommendations on whether individuals, particularly those with specific health conditions, can include the mentioned food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use Arabic languages for the response.
               """

# User input for the food description
user_input = st.text_area("Enter text describing a food item:")

# Function to generate response using the selected model - MODIFIED FROM THE FIRST CODE
def generate_response(model_name, prompt, user_text):
    try:
        # Initialize the model
        model = genai.GenerativeModel(model_name)

        # Check if the model supports safety settings and apply if needed
        safety_settings = None
        try:
            # Some models support safety settings
            safety_settings = {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"
            }
            # Generate content with the provided prompt and user input
            response = model.generate_content(
                [prompt, user_text],
                safety_settings=safety_settings
            )
        except:
            # If safety settings aren't supported, try without them
            response = model.generate_content([prompt, user_text])

        return response.text
    except Exception as e:
        st.error(f"Error generating response with {model_name}: {e}")
        st.error(f"Detailed error: {str(e)}")

        # Provide troubleshooting guidance based on the error
        if "404" in str(e) and "not found" in str(e):
            st.error(f"The model '{model_name}' might not support the generateContent method.")
            st.error("Try selecting a different model from the dropdown.")
        elif "403" in str(e):
            st.error("Permission denied. Your API key may not have access to this model.")

        return None

# Generate response button
if st.button("Generate Response"):
    if not user_input:
        st.warning("Please enter some text about a food item to analyze.")
    else:
        with st.spinner(f"Generating response using {selected_model_name}..."): # ADDED SPINNER
            response = generate_response(selected_model_name, input_prompt, user_input)

            if response:
                st.subheader("Generated Response:") # IMPROVED RESPONSE DISPLAY
                st.write(response)
            else:
                st.error("Failed to generate a response. Try selecting a different model.")

                # Suggest a fallback option
                st.info("If you continue to have issues, try one of these approaches:")
                st.info("1. Select a different model from the dropdown")
                st.info("2. Make sure the Google Generative AI API is enabled in your Google Cloud project")
                st.info("3. Check if your API key has the necessary permissions")
