import streamlit as st
from youtube_analyzer import youtube_analyzer_agent

st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"
)

st.title("📺 AI Youtube Video Analyzer")

st.caption("Paste a YouTube URL and get an AI-powered analysis.")

@st.cache_resource
def get_agent():
    return youtube_analyzer_agent()


agent = get_agent()


with st.sidebar:
    st.header("📋 About")
    st.write(
        "This AI agent analyzes YouTube videos and generates a detailed report."
    )


# input
video_url = st.text_input("Enter Youtube Video Link")  # str 
button = st.button("Analyze Video")   # True/False


if video_url and button:
    try:
        with st.spinner("Analyzing Video..."):
            response = agent.run(
                f"Analyze this video: {video_url}"
            )

        st.success("Analysis Completed.")

        st.markdown("Analysis Report of Video:")
        st.markdown(response.content)

    except Exception as e:
        st.error(f"Error: {e}")
