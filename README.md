# Summarize-Karo

A multimodal data summarization application using Google's Gemini AI to summarize content from YouTube videos, images, and documents.

## Features

- **YouTube Video Summarizer**: Extract transcripts and generate comprehensive summaries
- **Image Analyzer & Summarizer**: Analyze and describe images with AI
- **Document Summarizer**: Process PDF documents and generate summaries

## YouTube Transcript Extraction Solution

### Problem
When deploying to cloud platforms like Hugging Face, YouTube often detects automated tools like `yt-dlp` as bots and requires authentication, causing the error:
```
ERROR: [youtube] video_id: Sign in to confirm you're not a bot. Use --cookies-from-browser or --cookies for the authentication.
```

### Solution
The application now uses a **multi-method fallback system**:

1. **Primary Method**: `youtube-transcript-api` - Most reliable for cloud deployments
2. **Fallback Method**: `yt-dlp` with enhanced options for better bot detection avoidance
3. **Future Method**: YouTube Data API (requires API key setup)

### Key Improvements

- **Enhanced yt-dlp options**: Added user-agent, no-certificate-check, and Android client emulation
- **Multiple fallback methods**: If one method fails, automatically tries the next
- **Better error handling**: Provides helpful error messages and troubleshooting tips
- **Cloud-optimized**: Designed to work reliably on Hugging Face and other cloud platforms

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

### Testing

To test the transcript extraction:
```bash
python test_transcript.py
```

### Troubleshooting

If transcript extraction fails:

1. **Check video availability**: Ensure the video is public and has subtitles enabled
2. **Try different videos**: Some videos may have restricted access
3. **Check network**: Ensure stable internet connection
4. **Update dependencies**: Make sure all packages are up to date

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
