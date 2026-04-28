import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/{full_path:path}")
async def proxy(full_path: str, request: Request):
    body = await request.json()
    headers = dict(request.headers)
    async with httpx.AsyncClient(timeout=600) as client:
        resp = await client.post(
            f"https://generativelanguage.googleapis.com/{full_path}",
            headers={k: v for k, v in headers.items() if k.lower() in ["x-goog-api-key", "content-type"]},
            json=body
        )
        return JSONResponse(content=resp.json())
