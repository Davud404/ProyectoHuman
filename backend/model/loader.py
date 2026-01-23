import torch
from model.cnn import FruitCNN

DEVICE = "cpu"

CLASSES = [
    'Apple', 'Apricot', 'Avocado', 'Banana', 'Dragonfruit', 'Kiwi',
    'Lemon', 'Lemon Meyer', 'Limes', 'Mandarine', 'Mango', 'Mango Red',
    'Orange', 'Papaya', 'Peach', 'Pear', 'Plum', 'Pomelo',
    'Strawberry', 'Tomato', 'Watermelon'
]

def load_model(model_path: str):
    model = FruitCNN().to(DEVICE)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.eval()
    return model
