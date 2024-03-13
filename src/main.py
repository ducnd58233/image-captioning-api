from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image
from loguru import logger
from src.services.image_caption_generator import predict
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

# Transformers model
model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)
feature_extractor = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

max_length = 20
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# Tracer
set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "image-captioning"}))
)
tracer = get_tracer_provider().get_tracer("ic-app", "latest")
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)

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
    with tracer.start_as_current_span('processors') as processors:
        with tracer.start_as_current_span(
            "image-loader", links=[trace.Link(processors.get_span_context())]
        ):
            request_object_content = await file.read()
            pil_image = Image.open(BytesIO(request_object_content))
            
            pixel_values = feature_extractor(
                images=[pil_image], return_tensors="pt"
            ).pixel_values

            logger.info("Reading image successfully!")
        
        with tracer.start_as_current_span(
            "predictor", links=[trace.Link(processors.get_span_context())]
        ):
            output_ids = model.generate(pixel_values, **gen_kwargs)

            preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

            preds = [pred.strip() for pred in preds]

            logger.info("Generated caption for image successfully!")

            return {"caption": preds[0]}
