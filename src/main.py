from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HR AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    employee_id: str
    question: str

@app.get("/")
async def health_check():
    """Lightweight health check endpoint to verify port binding instantly."""
    return {"status": "ok"}

@app.post("/ask")
async def ask_question(request: AskRequest):
    # Lazy import agent_executor when a request arrives
    # This prevents heavy imports from delaying port binding on app startup
    from src.agent import agent_executor

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
