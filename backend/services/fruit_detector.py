import requests

API_KEY = "WtpQAuMcgbhFxjzcuxFq"
MODEL = "fruit-vtdgm"
VERSION = 1

def detect_fruit(image_path):
    url = f"https://classify.roboflow.com/{MODEL}/{VERSION}?api_key={API_KEY}"

    with open(image_path, "rb") as img:
        response = requests.post(url, files={"file": img})

    data = response.json()
    print("🔍 RESPUESTA FRUIT MODEL:", data)

    if "predictions" not in data or len(data["predictions"]) == 0:
        return None

    best = max(data["predictions"], key=lambda x: x["confidence"])

    return {
        "fruit": best["class"],
        "confidence": best["confidence"]
    }