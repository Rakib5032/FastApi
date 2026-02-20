from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated, Literal
import json

app = FastAPI()

# pydantic class for patient data validation
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Patient id', examples=['P001'])]
    name: Annotated[str, Field(title="Name of the patient", description="Enter the patient Name here", examples=['Rakib', 'Rabbi'], max_length=25, min_length=2)]
    city: Annotated[str, Field(title='Name of the city', description='Enter the city name', examples=['Dhaka', 'Narsingdi'], max_length=20, min_length=3)]
    age: Annotated[int, Field(..., gt=0, lt=130)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Your gender here')]
    height: Annotated[float, Field(default=0.0, gt=0, strict=True)]
    weight: Annotated[float, Field(default=0.0, gt=0, lt=300, strict=True)]

    #computed field to calculate the bmi and verdict
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18:
            return 'Underweight'
        elif self.bmi <=25:
            return 'Normal'
        elif self.bmi <=30:
            return 'Overweight'
        else : return 'Obsese'


patient_info = {'id': 'P011', 'name': 'Rakib', 'city': 'Narsingdi', 'age': 25, 'gender': 'male', 'height': 1.64, 'weight': 67}

def get_info(patient: Patient):
    print(patient)
    print(patient.bmi)
    print(patient.verdict)

# patient1 = Patient(**patient_info)
# get_info(patient1)

# new_patient = patient1.model_dump()
# print(new_patient)

@app.get('/test')
def test():
    return new_patient


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


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


@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    # check if the data already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')

    # insert new patient data
    data[patient.id] = patient.model_dump(exclude={'id'})

    #save the data
    save_data(data)

    return  JSONResponse(status_code=201, content={'message': 'Patient created successfully'})
