from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from src.rag import query_policy_documents
from src.database import query_employee_db
from src.config import GROQ_API_KEY

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY # Use api_key instead of groq_api_key
)

# 2. Define the tools array
tools = [query_policy_documents, query_employee_db]

# 3. Design the System Prompt
system_prompt = """You are a highly precise, internal HR AI assistant.
Your objective is to answer employee questions using strictly the provided tools.

DATABASE TOOLS USAGE:
- You have access to the 'employees' table.
- You can query details for the authenticated user or any other employee mentioned in the question (e.g., managers, colleagues).
- Available columns: employee_id, full_name, department, grade_level, hire_date, annual_leave_days, leave_taken, leave_balance, remote_model, manager, performance_rating, training_budget, employment_status

CRITICAL GUIDELINES:
1. If the question asks about a specific person by name, query the database using `WHERE full_name LIKE '%Name%'`.
2. Do not assume information. Only use data returned directly from the tools.
3. If the data is not returned by the database tool or the RAG tool, only then reply with "I don't know."
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Construct the Agent and Executor
agent = create_tool_calling_agent(llm, tools, prompt)

# return_intermediate_steps=True is critical. It allows us to track which tool was called
# so we can populate the "source" field in the FastAPI response.
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)
