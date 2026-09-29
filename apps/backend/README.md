# GRP Backend

Backend and AI agent platform for GRP.

## Technology

- Python
- FastAPI
- LangGraph
- PostgreSQL (Neon)
- Docker
- Google Cloud Run

## Project Structure

    app/
    ├── agents/          # AI agents and agent subgraphs
    ├── api/             # FastAPI routes
    ├── core/            # Configuration, security, logging
    ├── db/              # Neon PostgreSQL access
    ├── orchestration/   # Top-level LangGraph orchestration
    ├── schemas/         # Request and response models
    ├── services/        # Application and integration services
    └── tools/           # Controlled tools available to agents

    tests/               # Automated tests

## Local Development

From the backend directory:

    cd apps/backend

Create a virtual environment:

    python -m venv .venv

Activate it on Windows:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

Start the backend:

    uvicorn app.main:app --reload

## Health Check

    GET /health

Expected response:

    {
      "status": "ok",
      "service": "grp-backend"
    }

## API Documentation

When the backend is running:

    http://127.0.0.1:8000/docs