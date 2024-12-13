#!/usr/bin/env python
from fastapi import FastAPI
import httpx

import random
from urllib.parse import urljoin

app = FastAPI()


@app.get("/{path:path}")
async def route(path: str):
    backends = [
            "http://backend_good:9000/",
            "http://backend_sometime_works:9000/",
            "http://backend_faulty:9000/",
            "http://backend_average:9000/",
    ]
    async with httpx.AsyncClient() as client:
        backend = random.choice(backends)
        response = await client.get(urljoin(backend, path))

    return response.json().get("message")
