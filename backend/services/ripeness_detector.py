import requests

API_KEY = "WtpQAuMcgbhFxjzcuxFq"
MODEL = "fruit-ripeness-unjex"
VERSION = 2

def detect_ripeness(image_path):
    url = f"https://detect.roboflow.com/{MODEL}/{VERSION}?api_key={API_KEY}"

    with open(image_path, "rb") as img:
        response = requests.post(url, files={"file": img})

    data = response.json()

    if "predictions" not in data or len(data["predictions"]) == 0:
        return "Unknown"

    best = max(data["predictions"], key=lambda x: x["confidence"])

    # Ejemplo: "Mango Unripe" → "Unripe"
    raw_class = best["class"]
    maturity = raw_class.split()[-1]

    return maturity