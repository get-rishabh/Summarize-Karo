import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
import textract, re



def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """You are a Professional PDF Analyzer and Summarizer, summarize the key points and main ideas presented in the uploaded PDF's text, providing a concise overview of the content. Identify the most important takeaways and lessons, and outline the files's structure, including its deep insights. Extract notable quotes or phrases, compare and contrast different viewpoints, and offer expert analysis where applicable. In case of a question paper or a study material, also analyze what is important for student's growth in their career. Finally, provide actionable insights or recommendations based on the uploaded file. Leave No IMPORTANT INFORMATION. The PDF's text is appended here :
    """

    def extract_text(uploaded_file):
        try:

            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            return text

        except Exception as e:
            raise e

    def generate_gemini_content(prompt, pdf_text):
        model = genai.GenerativeModel("gemini-1.0-pro-latest")
        response = model.generate_content(prompt + pdf_text)
        return response.text

    st.header(":orange[Document Summarizer 📄]")
    # st.header('This is a header with a divider')

    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
    st.write("")

    if uploaded_file is not None:
        text = extract_text(uploaded_file)
        if len(text) > 600000:
            st.markdown("Number Of Words Exceeded, Try Again with less words (<600,000) !!!")
        else:   
            st.write("Click below button to Analyze and Summarize the file.")
            if st.button(" Get Detailed Notes ", key=3):
                try:
                    summary = generate_gemini_content(prompt, text)
                    st.markdown("## Detailed Notes :")
                    st.write(summary)
                except Exception:
                    st.markdown("Some Error Occured, Try Again")
