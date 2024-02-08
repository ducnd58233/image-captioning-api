import torchvision.transforms as T
from PIL import Image
from common.constants import AI_MODEL, INPUT_SIZE, VOCABULARY_DICT

def predict(file):
    transform = T.Compose(
        [
            T.Resize(INPUT_SIZE),
            T.ToTensor(),
            T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    
    image = transform(Image.open(file).convert("RGB")).unsqueeze(0)
    return ' '.join(AI_MODEL.caption_image(image, VOCABULARY_DICT))
