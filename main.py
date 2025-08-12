from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=['John Doe'])]
    city: Annotated[str, Field(..., description="City of the patient", examples=['New York'])]
    age:  Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male','female','others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male','female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]





def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)
        

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    #new patient add to the db
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


#UPDATE
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing patient info -> pydantic obj -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pyd_obj = Patient(**existing_patient_info)
    
    #pydantic obj -> dict
    existing_patient_info = patient_pyd_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})




@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})



# @app.get('/') #create a route that listens to the get method
# def hello():
#     return {'message':"Patient Management System API"}


# @app.get('/about')
# def about():
#     return {'message': 'A fully functional API to manage your patient records'}

# @app.get('/view')
# def view():
#     data = load_data()

#     return data

# @app.get('/patient/{patient_id}')
# def view_patient(patient_id: str = Path(..., description="ID of the patient in the database", example="P001")):
#     #load all the patients
#     data = load_data()

#     if patient_id in data:
#         return data[patient_id]
#     raise HTTPException(status_code=404, detail="Patient not found")
    

# @app.get('/sort')
# def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc',description='Sort in asc or desc order')):

#     valid_fields = ['height', 'weight', 'bmi']
#     if sort_by not in valid_fields:
#         raise HTTPException(status_code=400, detail="Invalid sort field. Choose from height, weight, or bmi.")
    
#     if order not in ['asc', 'desc']:
#         raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'.")
    
#     data = load_data()

#     sort_order = True if order == 'desc' else False

#     sorted_data = sorted(data.values(), key=lambda x:x.get('height',0), reverse=sort_order)

#     return sorted_data