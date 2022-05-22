from fastapi import FastAPI
import wowt_app

app = FastAPI()

@app.get("/")
async def main():
    return { "status": 200 }

@app.get("/about")
async def version():
    return wowt_app.version()