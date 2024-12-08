#!/usr/bin/env python3

from fastapi import HTTPException, FastAPI

import os
import random
import time

app = FastAPI()

REQUEST_MEMORY = 0
REQUEST_FORGETFULNESS = 10

BACKEND_NAME = os.environ.get("BACKEND_NAME", "no-number")
try:
    FAILURE_RATE = float(os.environ.get("FAILURE_RATE", 0.0))
except ValueError:
    print(f"Failed to parse FAILURE_RATE: {os.environ.get('FAILURE_RATE')}")
    FAILURE_RATE = 0.0
try:
    LOAD_PER_REQUEST_S = int(os.environ.get("LOAD_PER_REQUEST_S", 0))
except ValueError:
    print(f"Failed to parse LOAD_PER_REQUEST_S: {os.environ.get('LOAD_PER_REQUEST_S')}")
    LOAD_PER_REQUEST_S = 1

print(f"Started Backend: {BACKEND_NAME}")
print(f"Failure Rate: {FAILURE_RATE}")
print(f"Load per request: {LOAD_PER_REQUEST_S}")


def respect_failure_rate():
    if random.random() < FAILURE_RATE:
        print(f"Decision: failure from {BACKEND_NAME}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error from Backend {BACKEND_NAME}",
        )
    print(f"Decision: success from {BACKEND_NAME}")


def respect_load():
    global REQUEST_MEMORY
    REQUEST_MEMORY = REQUEST_MEMORY + 1

    time.sleep(LOAD_PER_REQUEST_S * REQUEST_MEMORY)

    if REQUEST_MEMORY > REQUEST_FORGETFULNESS:
        REQUEST_MEMORY = 0


@app.get("/")
def read_root():
    respect_load()
    respect_failure_rate()
    return {
        "message": f"Response from Backend {BACKEND_NAME}",
        "metadata": {"backend": BACKEND_NAME},
    }
