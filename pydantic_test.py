from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    # name: str = Field(max_length=20)
    name: Annotated[str, Field(max_length=20, min_length=2, title='Name of the patient', description='Give name here', examples=['Rakib'])]
    email: EmailStr
    age: int = Field(gt=0)
    weight: Annotated[float, Field(default=0.0, gt=0, strict=True)]
    height: Annotated[float, Field(gt=0, strict=True)]
    married: Optional[bool] = None
    allergies: List[str]
    address: Dict[str, str]

    @field_validator('email')
    @classmethod

    def email_validator(cls, value):
        valid_domains = ['diu.edu', 'edu.bd'] 
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not valid')
        return value
    
    @field_validator('name')
    @classmethod
    def name_conversion(cls, value):
        return value.upper()
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 50 and 'emergency_contact' not in model.address:
            raise ValueError('No emergency Contact')
        return model
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.address)
    print('bmi', patient.bmi)

def update(patient: Patient):
    print(patient)


patient_info = {'name': 'rakib', 'email': 'adsfsadfbc@edu.bd' ,'age': 100, 'weight': 67.5, 'height': 1.64, 'allergies': ['dust', 'others'], 'address':{'emergency_contact': '12345'}}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)
update(patient1)