
from fastapi import FastAPI

from app.api.chat import router as chat_router


# Create the FastAPI application.
app = FastAPI(
    title="GRP Backend",
    version="1.0.0",
)

# Register the chat API routes.
app.include_router(chat_router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Check whether the backend application is running."""
    return {
        "status": "ok",
        "service": "grp-backend",
    }
