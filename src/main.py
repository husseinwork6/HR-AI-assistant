from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import agent_executor

app = FastAPI(title="HR AI Assistant API")

class AskRequest(BaseModel):
    employee_id: str
    question: str

@app.post("/ask")
async def ask_question(request: AskRequest):
    # Inject the employee_id into the query context
    contextual_query = f"My employee ID is {request.employee_id}. {request.question}"

    # Invoke the LangChain agent
    response = agent_executor.invoke({"input": contextual_query})

    answer = response.get("output", "I don't know.")
    intermediate_steps = response.get("intermediate_steps", [])

    # Map the tool execution to the required source string
    source = "unknown"
    if "I don't know" in answer:
        source = "unknown"
    elif intermediate_steps:
        # Check the name of the first tool the agent decided to call
        tool_name = intermediate_steps[0][0].tool
        if tool_name == "query_policy_documents":
            source = "rag"
        elif tool_name == "query_employee_db":
            source = "structured_data"

    return {
        "answer": answer,
        "source": source
    }
