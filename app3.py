import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from PyPDF2 import PdfReader



def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """
    You are a professional PDF analyzer and summarizer. Summarize the key points and main ideas from the uploaded PDF, providing a clear overview. Highlight key takeaways, insights, and notable quotes or phrases. Compare viewpoints where applicable and offer expert analysis. For study materials or question papers, identify important content for student growth. Provide actionable recommendations based on the document's content. Ensure no critical information is missed.
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
            st.markdown("Error Extracting Content from PDF")
            raise e

    def generate_gemini_content(prompt, pdf_text):
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt + pdf_text)
        return response.text

    st.header(":orange[Document Summarizer 📄]")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
    st.write("")

    if uploaded_file is not None:
        st.write("Click below button to Analyze and Summarize the file.")
        if st.button(" Get Detailed Notes ", key=3):
            try:
                # Progress bar for overall process
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Parsing PDF document
                status_text.text("📄 Parsing PDF document...")
                progress_bar.progress(20)
                
                with st.spinner("Parsing PDF document..."):
                    text = extract_text(uploaded_file)
                
                # Check word limit after parsing
                if len(text) > 600000:
                    progress_bar.progress(100)
                    status_text.text("❌ Document too large")
                    st.markdown("Number Of Words Exceeded, Try Again with less words (<600,000) !!!")
                    return
                
                progress_bar.progress(40)
                
                # Step 2: Processing document content
                status_text.text("🔄 Processing document content...")
                progress_bar.progress(60)
                
                with st.spinner("Processing document content..."):
                    # Additional processing if needed
                    pass
                
                progress_bar.progress(80)
                
                # Step 3: Generating summary
                status_text.text("🤖 Generating AI summary...")
                
                with st.spinner("Generating AI summary with Gemini..."):
                    summary = generate_gemini_content(prompt, text)
                
                if summary:
                    progress_bar.progress(100)
                    status_text.text("✅ Summary generated successfully!")
                    
                    # Display the summary
                    st.markdown("## Detailed Notes :")
                    st.write(summary)
                    
                    # Clear the progress indicators after a short delay
                    st.success("Summary completed successfully!")
                else:
                    progress_bar.progress(100)
                    status_text.text("❌ Failed to generate summary")
                    st.markdown("Unable to Summarize, Try Again !!!")
                    
            except Exception as e:
                st.error(f"Error Generating Content: {e}")
