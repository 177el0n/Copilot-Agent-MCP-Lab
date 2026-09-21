from fastapi import FastAPI
from app.routers import todos

app = FastAPI()

# Register routers
app.include_router(todos.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
