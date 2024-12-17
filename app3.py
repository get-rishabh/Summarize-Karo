import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from PyPDF2 import PdfReader



def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """
    You are a professional PDF analyzer and summarizer. Summarize the key points and main ideas from the uploaded PDF, providing a clear overview. Highlight key takeaways, insights, and notable quotes or phrases. Compare viewpoints where applicable and offer expert analysis. For study materials or question papers, identify important content for student growth. Provide actionable recommendations based on the document’s content. Ensure no critical information is missed.
    The PDF's text is appended here :
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
                    st.markdown("## Detailed Summary :")
                    st.write(summary)
                except Exception:
                    st.markdown("Some Error Occured, Try Again")
