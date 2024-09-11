from fastapi import FastAPI, BackgroundTasks, Request
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

