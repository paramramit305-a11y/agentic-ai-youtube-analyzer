from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from rich.pretty import pprint


load_dotenv()

db = SqliteDb(db_file="agno.db")
db.clear_memories()

agent = Agent(
    db=db,
    model=Groq(id="qwen/qwen3-32b"),
    markdown=True,
    add_history_to_context=True,
    enable_user_memories=True
)

user_id = "Amit@gmail.com"
agent.print_response("My name is Amit and I prefer email over phone calls.", user_id=user_id)
agent.print_response("What's the best way to reach me?", user_id=user_id)

memories = agent.get_user_memories(
    user_id=user_id
)

print("MEMORIES: ")
pprint(memories)