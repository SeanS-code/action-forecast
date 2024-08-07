from fastapi import FastAPI
from forecast.graphql.schema import graphql_app

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Forecast API"}

@app.get("/hello")
async def hello_world():
    return {"message": "Hello World"}

@app.get("/bye")
async def good_bye():
    return {"message": "Good Bye"}

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

