import streamlit as st
import re
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi


def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """ 
        You are a Youtube Video Summarizer, summarize the key points and main ideas presented in the YouTube Transcript, providing a concise overview of the content. Identify the most important takeaways and lessons, and outline the video's structure, including its introduction, main content sections, and conclusion. Include timestamps for each major section along with brief descriptions. Extract notable quotes or phrases, compare and contrast different viewpoints, and offer expert analysis where applicable. Assess the potential impact of the information presented and discuss any future directions or implications. Additionally, summarize audience engagement prompts and questions asked, along with their corresponding answers provided in the video. Ensure that all visual content, such as charts, graphs, or diagrams, is appropriately summarized. Finally, provide actionable insights or recommendations based on the video's content. Leave No IMPORTANT INFORMATION.The transcript provided to you can be in any language, so convert it accordingly and then summarize it. 
        The Transcript text is appended here :
    """

    def extract_transcript_details(youtube_video_url):
        try:
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            try:
                transcript = transcript_list.find_generated_transcript(['hi', 'en'])
                translated_script = transcript.translate('en')
                transcript_text = translated_script.fetch()
                print(transcript_text)
            except Exception as e:
                raise e
        
        if transcript_text:               
            transcript = ""
            for lines in transcript_text:
                transcript += " " + lines["text"]
            return transcript

    def generate_gemini_content(transcript_text, prompt):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text

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
            print(video_id)
            st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
        except IndexError as e:
            st.error("Only Long Format Videos are supported")
        # Universal YT Thumbnail :  https://img.youtube.com/vi/HFfXvfFe9F8/0.jpg

    if st.button("Summarise Now", key=1):
        try :
            transcript_yt = extract_transcript_details(video_id)
            try:
                if transcript_yt:
                    print("Got transc.")
                    summary = generate_gemini_content(transcript_yt, prompt)
                    st.markdown("## Detailed Notes :")
                    st.write(summary)
            except Exception:
                st.markdown("Unable to Summarize, Try Again !!!")

        except Exception:
            st.markdown("Unable to Fetch the Transcript (Transcript must be in Enligh only)")
