import json
import torch
import torchvision.transforms as T

from pathlib import Path

from src.models.cnn_to_rnn import CNNtoRNN
from .get_latest_model import get_latest_and_highest_score_model


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_SIZE = (384, 384)
EMBED_SIZE = 256
HIDDEN_SIZE = 256
NUM_LAYERS = 1

ROOT_DIR = f"{BASE_DIR}/models/CNNtoRNN"
WEIGHT = get_latest_and_highest_score_model(ROOT_DIR)

with open(f"{BASE_DIR}/models/vocab.json") as f:
    VOCABULARY_DICT = json.load(f)

AI_MODEL = CNNtoRNN(EMBED_SIZE, HIDDEN_SIZE, len(VOCABULARY_DICT["itos"]), NUM_LAYERS)
AI_MODEL.load_state_dict(
    torch.load(WEIGHT, map_location=torch.device("cpu"))["model_state_dict"]
)
AI_MODEL.eval()
