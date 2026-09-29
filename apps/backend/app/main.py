from fastapi import FastAPI

app = FastAPI(
    title="GRP Backend",
    version="1.0.0",
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "grp-backend",
    }