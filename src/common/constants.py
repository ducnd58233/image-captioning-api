import os
import json
import torch
import torchvision.transforms as T
from models.cnn_to_rnn import CNNtoRNN

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

INPUT_SIZE = (384, 384)
EMBED_SIZE = 256
HIDDEN_SIZE = 256
NUM_LAYERS = 1

ROOT_DIR = f'{os.path.dirname(os.getcwd())}/models'
WEIGHT = f"{ROOT_DIR}/CNNtoRNN/2024-02-07 08:10:38.740121_2024-02-07 15:03:14.524717_fold-1_epoch-10_384_BS-32_bleu-score-0.188.pth"

with open(f'{ROOT_DIR}/vocab.json') as f:
    VOCABULARY_DICT = json.load(f)

AI_MODEL = CNNtoRNN(EMBED_SIZE, HIDDEN_SIZE, len(VOCABULARY_DICT['itos']), NUM_LAYERS)
AI_MODEL.load_state_dict(torch.load(WEIGHT)['model_state_dict'])
AI_MODEL.eval()
    