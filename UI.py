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

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* The header ELEMENT must stay in the DOM — that's what keeps the
   sidebar collapse/expand arrow working (confirmed by testing).
   IMPORTANT: do NOT hide stToolbar — after reading Streamlit's actual
   compiled source, the sidebar reopen button (stExpandSidebarButton) is
   rendered AS A CHILD of stToolbar, so hiding stToolbar would silently
   break the reopen arrow again. Instead we only strip the header's
   background so it stops rendering as a visible black bar/strip, while
   leaving every element inside it fully intact and functional. */
[data-testid="stHeader"] {
    background: transparent !important;
    height: 3rem;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(139,124,246,0.25), transparent 40%),
        radial-gradient(circle at 85% 100%, rgba(99,102,241,0.18), transparent 45%),
        #0B0E17;
}

.block-container {
    padding-top: 1.8rem !important;
    margin-top: 0 !important;
    padding-bottom: 3rem;
    max-width: 700px;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, rgba(139,124,246,0.18), rgba(99,102,241,0.10));
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    padding: 2.3rem 2rem;
    border-radius: 20px;
    margin-bottom: 1.6rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
.hero h1 {
    color: #F4F3FF;
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
}
.hero p {
    color: #B9B6D6;
    font-size: 1rem;
    line-height: 1.5;
    margin: 0;
}

/* Input card - now targets the ACTUAL container via key, not a fake markdown div */
.st-key-input_card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 1.4rem;
    margin-bottom: 1.4rem;
}

/* Result card - same fix */
.st-key-result_card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.6rem;
    margin-top: 1rem;
    color: #EDEDF5;
}
.st-key-result_card h4 {
    color: #F4F3FF;
    margin-top: 0;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #8B7CF6, #6366F1);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: 0.2s ease;
}
div.stButton > button:hover {
    filter: brightness(1.12);
    color: white;
}

/* Text input */
div[data-baseweb="input"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
}

/* Badges */
.badge {
    display: inline-block;
    background: rgba(139,124,246,0.15);
    color: #C9C4FF;
    border: 1px solid rgba(139,124,246,0.3);
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.15rem 0.25rem 0.15rem 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10131F;
    border-right: 1px solid rgba(255,255,255,0.06);
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


# SIDEBAR
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

with st.container(key="input_card"):
    video_url = st.text_input(
        "YouTube video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_clicked = st.button("🔍 Analyze Video", use_container_width=True)


if analyze_clicked:
    if not video_url:
        st.warning("Please enter a valid YouTube link first.")
    else:
        video_id = extract_video_id(video_url)

        if not video_id:
            st.error("That doesn't look like a valid YouTube link. Please check the URL.")
        else:
            st.video(f"https://www.youtube.com/watch?v={video_id}")

            try:
                with st.spinner("Analyzing video — this can take a few seconds..."):
                    response = agent.run(f"Analyze this video: {video_url}")

                st.success("Analysis complete!")

                with st.container(key="result_card"):
                    st.markdown("#### 📄 Analysis Report")
                    st.markdown(response.content)

                st.download_button(
                    "⬇️ Download Report",
                    data=response.content,
                    file_name="video_analysis_report.md",
                    mime="text/markdown",
                )
                
                if video_url in st.session_state.history:
                    st.session_state.history.remove(video_url)
                st.session_state.history.insert(0, video_url)

            except Exception as e:
                st.error(f"Something went wrong: {e}")


if st.session_state.history:
    with st.expander("🕘 Recently analyzed"):
        for url in st.session_state.history[:5]:
            st.write(url)
