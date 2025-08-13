import streamlit as st
import re
import subprocess
import logging
from dotenv import load_dotenv
import yt_dlp
import assemblyai as aai
# Configure logging
logging.basicConfig(level=logging.INFO)
logging = logging.getLogger(__name__)

load_dotenv()
import google.generativeai as genai
import os

# Configure API keys
# AssemblyAI API key will be loaded from environment variables

def app():
    # Check required environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")

    missing_keys = []
    if not google_api_key:
        missing_keys.append("GOOGLE_API_KEY")
    if not assemblyai_api_key:
        missing_keys.append("ASSEMBLYAI_API_KEY")

    if missing_keys:
        st.error(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        st.markdown("""
        Please set the required API keys in your `.env` file:
        ```
        GOOGLE_API_KEY=your_google_key
        ASSEMBLYAI_API_KEY=your_assemblyai_key
        ```
        """)
        return

    genai.configure(api_key=google_api_key)
    aai.settings.api_key = assemblyai_api_key

    prompt = """ 
        You are a **professional YouTube Video Summarizer**. Analyze the **transcript provided**, adapt your approach based on the type of content (e.g., educational, story, news, tutorial, commentary), and follow these detailed steps:
        ---
        ## THINK STEP-BY-STEP
        ### 1. Language Handling:
        - Automatically detect the language of the transcript.
        - Translate it into **English** before summarizing (if necessary).
        ### 2. Content-Type Identification:
        Based on the tone, structure, and keywords of the transcript, determine the **type of video**, such as:
        - Educational / Tutorial
        - Storytelling (personal or fictional)
        - News / Commentary / Opinion
        - Review / Explainer
        - Motivational / Inspirational
        ---
        ## UNIVERSAL SUMMARY STRUCTURE (All Videos)
        ### Video Structure with Timestamps:
        Break the video into major sections, include **timestamps**, and describe what happens in each.
        ### Main Summary (Concise Overview):
        - Summarize the **core ideas, arguments, or narrative**.
        - Present the **main takeaways**, ensuring no critical detail is skipped.
        ### Visuals Summary:
        - Describe and interpret **charts, graphs, demonstrations, diagrams, or screen recordings**.
        ### Impact & Implications:
        - Assess the **relevance, applications, and future directions** of the content.
        - Comment on **how this might affect viewers or related industries**.
        ---
        ## IF EDUCATIONAL / TUTORIAL VIDEO
        ### Key Concepts & Explanations:
        - List each **concept explained** with simple definitions.
        - Mention **formulas, theories, processes, examples, and demonstrations** shown.
        ### Techniques, Tips, or Frameworks:
        - Clearly outline **methods, strategies, models**, or **step-by-step guides** provided.
        ### Insights or Recommendations:
        - Provide **practical advice** or **learning recommendations** based on the topic.
        ---
        ## IF STORY-BASED VIDEO
        ### Story Crux & Analysis:
        - Outline the **main plot**, **key events**, and **turning points**.
        - Identify the **emotional tone** (e.g., humorous, dramatic, suspenseful).
        - Discuss **themes, morals, character motivations**, or **twists**.
        ### Reactions & Interpretations:
        - Provide **analysis or reflection** on the message, meaning, or societal relevance.
        ---
        ## IF COMMENTARY / REVIEW / OPINION
        ### Viewpoints Presented:
        - Identify **main arguments** or **opinions** expressed.
        - Note **contrasting perspectives**, if any.
        ### Comparisons & Evaluation:
        - Compare with **other viewpoints, products, events**, or **prior videos**.
        ---
        ## FINAL OUTPUT SHOULD BE IN MARKDOWN FORMAT, FOLLOWING THE FORMAT BELOW:
        ## FINAL OUTPUT FORMAT
        - **Section 1:** Video Overview
        - **Section 2:** Main Summary
        - **Section 3:** Type-Specific Breakdown (Concepts / Story / Opinions)
        - **Section 4:** Quotes & Visual Summary
        - **Section 5:** Impact, Future Directions, Recommendations

        ## STRICTLY FOLLOW the GUIDELINES BELOW, do not deviate from the final_output_format and don't add text like :
        #  "The video transcript is in English, so no translation is needed."
        #  "The video is a tutorial, so the summary should be in the format of a tutorial."
        #  "The video is a news, so the summary should be in the format of a news."
        #  "The video is a commentary, so the summary should be in the format of a commentary."
        #  "The video is a review, so the summary should be in the format of a review."
        #  "The video is a motivational, so the summary should be in the format of a motivational."
        #  "The video is a inspirational, so the summary should be in the format of a inspirational."
    """

    def download_audio(video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        output_path = f"/tmp/{video_id}.webm"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "quiet": True,
            "noplaylist": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return output_path

    def fetch_video_metadata(video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info.get("title", ""), info.get("description", "")

    def transcribe_with_assemblyai(audio_path):
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)
        return transcript.text

    def generate_gemini_content(transcript_text, prompt):
        try :
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt + transcript_text)
            return response.text
        except Exception as e:
            st.error("Error in generating content : ", e)
            return None

    st.header(":orange[Youtube Video Summarizer 🦜]")

    st.info('Currently Supports Only Long Format Videos (No Shorts)', icon="ℹ️")
    yt_link = st.text_area(
        "Enter the Url of the Youtube Video", placeholder="Format : http://youtube.com/?video_id"
    )
    st.write("")

    video_id = ""
    if yt_link:
        try:
            reg = re.search(r'(?<=v=)[^&]+', yt_link) #regex for extracting the video_id from the URL 
            video_id = reg.group(0)
            print("VIDEO ID : ", video_id)
            st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
        except IndexError as e:
            st.error("Only Long Format Videos are supported")
        # Universal YT Thumbnail :  https://img.youtube.com/vi/HFfXvfFe9F8/0.jpg

    if st.button("Summarise Now", key=1):
        try :
            # Debug: Check if button was clicked
            st.write("Button clicked! Starting transcript extraction...")

            # Progress bar for overall process
            progress_bar = st.progress(0)
            status_text = st.empty()

            # 1. Download audio
            status_text.text("🎵 Downloading audio from YouTube...")
            progress_bar.progress(25)
            
            with st.spinner("Downloading audio from YouTube..."):
                audio_path = download_audio(video_id)
            
            # 2. Fetch metadata
            status_text.text("📝 Fetching video metadata...")
            progress_bar.progress(40)
            
            with st.spinner("Fetching video title and description..."):
                title, description = fetch_video_metadata(video_id)
            
            # 3. Transcribe
            status_text.text("🔤 Transcribing audio with AssemblyAI...")
            progress_bar.progress(60)
            
            with st.spinner("Transcribing audio with AssemblyAI..."):
                transcript_text = transcribe_with_assemblyai(audio_path)
            
            progress_bar.progress(75)
            
            if transcript_text:
                # 4. Combine for Gemini
                status_text.text("🤖 Generating AI summary...")
                
                with st.spinner("Generating AI summary with Gemini..."):
                    combined_input = f"Video Title: {title}\nDescription: {description}\nTranscript:\n{transcript_text}"
                    summary = generate_gemini_content(combined_input, prompt)

                if summary:                
                    progress_bar.progress(100)
                    status_text.text("✅ Summary generated successfully!")
                    
                    # Display the summary
                    st.markdown(summary)
                    
                    # Clear the progress indicators after a short delay
                    st.success("🎉 Summary completed!")
                else:
                    progress_bar.progress(100)
                    status_text.text("❌ Failed to generate summary")
                    st.markdown("Unable to Summarize, Try Again !!!")

            else:
                progress_bar.progress(100)
                status_text.text("❌ Failed to transcribe audio")
                st.error("❌ Unable to transcribe audio")
                st.markdown("""
                **Possible reasons:**
                - AssemblyAI API key not configured or invalid
                - Audio download failed
                - Network connectivity issues
                - Audio format not supported
                
                **Try these solutions:**
                - Check your AssemblyAI API key
                - Try a different video
                - Ensure the video is public and accessible
                """)

        except Exception as e:
            print("Error : ", e)
            st.error("Something Went Wrong !!!")
            st.error(f"Error details: {str(e)}")
