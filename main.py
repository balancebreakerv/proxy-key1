import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/ip")
async def get_ip():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.ipify.org?format=json")
        return resp.json()

@app.post("/{full_path:path}")
async def proxy(full_path: str, request: Request):
    body = await request.json()
    query_params = request.query_params
    headers = dict(request.headers)

    # Build target URL, preserving query parameters
    target_url = f"https://generativelanguage.googleapis.com/{full_path}"
    if query_params:
        target_url += "?" + str(query_params)

    async with httpx.AsyncClient(timeout=600) as client:
        resp = await client.post(
            target_url,
            headers={
                k: v for k, v in headers.items()
                if k.lower() in ("x-goog-api-key", "content-type")
            },
            json=body,
        )
        return JSONResponse(content=resp.json())
