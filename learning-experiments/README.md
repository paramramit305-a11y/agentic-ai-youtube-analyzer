# Agno practice files

Working exercises from learning the Agno framework, before building the [YouTube analyzer](../README.md). Not cleaned up for presentation — kept as-is to show what the learning process actually looked like.

| File | What's in it |
|---|---|
| `agent.py` | Single agent with a web search tool (Tavily) — instructed to find real AI/ML internships and return only what the search tool actually returns, nothing invented |
| `finance.py` | Agent with two tools (`YFinanceTools`, `TavilyTools`) — pulls stock price and analyst recommendations, formats output as markdown tables |
| `memory.py` | Agent with persistent memory using Agno's `SqliteDb` — stores and recalls user-specific facts across separate calls |
| `team.py` | Three agents (English/Chinese/Hindi) coordinated by a `Team` leader, each required to respond independently to the same query |

All of these use Groq (`qwen/qwen3-32b`), same as the main project.

`agno.db`, the SQLite file `memory.py` generates at runtime, isn't committed — it's listed in `.gitignore` since it's local output, not source code.
