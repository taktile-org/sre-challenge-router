#!/usr/bin/env python
from fastapi import FastAPI
import httpx

from urllib.parse import urljoin

app = FastAPI()


@app.get("/{path:path}")
async def route(path: str):
    backends = [
            "http://backend_good:9000/",
            "http://backend_average:9000/",
            "http://backend_faulty:9000/",
    ]
    async with httpx.AsyncClient() as client:
        backend = backends[0]
        response = await client.get(urljoin(backend, path))

    return response.json().get("message")
