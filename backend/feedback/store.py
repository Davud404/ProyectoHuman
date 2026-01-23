import json
from datetime import datetime

FILE = "feedback.json"

def save_feedback(data):
    data["timestamp"] = datetime.now().isoformat()

    try:
        with open(FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(data)

    with open(FILE, "w") as f:
        json.dump(history, f, indent=4)
