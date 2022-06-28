from fastapi import FastAPI
from routers import sampling
import server_cors
from wowt import wowt_app

app = FastAPI()
app.include_router(sampling.router)
server_cors.setup_cors_middleware(app)


@app.get("/")
async def main():
    return { "status": 200 }


@app.get("/version")
async def version():
    return wowt_app.version()