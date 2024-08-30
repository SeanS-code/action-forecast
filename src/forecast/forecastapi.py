from fastapi import FastAPI, File, UploadFile

from forecast.graphql.schema import graphql_app
from forecast.model import run_model

from forecast.redis_scripts import generate_taskID, taskID_value, client_task

import pandas as pd
import uuid

app = FastAPI()

# Base API
# @app.get("/")
# async def root():
#     return {"message": "Forecast API"}

# @app.get("/hello")
# async def hello_world():
#     return {"message": "Hello World"}

# @app.get("/bye")
# async def good_bye():
#     return {"message": "Good Bye"}


# Model Instructions
@app.post("/data")
async def data_upload(csv_file: UploadFile):
    data = pd.read_csv(csv_file.file)
    data = data.dropna(axis=0)
    return {"filename": csv_file.filename}

@app.get("/model")
async def model():
    uu = uuid.uuid4()
    task_id = generate_taskID(str(uu))
    return task_id

@app.get("/model/task/{task_id}")
async def model_result(task_id: str):
    res = 1000
    redis_set = taskID_value(task_id, res)
    return {task_id: res}

# @app.post("/model/client/{value}")
# async def key_gen(value: str):
#     ctask_id = client_task(value)
#     return {ctask_id: value}

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

