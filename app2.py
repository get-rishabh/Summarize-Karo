import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai
import os
from PIL import Image
import io


def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """You are a Professional Image Analyzer and Summarizer, summarize the key points and main ideas presented in the uploaded image, providing a concise overview of the content. Identify the most important takeaways and lessons, and outline the files's structure, including its deep insights. Extract notable quotes or phrases, compare and contrast different viewpoints, and offer expert analysis where applicable. Assess the potential impact of the information presented and discuss any future directions or implications. Ensure that all visual content, such as charts, graphs, or diagrams, is appropriately summarized. Finally, provide actionable insights or recommendations based on the uploaded file. Leave No IMPORTANT INFORMATION. The File is appended here :
    """

    def generate_gemini_content(prompt, uploaded_file):
        image = Image.open(io.BytesIO(uploaded_file.read()))
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([prompt, image])
        return response.text

    st.header(":orange[Image Analyzer and Summarizer 📸]")
    # st.subheader('This is a subheader with a divider')

    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg","jpeg"])
    st.write("")

    if uploaded_file is not None:

        st.write("File Uploaded Succesfully")
        st.image(uploaded_file, use_column_width=True)
        st.write("Click below button to Analyze and Summarize the file.")

    if st.button("Summarise Now", key=2):
        try:
            summary = generate_gemini_content(prompt, uploaded_file)
            st.markdown("## Detailed Notes :")
            st.write(summary)
        except Exception:
            st.markdown("Some Error Occured, Try Again !!!")
