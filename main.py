from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated, Literal
import json

app = FastAPI()

# pydantic class for patient data validation
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Patient id', examples=['P001'])]
    name: Annotated[str, Field(..., title="Name of the patient", description="Enter the patient Name here", examples=['Rakib', 'Rabbi'], max_length=25, min_length=2)]
    city: Annotated[str, Field(..., title='Name of the city', description='Enter the city name', examples=['Dhaka', 'Narsingdi'], max_length=20, min_length=3)]
    age: Annotated[int, Field(..., gt=0, lt=130)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Your gender here')]
    height: Annotated[float, Field(..., gt=0, strict=True)]
    weight: Annotated[float, Field(..., gt=0, lt=300, strict=True)]

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


# patient_info = {'id': 'P011', 'name': 'Rakib', 'city': 'Narsingdi', 'age': 25, 'gender': 'male', 'height': 1.64, 'weight': 67}

# patient1 = Patient(**patient_info)
# get_info(patient1)

# new_patient = patient1.model_dump()
# print(new_patient)

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


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

#create new patient
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

#update patient
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Patient):
    data = load_data()

    #check if the patient exist
    if patient_id not in data:
        raise HTTPException(status_code=404, detail={'message': 'Patient Not exist'})
    
    #extract data from json
    existing_patient_info = data[patient_id]
    #keep only inserted field or data
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    #update inserted data
    for info in updated_patient_info:
        existing_patient_info[info] = updated_patient_info[info]

    #need to update the bmi and status
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    #update in json
    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Updated Successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not found')
    
    data.pop(patient_id)
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient Deleted'})

    