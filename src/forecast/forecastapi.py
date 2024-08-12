from fastapi import FastAPI, File, UploadFile
from forecast.graphql.schema import graphql_app

import pandas as pd

from forecast.model import run_model

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Forecast API"}

@app.get("/hello")
async def hello_world():
    return {"message": "Hello World"}

@app.get("/bye")
async def good_bye():
    return {"message": "Good Bye"}

@app.post("/data")
async def data_upload(csv_file: UploadFile):
    data = pd.read_csv(csv_file.file)
    print(run_model(data))
    return {"filename": csv_file.filename}

@app.get("/model/{task_id}")
async def model_results():
    return 

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

