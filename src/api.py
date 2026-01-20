from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import papermill
import pandas
from prometheus_fastapi_instrumentator import Instrumentator
import json
import datetime


app = FastAPI()

@app.get("/health_check")
async def health_check():
    return {"status": "ok"}

