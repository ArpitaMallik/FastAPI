from fastapi import FastAPI

app = FastAPI()

@app.get('/') #create a route that listens to the get method
def hello():
    return {'message':"Hello World!"}


@app.get('/about')
def about():
    return {'message': 'I am Arpita Mallik and I am interested in AI and ML.'}