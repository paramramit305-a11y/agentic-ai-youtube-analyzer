import re
import streamlit as st
from youtube_analyzer import youtube_analyzer_agent

st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {
    display: none;
}

.stApp {
    background: linear-gradient(180deg, #FAFAFF 0%, #F3F1FF 100%);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 760px;
}


/* Hero */
.hero {
    background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
    padding: 2.2rem 2rem;
    border-radius: 18px;
    color: white;
    margin-bottom: 1.8rem;
    box-shadow: 0 10px 30px rgba(108, 92, 231, 0.25);
}
.hero h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 0.4rem 0;
}
.hero p {
    font-size: 1.02rem;
    opacity: 0.92;
    margin: 0;
}

/* Card wrapper for input section */
.input-card {
    background: #F5F4FF;
    border: 1px solid #E4E1FB;
    border-radius: 16px;
    padding: 1.5rem 1.5rem 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}

/* Result card */
.result-card {
    background: #FFFFFF;
    border: 1px solid #ECECEC;
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 4px 18px rgba(0,0,0,0.05);
    margin-top: 1rem;
}

/* Buttons */
div.stButton > button {
    background: #6C5CE7;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.4rem;
    font-weight: 600;
    transition: 0.2s ease;
}
div.stButton > button:hover {
    background: #5A4BD6;
    color: white;
}

/* Text input */
div[data-baseweb="input"] {
    border-radius: 10px !important;
}

/* Badges */
.badge {
    display: inline-block;
    background: #F5F4FF;
    color: #6C5CE7;
    border: 1px solid #E4E1FB;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.15rem 0.25rem 0.15rem 0;
}
</style>
""", unsafe_allow_html=True)


def extract_video_id(url: str):
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else None


@st.cache_resource
def get_agent():
    return youtube_analyzer_agent()


agent = get_agent()

if "history" not in st.session_state:
    st.session_state.history = []


# SIDEBAR-
with st.sidebar:
    st.markdown("### 📺 About this Agent")
    st.write(
        "An AI agent that watches a YouTube video for you and returns a "
        "structured summary — topics covered, key takeaways, and an "
        "overall breakdown — in seconds."
    )

    st.markdown("---")
    st.markdown("### ⚙️ How it works")
    st.markdown(
        """
1. Paste a YouTube video link
2. The agent fetches video context (captions/metadata)
3. An LLM analyzes and structures the content
4. You get a clean, readable report
        """
    )

    st.markdown("---")
    st.markdown("### 🛠️ Built with")
    st.markdown(
        """
<span class="badge">Python</span>
<span class="badge">Agno</span>
<span class="badge">Streamlit</span>
<span class="badge">LLM Agent</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub Repo](https://github.com/paramramit305-a11y/agentic-ai-youtube-analyzer)")


st.markdown(
    """
<div class="hero">
    <h1>📺 AI YouTube Video Analyzer</h1>
    <p>Paste any YouTube link and get an AI-generated breakdown — key points,
    structure, and takeaways — without watching the full video.</p>
</div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="input-card">', unsafe_allow_html=True)

video_url = st.text_input(
    "YouTube video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 5])
with col1:
    analyze_clicked = st.button("🔍 Analyze Video", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


if analyze_clicked:
    if not video_url:
        st.warning("Please enter a valid YouTube link first.")
    else:
        video_id = extract_video_id(video_url)

        if video_id:
            st.video(f"https://www.youtube.com/watch?v={video_id}")

        try:
            with st.spinner("Analyzing video — this can take a few seconds..."):
                response = agent.run(f"Analyze this video: {video_url}")

            st.success("Analysis complete !")

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("#### 📄 Analysis Report")
            st.markdown(response.content)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                "⬇️ Download Report",
                data=response.content,
                file_name="video_analysis_report.md",
                mime="text/markdown",
            )

            st.session_state.history.insert(0, video_url)

        except Exception as e:
            st.error(f"Something went wrong: {e}")


if st.session_state.history:
    with st.expander("🕘 Recently analyzed"):
        for url in st.session_state.history[:5]:
            st.write(url)
