from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return{"Root": "Root"}

@app.get("/hello")
def hello_world():
    return {"Hello": "World"}

@app.get("/bye")
def good_bye():
    return {"Good": "Bye"}