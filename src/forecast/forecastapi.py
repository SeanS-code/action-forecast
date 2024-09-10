from fastapi import FastAPI, BackgroundTasks, File, UploadFile, Request
from forecast.graphql.schema import graphql_app
from forecast import forecast

app = FastAPI()

def predict(requestid: str):
    forecast.predictres(requestid)

@app.get("/")
async def root():
    return {"message": "Forecast API"}

@app.post("/predict")
async def predictreq(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()

    requestid = forecast.submitreq(data)

    background_tasks.add_task(predict, requestid)

    return {"results": f"/results/{requestid}"}

@app.get("/results/{requestid}")
async def predictres(requestid: str):

    res = forecast.predictres(requestid)
    
    return {"results": res}

@app.get("/results")
async def returnallreq():

    res = forecast.returnallreq()
    
    return {"results": res}

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

# Base API

# @app.get("/hello")
# async def hello_world():
#     return {"message": "Hello World"}

# @app.get("/bye")
# async def good_bye():
#     return {"message": "Good Bye"}


# Model Instructions
# @app.post("/data")
# async def data_upload(csv_file: UploadFile):
#     data = pd.read_csv(csv_file.file)
#    data = data.dropna(axis=0)
#     return {"filename": csv_file.filename}

# @app.get("/model")
# async def model():
#     uu = uuid.uuid4()
#     task_id = generate_taskID(str(uu))
#     return task_id

# @app.post("/model/client/{value}")
# async def key_gen(value: str):
#     ctask_id = client_task(value)
#     return {ctask_id: value}

