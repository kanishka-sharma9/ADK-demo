from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import Session
from google.adk.tools import google_search_tool,google_search
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.agent_tool import AgentTool

session_service=InMemoryMemoryService()

session=Session(
    app_name="ADK demo",
    user_id="user-1",
    id="session-1"
)

session = session_service.add_session_to_memory(
    session=session,
)


from dotenv import load_dotenv
load_dotenv("./.env")

def hello(s:str):
    """Tool to say hello"""
    print("hello tool called")
    return f"hello {s}"

def bye():
    """Tool to say goodbye"""
    print("bye tool called")
    return "bye"


greeting_agent=Agent(
    name="greeting_agent",
    model="gemini-2.0-flash-001",
    description="""You are a greeting agent.""",
    instruction="""Your task is to greet the user 'hello' and 'goodbye' to the users.
                You can use the followig tools:
                    - hello : Tool for saying hello to the user.
                    - bye : Tool for saying goodbye.""",
    tools=[FunctionTool(hello),FunctionTool(bye)]
)


root_agent=Agent(
    name="root_agent",
    model="gemini-2.0-flash-001",
    description="You are a helpful assistant.",
    instruction="First, formally greet the user and then use the following tool(s) to answer user queries:" \
    "TOOL(S):" \
    "   - google_search_tool : search the web for information",
    # sub_agents=[AgentTool(agent=greeting_agent)],
    tools=[google_search]
)


runner=Runner(
    app_name="ADK demo",
    agent=root_agent,
    session_service=session,
)

print(runner.run(user_id="user-1",session_id='session-1',new_message="hi"))