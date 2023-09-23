import asyncio

import uvicorn
from sanic import Sanic, json
from curl_cffi import requests

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = Sanic("CurlCffi")


@app.listener('before_server_start')
def init(app1, loop):
    app1.ctx.curl_session = requests.AsyncSession()


@app.listener('after_server_stop')
def finish(app1, loop):
    loop.run_until_complete(app1.ctx.curl_session.close())
    loop.close()


@app.get("/test")
async def async_main(request):
    async with requests.AsyncSession() as s:
        r = await s.get("https://httpbin.org/headers", timeout=30)
    print(r.text)
    return json({"test": "test"})


@app.get("/test-multi")
async def async_better(request):
    r = await app.ctx.curl_session.get("https://httpbin.org/headers", timeout=30)
    print(r.text)
    return json({"test": "test"})


@app.get("/test-concurrency")
async def async_best(request):
    tasks = []
    for _ in range(10):
        task = app.ctx.curl_session.get("https://httpbin.org/headers", timeout=30)
        tasks.append(task)
    print([getattr(task, "text") for task in await asyncio.gather(*tasks)])
    return json({"test": "test"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
