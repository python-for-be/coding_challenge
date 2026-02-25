from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def ping_health():
    return {"status": "OK", "version": "0.0.1"}