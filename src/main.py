from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.agent import agent_executor

app = FastAPI(title="HR AI Assistant API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from Netlify and local dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    employee_id: str
    question: str

@app.post("/ask")
async def ask_question(request: AskRequest):
    contextual_query = f"My employee ID is {request.employee_id}. {request.question}"

    response = agent_executor.invoke({"input": contextual_query})

    answer = response.get("output", "I don't know.")
    intermediate_steps = response.get("intermediate_steps", [])

    source = "unknown"
    if "I don't know" in answer:
        source = "unknown"
    elif intermediate_steps:
        tool_name = intermediate_steps[0][0].tool
        if tool_name == "query_policy_documents":
            source = "rag"
        elif tool_name == "query_employee_db":
            source = "structured_data"

    return {
        "answer": answer,
        "source": source
    }
