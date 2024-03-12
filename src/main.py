from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image
from src.services.image_caption_generator import predict
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)
feature_extractor = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

app = FastAPI()

@app.get("/ping")
def healthz():
    return "ok"

@app.post("/v1/caption")
async def generate_caption(file: UploadFile = File(...)):
    request_object_content = await file.read()
    preds = predict(BytesIO(request_object_content))
    
    return {"caption": preds}

@app.post("/v2/caption")
async def generate_caption(file: UploadFile = File(...)):
    request_object_content = await file.read()
    pil_image = Image.open(BytesIO(request_object_content))

    pixel_values = feature_extractor(images=[pil_image], return_tensors="pt").pixel_values

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

    preds = [pred.strip() for pred in preds]

    return {"caption": preds[0]}
