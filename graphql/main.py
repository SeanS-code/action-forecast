from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return{"Root": "Root"}

@app.get("/graphql")
def query():
    return {"blank": "blank"}