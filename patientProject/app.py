from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from schema.user_input import UserInput
from model.predict import predict_output, MODEL_VERSION, model
from schema.pred_response import PredictionResponse

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

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    # Wrap in a list so DataFrame is shaped correctly for predict.py
    user_input_list = [user_input]

    # Get prediction
    predicted_class = predict_output(user_input_list)

    # Calculate probabilities if supported
    if hasattr(model, "predict_proba"):
        input_df = pd.DataFrame(user_input_list)
        probabilities = model.predict_proba(input_df)[0]
        class_labels = model.classes_
        class_probabilities = dict(zip(class_labels, probabilities))
        confidence = float(class_probabilities[predicted_class])
    else:
        class_probabilities = {}
        confidence = None

    return JSONResponse(status_code=200, content={
        "response": {
            "predicted_category": predicted_class,
            "confidence": confidence,
            "class_probabilities": class_probabilities
        }
    })
