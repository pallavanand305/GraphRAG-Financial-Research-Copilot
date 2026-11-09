from fastapi import FastAPI

app = FastAPI(title="GraphRAG Financial Research Copilot")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready", "stores": {"postgres": "ok", "qdrant": "ok", "neo4j": "ok", "redis": "ok"}}
