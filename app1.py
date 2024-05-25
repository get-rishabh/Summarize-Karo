import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi


def app():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = """ You are a Youtube Video Summarizer, summarize the key points and main ideas presented in the YouTube Transcript, providing a concise overview of the content. Identify the most important takeaways and lessons, and outline the video's structure, including its introduction, main content sections, and conclusion. Include timestamps for each major section along with brief descriptions. Extract notable quotes or phrases, compare and contrast different viewpoints, and offer expert analysis where applicable. Assess the potential impact of the information presented and discuss any future directions or implications. Additionally, summarize audience engagement prompts and questions asked, along with their corresponding answers provided in the video. Ensure that all visual content, such as charts, graphs, or diagrams, is appropriately summarized. Finally, provide actionable insights or recommendations based on the video's content. Leave No IMPORTANT INFORMATION. The Transcript text is appended here :
    """

    def extract_transcript_details(youtube_video_url):
        try:
            video_id = youtube_video_url.split("=")[1]
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

            transcript = ""

            # print(video_id)

            for lines in transcript_text:
                transcript += " " + lines["text"]

            return transcript

        except Exception as e:
            raise e

    def generate_gemini_content(transcript_text, prompt):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text

    st.header(":orange[Youtube Video Summarizer 🐦‍🔥]")
    yt_link = st.text_area(
        "Enter the Url of the Youtube Video", placeholder="http://youtube.com/?video_id"
    )
    st.write("")
    if yt_link:
        video_id = yt_link.split("=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        # https://img.youtube.com/vi/HFfXvfFe9F8/0.jpg

    if st.button("Summarise Now", key=1):

        try :
            transcript_yt = extract_transcript_details(yt_link)
            try:
                if transcript_yt:
                    summary = generate_gemini_content(transcript_yt, prompt)
                    st.markdown("## Detailed Notes :")
                    st.write(summary)
            except Exception:
                st.markdown("Unable to Summarize, Try Again !!!")
        except Exception:
            st.markdown("Unable to Fetch the Transcript (Transcript must be in Enligh only)")
