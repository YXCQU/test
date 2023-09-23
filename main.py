import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI()

limits = httpx.Limits(max_connections=500, max_keepalive_connections=900)
client = httpx.AsyncClient(timeout=7, limits=limits)


@app.post("/test")
async def root():
    url1 = "http://127.0.0.1:6000/test"
    resp = await client.post(url1)
    resp.json()
    return {"message": "main test1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
