from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from services.image_caption_generator import predict

app = FastAPI()

@app.get("/ping")
def healthz():
    return "ok"

@app.post("/predict")
async def generate_caption(file: UploadFile = File(...)):
    request_object_content = await file.read()
    return predict(BytesIO(request_object_content))