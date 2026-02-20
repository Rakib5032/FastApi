from pydantic import BaseModel

class Address(BaseModel):
    district: str
    post: int

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

def show_info(patient: Patient):
    print(patient.name)
    print(patient.gender)
    print(patient.age)
    print(patient.address.district)
    print(patient.address.post)
    print('All doen')
    print(patient)

address_info = {'district': 'Narsingdi', 'post': 1500}
address1 = Address(**address_info)

# patient_info = {'name': 'Rakib', 'gender': 'male', 'age': 25,'address':{'district': 'Narsingdi', 'post': 1600}}

patient_info = {'name': 'Rakib', 'gender': 'male', 'age': 25,'address':address1}

patient1 = Patient(**patient_info)
# show_info(patient1)

temp_data = patient1.model_dump()
print(temp_data)
print(len(temp_data))
print(type(temp_data))


