import pickle

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)



MODEL_VERSION = "1.0.0"