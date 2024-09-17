from fastapi import FastAPI, BackgroundTasks, Request
from forecast.graphql.schema import graphql_app
from forecast import forecast

app = FastAPI()

def callmodel(requestid: str, data: str):
    forecast.submitreq(requestid, data)

@app.get("/")
async def root():
    return {"message": "Forecast API"}

@app.post("/predict")
async def predictreq(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()

    requestid = forecast.generatereq()

    background_tasks.add_task(callmodel, requestid, data)

    return {"results": f"/results/{requestid}"}

@app.get("/results/{requestid}")
async def resultsres(requestid: str):

    res = forecast.predictres(requestid)

    return {"results": res}

@app.get("/results")
async def returnallreq():

    res = forecast.returnallreq()

    return {"results": res}

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

