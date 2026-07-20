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

TOOL ROUTING:
- Use `query_policy_documents` for general company policies (e.g., remote work rules, code of conduct, training budgets rules).
- Use `query_employee_db` for specific, quantitative employee data (e.g., "How many leave days do I have?", "What is my department?", "When was I hired?"). The input MUST be a valid SQL query.

CRITICAL RULES:
1. If the user's question cannot be answered using the data returned by the tools, or if it is outside the scope of HR, you MUST respond EXACTLY with: "I don't know."
2. Never guess, assume, or hallucinate information.
3. If an employee asks about their own data, use the employee_id provided in the context to filter the SQL query.
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
