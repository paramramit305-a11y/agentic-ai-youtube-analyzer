# YouTube Video Analyzer (Agno Agent)

Takes a YouTube link and returns a timestamped breakdown of the video — pulls the transcript when accessible, using an Agno agent backed by Groq.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Agno](https://img.shields.io/badge/Agno-agentic_framework-7C3AED?style=flat-square)](https://agno.com)
[![Groq](https://img.shields.io/badge/Groq-qwen3--32b-F55036?style=flat-square)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**[Live demo →](https://agentic-ai-youtube-analyzer.streamlit.app)**

## What it does

Paste a YouTube URL, get back:
- Video overview — title, author, duration, content type
- Timestamped segment breakdown, grounded in the transcript the tool returns (the agent is explicitly instructed not to guess timestamps)
- Key learning points and technical notes

I built this after going through Agno's basics — single agents, tool use, memory, multi-agent teams — as the final, "actually usable" project from that learning process. The earlier exercises are kept in [`learning-experiments/`](./learning-experiments) rather than deleted, since they show the progression.

## Why I built it this way

YouTube videos (lectures, tutorials, talks) are slow to skim if you just want to know whether a specific topic is covered and where. Rather than writing a script that fetches a transcript and dumps it through an LLM once, I used Agno's `Agent` class so the model has tool access (`YouTubeTools`) and follows a multi-step instruction set — overview first, then timestamps, then thematic grouping — instead of producing one unstructured summary.

## How it works

```
UI.py (Streamlit)
   │  takes a YouTube URL, calls agent.run()
   ▼
youtube_analyzer.py (Agno Agent)
   │  model: Groq qwen/qwen3-32b
   │  tools: YouTubeTools (transcript + metadata)
   ▼
Groq API → structured markdown report → rendered in Streamlit
```

## Stack

| Part | Choice | Why |
|---|---|---|
| Agent framework | Agno | Much less boilerplate than LangChain for a single tool-using agent; was already learning it for this reason |
| Model | Groq — `qwen/qwen3-32b` | Free tier, fast enough for interactive use in the UI |
| Tool | `YouTubeTools` | Handles transcript fetching so the agent doesn't have to |
| Frontend | Streamlit | Fastest way to get a usable UI on top of a Python agent |

## Project structure

```
agentic-ai-youtube-analyzer/
├── UI.py                   # Streamlit app
├── youtube_analyzer.py     # Agent definition + instructions
├── requirements.txt
├── .gitignore
└── learning-experiments/   # Earlier Agno practice (see its own README)
    ├── agent.py             # Tool-using agent: searches for AI/ML internships (Tavily)
    ├── finance.py           # Agent with YFinance + Tavily tools
    ├── memory.py            # Agent with persistent SQLite-backed memory
    └── team.py               # Multi-agent team (3 agents, 3 languages)
```

## Running it locally

```bash
git clone https://github.com/paramramit305-a11y/agentic-ai-youtube-analyzer.git
cd agentic-ai-youtube-analyzer
pip install -r requirements.txt
```

Create a `.env` file in the root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

```bash
streamlit run UI.py
```

Opens at `http://localhost:8501`.

## Known limitations

- **Transcript fetching is unreliable on cloud deployment.** `youtube-transcript-api` (used by `YouTubeTools`) works reliably when run locally, but YouTube blocks most requests coming from cloud provider IP ranges (AWS, GCP, Azure, and by extension Streamlit Community Cloud) — this is a known limitation of the library itself, not specific to this project. When the transcript fetch fails, the agent falls back to metadata-only analysis and explicitly flags the missing transcript instead of fabricating timestamps. A proper fix needs a residential proxy (e.g. Webshare), which I haven't added since it's a paid dependency.
- Single video at a time, no comparison mode

## Possible next steps

- Add residential proxy support so transcript fetching works reliably on the deployed version, not just locally
- Let users ask follow-up questions about the analyzed video instead of just getting a one-shot report
- Swap the model provider (OpenAI/Anthropic) to confirm the Agno setup is actually model-agnostic, not just working with Groq

## Author

Amit Parmar — BSc IT (AIML), Gokul Global University
[GitHub](https://github.com/paramramit305-a11y) · [LinkedIn](https://www.linkedin.com/in/parmar-amit-97941a377) · [HuggingFace](https://huggingface.co/parmar-amit)
