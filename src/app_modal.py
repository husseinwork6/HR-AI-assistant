import modal

# Define container image with all required dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi",
        "uvicorn",
        "pydantic",
        "langchain",
        "langchain-community",
        "langchain-groq",
        "langchain-huggingface",
        "sentence-transformers",  # ✅ Added
        "langchain-chroma",
        "chromadb",
        "pandas",
        "pypdf"
    )
    # Add local project directories into the container image
    .add_local_dir("src", remote_path="/root/src")
    .add_local_dir("data", remote_path="/root/data")
)

app = modal.App("hr-ai-assistant")

@app.function(
    image=image,
    secrets=[modal.Secret.from_name("groq-secret")],
    timeout=300,
)
@modal.asgi_app()
def fastapi_app():
    from src.main import app as main_app
    return main_app
