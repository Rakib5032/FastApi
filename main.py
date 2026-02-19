from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {'message': 'Patient Mangement System'}

@app.get('/about')
def about():
    return {'Message': 'Fully functional Patient record system'}

@app.get("/data")
def data():
    return load_data()