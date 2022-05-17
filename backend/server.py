from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
    return { "status": 200 }

@app.get("/about")
async def version():
    pass