from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pandas as pd
from schema.user_input import UserInput
from config.city_tier import tier_1_cities, tier_2_cities


app = FastAPI()
    

@app.get('/')
def home():
    return {"message": "Welcome to the Insurance Premium Category Predictor API!"}


@app.get('/health')
def health_check():
    return {
        'status': 'healthy',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }




@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    # Prediction
    predicted_class = model.predict(input_df)[0]

    # Probabilities for each class
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        class_labels = model.classes_
        class_probabilities = dict(zip(class_labels, probabilities))
        confidence = float(class_probabilities[predicted_class])
    else:
        # If the model doesn't support predict_proba
        class_probabilities = {}
        confidence = None

    return JSONResponse(status_code=200, content={
        "response": {
            "predicted_category": predicted_class,
            "confidence": confidence,
            "class_probabilities": class_probabilities
        }
    })




