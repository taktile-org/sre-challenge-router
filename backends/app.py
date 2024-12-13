#!/usr/bin/env python3

from fastapi import HTTPException, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

import random
import time

app = FastAPI()

REQUEST_MEMORY = 0
DOWNTIME_MEMORY = 0


class Settings(BaseSettings):
    BACKEND_NAME: str = "no-number"

    # The number of requests after which the backend forgets the load
    REQUEST_FORGETFULNESS: int = 10
    LOAD_PER_REQUEST_S: int = 1

    # The chance of backend returning 500
    FAILURE_RATE: float = 0.0

    # The chance of backend going down
    DOWNTIME_RATE: float = 0

    # How many requests fail in a row in downtime period
    DOWNTIME_REQUEST_COUNT: int = 10

    model_config = SettingsConfigDict()


SETTINGS = Settings()

print(f"SETTINGS: {SETTINGS}")


def respect_failure_rate():
    if random.random() < SETTINGS.FAILURE_RATE:
        print(f"Decision: failure from {SETTINGS.BACKEND_NAME}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error from Backend {SETTINGS.BACKEND_NAME}",
        )
    print(f"Decision: success from {SETTINGS.BACKEND_NAME}")


def respect_load():
    global REQUEST_MEMORY
    REQUEST_MEMORY = REQUEST_MEMORY + 1

    time.sleep(SETTINGS.LOAD_PER_REQUEST_S * REQUEST_MEMORY)

    if REQUEST_MEMORY > SETTINGS.REQUEST_FORGETFULNESS:
        REQUEST_MEMORY = 0


def respect_downtime():
    global DOWNTIME_MEMORY
    if DOWNTIME_MEMORY > 0:
        # We are already in downtime
        DOWNTIME_MEMORY = DOWNTIME_MEMORY - 1
        print(f"Decision: downtime from {SETTINGS.BACKEND_NAME} | requests left in downtime: {DOWNTIME_MEMORY}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error from Backend {SETTINGS.BACKEND_NAME}",
        )

    if random.random() < SETTINGS.DOWNTIME_RATE:
        DOWNTIME_MEMORY = SETTINGS.DOWNTIME_REQUEST_COUNT - 1
        print(f"Decision: downtime from {SETTINGS.BACKEND_NAME}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error from Backend {SETTINGS.BACKEND_NAME}",
        )


@app.get("/{path:path}")
def read_root(path: str):
    respect_load()
    respect_failure_rate()
    respect_downtime()
    return {
        "message": f"Response from Backend {SETTINGS.BACKEND_NAME}",
        "metadata": {"backend": SETTINGS.BACKEND_NAME, "path": path},
    }
