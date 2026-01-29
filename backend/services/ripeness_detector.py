import requests

API_KEY = "WtpQAuMcgbhFxjzcuxFq"
MODEL = "fruit-ripeness-unjex"
VERSION = 2

def detect_ripeness(image_path):
    url = f"https://detect.roboflow.com/{MODEL}/{VERSION}?api_key={API_KEY}"

    with open(image_path, "rb") as img:
        response = requests.post(url, files={"file": img})

    data = response.json()
    print("🔍 RESPUESTA RIPENESS MODEL:", data)


    if "predictions" not in data or len(data["predictions"]) == 0:
        return "unknown"

    best = max(data["predictions"], key=lambda x: x["confidence"])
    return best["class"]