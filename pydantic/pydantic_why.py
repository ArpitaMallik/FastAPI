from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List,Dict, Optional, Annotated

class Patient(BaseModel):
    #name: str = Field(max_length=50)
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Full name of the patient', examples=["John Doe", "Jane Smith"])]    #metadata
    email: EmailStr
    web: AnyUrl
    age: int = Field(gt=0, le=120)
    # weight: float = Field(gt=0)
    weight: Annotated[float, Field(gt=0, description='Weight of the patient in kg', strict=True)]
    # married: bool = False
    married: Annotated[bool, Field(default=None, description='Is the patient married?')]
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]
 

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('Inserted patient data successfully!')


patient_info = {'name': "Nitish Singh",
                "age": 30,
                "email": 'abc@gmail.com',
                "web": 'https://example.com',
                "weight": 54.5,
                'married': True,
                'allergies': ['pollen', 'dust'],
                'contact_details': {'email': 'abc@gmail.com','phone':'0293924'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)