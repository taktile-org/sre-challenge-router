#!/usr/bin/env python
from fastapi import FastAPI
import httpx

import random

app = FastAPI()


@app.get("/")
async def route():
    backends = [
            "http://backend_good:9000/",
            "http://backend_sometime_works:9000/",
            "http://backend_faulty:9000/",
            "http://backend_average:9000/",
    ]
    async with httpx.AsyncClient() as client:
        backend = random.choice(backends)
        response = await client.get(backend)

    return response.json().get("message")
