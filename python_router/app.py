#!/usr/bin/env python
from fastapi import FastAPI
import httpx
from urllib.parse import urljoin
from collections import defaultdict
import time

app = FastAPI()

counter = 0
request_hits = defaultdict(int)

@app.get("/{path:path}")
async def route(path: str):
    global counter
    backends = [
            "http://backend_good:9000/",
            "http://backend_average:9000/",
            "http://backend_faulty:9000/",
    ]
    async with httpx.AsyncClient() as client:
        backend = backends[counter % len(backends)]
        counter += 1
        request_hits[backend] += 1
        start_time = time.time()
        response = await client.get(urljoin(backend, path))
        end_time = time.time()
        request_time = end_time - start_time
        print(f"Request time: {request_time} seconds from {backend}")

    return response.json().get("message")
