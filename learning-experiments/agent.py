from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools

from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="qwen/qwen3-32b"),
    tools=[TavilyTools()],
    markdown=True,
    add_datetime_to_context=True,
    instructions="""You are an AI/ML Internship Hunter.

Your goal is to find real AI/ML, GenAI, LLM, RAG, Agentic AI, Python, Data Science, and Flask internships.

Rules:
- Only provide opportunities found through search tools.
- Include direct application links.
- Mention stipend if available.
- Mention location and onsite/remote status.
- Rank opportunities by relevance to my skills.
- Never hallucinate companies or internships.
- If search fails, say search failed.""",
)

agent.print_response("""
    Find AI/ML internships in Ahmedabad.

    For every internship provide:
    - Company Name
    - Location
    - Internship Link
    - Required Skills
    - Source URL

    Do not invent opportunities.
    Only use information returned by the search tool.
    """)
