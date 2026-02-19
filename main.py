from fastapi import FastAPI, Path, HTTPException, Query
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

@app.get("/view")
def data():
    return load_data()

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="Id of the patient", examples="P001")):
    data = load_data()
    
    # for id in data:
    #     if id == patient_id:
    #         return data[id]

    if patient_id in data:
        return data.get(patient_id)
    # return "Patient not found"
    raise HTTPException(status_code=404, detail="Patient Not found")

#query parameter
@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description='Sort on the basis of height, weight, bmi'), order: str = Query('asc', description='Sort in asc order')):

    # return sort_by
    
    valid_field = ['height', 'weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f'Not valid. Try with {valid_field}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f'Invalid order. Try with asc or desc')
    
    
    data = load_data()

    
    sorted_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sorted_order)
    return sorted_data