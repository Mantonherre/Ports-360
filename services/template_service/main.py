from fastapi import FastAPI

app = FastAPI(title="Template Service")


@app.get("/health")
def health():
    return {"status": "ok"}
