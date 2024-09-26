from fastapi import FastAPI, BackgroundTasks, Request
from forecast.graphql.schema import graphql_app
from forecast import forecast

import os

# export UNRELIABLE=True before starting forecastapi
unreliable = os.environ.get("UNRELIABLE")

app = FastAPI()


def asyncreqsubmit(requestid: str, data: str):
    forecast.submitreq(requestid, data)
    forecast.predictmodel(requestid)


def reqsubmit(requestid: str):
    forecast.predictmodel(requestid)


@app.get("/")
async def root():
    return {"message": "Forecast API"}


@app.post("/predict")
async def predictreq(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()

    requestid = forecast.generatereq()

    # check if the "UNRELIABLE" environment variable exists
    if unreliable is not None and unreliable == "True":
        background_tasks.add_task(asyncreqsubmit, requestid, data)
    else:
        forecast.submitreq(requestid, data)
        background_tasks.add_task(reqsubmit, requestid)

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
