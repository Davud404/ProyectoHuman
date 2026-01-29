from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import torch
import os
import shutil

from model.loader import load_model, CLASSES
from vision.preprocess import preprocess_image
from vision.hsv import estimate_maturity
from camera.webcam import capture_image
from feedback.store import save_feedback
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from services.fruit_detector import detect_fruit
from services.ripeness_detector import detect_ripeness
from camera.webcam import capture_image, get_frame

FRUIT_TRANSLATION = {
    "apple": "Manzana",
    "avocado": "Aguacate",
    "banana": "Banano",
    "cherry": "Cereza",
    "kiwi": "Kiwi",
    "mango": "Mango",
    "orange": "Naranja",
    "pineapple": "Piña",
    "strawberries": "Fresa",
    "watermelon": "Sandía"
}

MATURITY_TRANSLATION = {
    "Unripe": "Verde",
    "Ripe": "Maduro",
    "Overripe": "Pasado",
    "Rotten": "Podrido"
}


app = FastAPI()

directorio_actual = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(directorio_actual, 'model.pth')
model = load_model(MODEL_PATH)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_frames():
    while True:
        frame = get_frame()
        if frame is None:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

os.makedirs("temp", exist_ok=True)

# 📤 Subir imagen
@app.post("/analyze/upload")
async def analyze_upload(file: UploadFile = File(...)):
    image_path = f"temp/{file.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    fruit_data = detect_fruit(image_path)
    raw_maturity = detect_ripeness(image_path)

    fruit_en = fruit_data["fruit"]
    fruit_es = FRUIT_TRANSLATION.get(fruit_en, fruit_en)

    maturity_es = MATURITY_TRANSLATION.get(raw_maturity, "Desconocido")

    return {
        "fruit": fruit_es,
        "confidence": fruit_data["confidence"],
        "maturity": maturity_es
    }


# 📸 Capturar desde webcam
@app.post("/analyze/capture")
def analyze_capture():
    image_path = capture_image()

    if image_path is None:
        return {"error": "No se pudo capturar imagen"}

    fruit_data = detect_fruit(image_path)
    raw_maturity = detect_ripeness(image_path)

    fruit_en = fruit_data["fruit"]
    fruit_es = FRUIT_TRANSLATION.get(fruit_en, fruit_en)

    maturity_es = MATURITY_TRANSLATION.get(raw_maturity, "Desconocido")

    return {
        "fruit": fruit_es,
        "confidence": fruit_data["confidence"],
        "maturity": maturity_es
    }

'''
@app.post("/analyze/upload")
async def analyze_upload(file: UploadFile = File(...)):
    image_bytes = await file.read()
    np_img = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    return analyze(image)

@app.post("/analyze/capture")
def analyze_capture():
    image = get_frame()
    cv2.imwrite("assets/images/latest.jpg", image)
    return analyze(image)'''

def analyze(image):
    tensor = preprocess_image(image)
    with torch.no_grad():
        outputs = model(tensor)
        idx = outputs.argmax().item()
        fruit = CLASSES[idx]

    maturity = estimate_maturity(image, fruit)

    return {
        "fruit": fruit,
        "maturity": maturity
    }

@app.post("/feedback")
def feedback(data: dict):
    save_feedback(data)
    return {"status": "ok"}

from feedback.store import get_feedback_stats

@app.get("/feedback/stats")
def feedback_stats():
    return get_feedback_stats()
