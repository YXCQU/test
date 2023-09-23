import asyncio

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.post("/test")
async def root():
    await asyncio.sleep(2)
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6000)
