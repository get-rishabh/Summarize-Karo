# Summarize-Karo

A multimodal data summarization application using Google's Gemini AI to summarize content from YouTube videos, images, and documents.

## Youtube Summarizer Demo Video


https://github.com/user-attachments/assets/6860406c-488d-4576-8144-2953651dc19e


## Features

- **YouTube Video Summarizer**: Extract transcripts and generate comprehensive summaries
- **Image Analyzer & Summarizer**: Analyze and describe images with AI
- **Document Summarizer**: Process PDF documents and generate summaries

## YouTube Transcript Extraction Solution

### Problems on Cloud Deployment (Streamlit Cloud, Huggingface Spaces)
When deploying to cloud platforms like Hugging Face, YouTube often detects automated tools like `yt-dlp` as bots and requires authentication, causing the error:
```
ERROR: [youtube] video_id: Sign in to confirm you're not a bot. Use --cookies-from-browser or --cookies for the authentication.
```

### Installation

```bash
pip install -r requirements.txt
```

### Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Navigate to the YouTube Video Summarizer section
3. Paste a YouTube URL
4. Click "Summarise Now"


### Environment Variables

Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Dependencies

- `streamlit==1.48.0`
- `google-generativeai==0.8.5`
- `youtube-transcript-api==0.6.2`
- `yt-dlp==2025.8.11`
- `python-dotenv==1.1.1`
- And more (see `requirements.txt`)
