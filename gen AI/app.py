import streamlit as st
from pathlib import Path
import google.generativeai as genai

# Importing api_key from the api_key.py file
from api_key import api_key

# Configure API with API key
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide an output response with these 4 headings: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions.

please use the easy language (means use simple english words) which are easy to understand
"""

# Initialize generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

# Set page configuration with CSS for animations
st.set_page_config(page_title="DiseaseDetect AI", page_icon=":robot:", layout="centered")

# CSS for animations and styling
st.markdown("""
    <style>
        /* Animation for page load fade-in */
        .main .block-container { 
            animation: fadeIn 1s ease-in-out;
        }

        /* Loading spinner style for the small spinner */
        .spinner-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }
        .spinner {
            border: 8px solid #f3f3f3; 
            border-top: 8px solid #3498db; 
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
        }

        /* Keyframes for animations */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Button hover effect */
        .stButton>button:hover {
            background-color: #3498db !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Display the logo with specified width
st.image("img.png.webp", width=100, use_container_width=False)
st.title("🧑‍⚕️DiseaseDetect AI")
st.subheader("An application to identify and analyze medical images")

# Divider
st.markdown("---")

# Upload file section with animated description
uploaded_file = st.file_uploader(
    "Upload a medical image (PNG or JPG) for a detailed analysis:", type=["png", "jpg"]
)

# Display the uploaded image with inline styling
if uploaded_file:
    st.markdown("### Uploaded Medical Image")
    st.image(uploaded_file, width=400, caption="Uploaded Medical Image")

# Animated submit button
st.markdown(" ")
submit_button = st.button("Generate Analysis 🔍")

# Generate analysis with animated spinner
if submit_button:
    if uploaded_file is None:
        st.warning("Please upload an image to analyze.")
    else:
        # Show the small spinner
        with st.spinner("Analyzing image..."):
            # Process the uploaded image
            image_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
            prompt_parts = [image_parts[0], system_prompt]

            # Generate a response based on prompt and image
            response = model.generate_content(prompt_parts)

            # Once the analysis is complete, show the result
            st.markdown("### 📝 Detailed Analysis Report")
            st.write(response.text)
