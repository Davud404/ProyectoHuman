import cv2
import torch
import numpy as np
from torchvision import transforms

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((100,100)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
])

def preprocess_image(image):

    '''
    image = cv2.resize(image, (100, 100))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = image / 255.0
    image = np.transpose(image, (2, 0, 1))  # C,H,W'''
    img = cv2.resize(image, (100,100))

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    tensor = transform(img_rgb).unsqueeze(0)
    return tensor


