const API_URL = "http://localhost:8000";

let lastResult = null;

function captureImage() {
    fetch(`${API_URL}/analyze/capture`, { method: "POST" })
        .then(res => res.json())
        .then(data => showResult(data))
        .catch(() => alert("Error capturando imagen"));
}

function uploadImage(input) {
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    fetch(`${API_URL}/analyze/upload`, {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        const reader = new FileReader();
        reader.onload = () => {
            showResult(data, reader.result);
        };
        reader.readAsDataURL(file);
    })
    .catch(err => alert("Error subiendo imagen"));
}

function showResult(data) {
    const label = document.getElementById("label");
    const feedback = document.getElementById("feedback");

    label.innerText = `${data.fruit} - ${data.maturity}`;
    label.className = `label ${data.maturity}`;
    label.classList.remove("hidden");

    feedback.classList.remove("hidden");

    lastResult = data;
}

function sendFeedback(isCorrect) {
    if (!lastResult) return;

    fetch(`${API_URL}/feedback`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            fruit: lastResult.fruit,
            maturity: lastResult.maturity,
            correct: isCorrect
        })
    });

    alert("Gracias por tu retroalimentación 🙌");
}
