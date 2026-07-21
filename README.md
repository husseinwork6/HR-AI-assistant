# HR AI Assistant
A full-stack, serverless HR assistant that answers policy questions and retrieves employee records using Retrieval-Augmented Generation (RAG) and structured data querying.

### Run at: https://hrassistant1.netlify.app/

## Architecture
* **Frontend:** Plain HTML5, Tailwind CSS (CDN), deployed on Netlify.
* **Backend:** FastAPI running serverless on Modal.
* **LLM & Embeddings:** Groq (llama-3.3-70b-versatile) and Hugging Face sentence-transformers (vector embeddings).
* **Vector Store:** ChromaDB for policy document retrieval.
* **Package Manager:** `uv`

## Project Structure
```plaintext
.
├── data/              # HR policy documents and structured employee datasets
├── frontend/          # Web interface
│   └── index.html
├── src/               # Application logic
│   ├── app_modal.py   # Modal serverless entry point
│   └── main.py        # FastAPI routes and RAG/DB logic
├── pyproject.toml     # Project dependencies
└── uv.lock            # Lockfile for reproducible builds
```

## Setup & Local Development

### Prerequisites
* Python 3.11+
* `uv` package manager installed
* Modal CLI configured (`modal setup`)
* Groq API Key set in Modal secrets (`groq-secret`)

### Running Locally
1. Install dependencies:
```bash
uv sync
```
2. Start the Modal development server:
```bash
uv run modal serve src/app_modal.py
```
3. Open `frontend/index.html` in your browser or serve it locally.

## Deployment

### Backend (Modal)
Deploy the backend to Modal serverless hosting:
```bash
uv run modal deploy src/app_modal.py
```

### Frontend (Netlify)
1. Update `API_URL` in `frontend/index.html` with your Modal production URL.
2. Push changes to GitHub. Netlify will build and host the site automatically.

## API Specification

### POST `/ask`

**Request Body**
```json
{
  "employee_id": "EMP001",
  "question": "How many annual leave days do I have left?"
}
```

**Response**
```json
{
  "answer": "You have 12 annual leave days remaining for the current calendar year.",
  "source": "structured_data"
}
```
