import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/v1/messages")
async def proxy(request: Request):
    body = await request.json()
    headers = dict(request.headers)
    async with httpx.AsyncClient(timeout=600) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={k: v for k, v in headers.items() if k.lower() in ["x-api-key", "anthropic-version", "content-type"]},
            json=body
        )
        return JSONResponse(content=resp.json())
