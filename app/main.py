from fastapi import FastAPI
from .api import router


app=FastAPI()

@app.get("/")
def home():
    return {'msg':'Hello World'}

app.include_router(router)