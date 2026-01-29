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

def get_feedback_stats():
    try:
        with open(FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

    stats = {
        "both_correct": 0,
        "fruit_only": 0,
        "maturity_only": 0,
        "both_wrong": 0
    }

    for item in history:
        fruit_ok = item.get("fruit_correct", False)
        maturity_ok = item.get("maturity_correct", False)

        if fruit_ok and maturity_ok:
            stats["both_correct"] += 1
        elif fruit_ok and not maturity_ok:
            stats["fruit_only"] += 1
        elif not fruit_ok and maturity_ok:
            stats["maturity_only"] += 1
        else:
            stats["both_wrong"] += 1

    return stats
