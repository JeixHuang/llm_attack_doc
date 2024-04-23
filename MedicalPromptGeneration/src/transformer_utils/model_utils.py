# src/transformer_utils/model_utils.py
from transformers import AutoModel

def load_model(model_path):
    return AutoModel.from_pretrained(model_path)
