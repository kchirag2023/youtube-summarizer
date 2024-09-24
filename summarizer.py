import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv()


genai.configure(api_key=API_KEY)




def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        youtube_text = YouTubeTranscriptApi.get_transcript(video_id)
        print(youtube_text)
        # in youtube text we will get the list
        transcript = " ".join([i["text"] for i in youtube_text])
        print(transcript)
        return transcript
    except Exception as e:
        raise e


def extract_video_id(youtube_video_url):
    if 'youtu.be' in youtube_video_url:
        video_id = youtube_video_url.split('/')[-1].split('?')[0]
    elif 'watch' in youtube_video_url:
        video_id = youtube_video_url.split('=')[-1].split('&')[0]
    else:
        raise ValueError("Invalid YouTube URL")
    return video_id


def generate_gemini_content(youtube_text, prompt):
    model = genai.GenerativeModel('gemini-1.0-pro')
    response = model.generate_content(prompt + youtube_text)
    print(response)
    text = response.candidates[0].content.parts[0].text

    print(text)

   

    
    return text 




st.title("YouTube Vivaran")
youtube_link = st.text_input("Enter YouTube URL:")

if youtube_link:
    try:
        video_id = extract_video_id(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except ValueError:
        st.error("Please enter a valid YouTube URL")

if st.button("Get Summary"):
    try:
        youtube_text = extract_transcript_details(youtube_link)
        if youtube_text:
            prompt = "You are a YouTube video summarizer. You will take the transcript text and provide a summary within 1000 words paragraph along with that highlights the important points "
            summary = generate_gemini_content(youtube_text, prompt)
            print("summary")
            print(summary)
            st.markdown("Summary is generated:")
            st.write(summary)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
        
        
        # streamlit run summarizer.py
