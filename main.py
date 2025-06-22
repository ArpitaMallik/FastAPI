from fastapi import FastAPI

app = FastAPI()

@app.get('/') #create a route that listens to the get method
def hello():
    return ('message':"Hello World!")