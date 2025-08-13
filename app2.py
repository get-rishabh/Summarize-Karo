import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai
import os
from PIL import Image
import io


def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """"
        You are an AI agent designed to summarize images by recognizing key visual elements and generating a detailed explanation of the content. Your task is to:

    General Overview: Begin with a brief summary of the image as a whole in one or two sentences.
    Recognition of Famous Entities: Actively recognize well-known actors, celebrities, monuments, landmarks, brands, and objects. If recognizable, name them explicitly and provide relevant context. Pull additional, related information from the internet to enrich the summary (e.g., brief facts, historical significance, notable roles or achievements).
    
    Contextual Description: Accurately describe the relationships and placement of people, objects, and settings within the image. Highlight interactions, notable poses, and expressions where relevant.
    
    Details: Mention specific visual elements such as colors, emotions, clothing, architectural styles, and symbolism, focusing on aspects that enhance understanding of the image's message or context.
    
    Avoid Assumptions: Stick to what can be verified visually or recognized through data. Do not infer any hidden intentions or emotions that are not clearly present.
    
    Clarity & Simplicity: Ensure that descriptions are clear, simple, and avoid overly technical language. Focus on making the summary understandable to a wide audience.
    
    Information Gathering: If the image contains famous individuals, objects, or places, gather key facts from the internet, such as their significance, historical background, or cultural relevance. This should provide more depth to the image summary.
    
    Tone: Maintain a neutral, objective, and informative tone. Do not add subjective opinions unless it involves describing popular interpretations related to the recognized element.
    
    Limit Speculation: If certain aspects of the image are unclear or ambiguous, briefly note them as possibilities without making definitive claims.
    
    Leave No IMPORTANT INFORMATION. Output should be in markdown format, following the format below:
    # Image Summary
    ## General Overview
    ## Recognition of Famous Entities (if any)
    ## Contextual Description
    ## Details
    ## Tone(if any)

    """

    def generate_gemini_content(prompt, uploaded_file):
        image = Image.open(io.BytesIO(uploaded_file.read()))
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content([prompt, image])
        return response.text    

    st.header(":orange[Image Analyzer and Summarizer 📸]")

    uploaded_file = st.file_uploader("Choose a file", type=["png","jpeg","webp"])
    st.write("")

    if uploaded_file is not None:

        st.write("File Uploaded Succesfully")
        st.image(uploaded_file, use_container_width=True)
        st.write("Click below button to Analyze and Summarize the file.")

    if st.button("Summarise Now", key=2):
        try:
            # Progress bar for overall process
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Processing image
            status_text.text("🔄 Processing image...")
            progress_bar.progress(25)
            
            with st.spinner("Processing image..."):
                # Reset file pointer to beginning
                uploaded_file.seek(0)
            
            progress_bar.progress(50)
            
            # Step 2: Generating analysis
            status_text.text("🤖 Generating AI analysis...")
            progress_bar.progress(75)
            
            with st.spinner("Generating AI analysis with Gemini..."):
                summary = generate_gemini_content(prompt, uploaded_file)
            
            if summary:
                progress_bar.progress(100)
                status_text.text("✅ Analysis generated successfully!")
                
                # Display the summary
                st.markdown(summary)
                
                # Clear the progress indicators after a short delay
                st.success("Analysis completed successfully!")
            else:
                progress_bar.progress(100)
                status_text.text("❌ Failed to generate analysis")
                st.markdown("Unable to Analyze, Try Again !!!")
                
        except Exception as e:
            st.error(f"Some Error Occured, Try Again !!!, {e}")
