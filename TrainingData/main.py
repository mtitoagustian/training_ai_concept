from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Load model yang telah disimpan
model = joblib.load("model_rf.pkl")

# Definisikan skema input data
class InputData(BaseModel):
    features: list

# Endpoint root
@app.get("/")
def read_root():
    return {"message": "Model API is running!"}

# Endpoint untuk prediksi
@app.post("/predict")
def predict(data: InputData):
    input_array = np.array(data.features).reshape(1, -1)
    prediction = model.predict(input_array)
    return {"prediction": int(prediction[0])}
