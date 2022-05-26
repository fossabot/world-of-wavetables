from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# PLEASE REMOVE FROM PRODUCTION
ORIGINS_DEV = [
    "http://localhost",
    "http://localhost:4200",
    "https://localhost",
    "https://localhost:4200",
]


def setup_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS_DEV,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )