from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
from agno.tools.yfinance import YFinanceTools

load_dotenv()

agent = Agent(
    model=Groq(id="qwen/qwen3-32b"),
    tools=[YFinanceTools(), TavilyTools()],
    markdown=True,
    add_datetime_to_context=True,
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions=["use given tools whenever possible. Format your response using markdown and use tables to display data where possible."],
    debug_mode=True
)


agent.print_response("Share the MSFT stock price and analyst recommendations")