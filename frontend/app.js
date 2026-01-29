console.log("✅ app.js cargado correctamente");

const API = "http://localhost:8000";

async function captureImage() {
    const res = await fetch(`${API}/analyze/capture`, { method: "POST" });
    const data = await res.json();
    console.log("📦 RESPUESTA BACKEND:", data);
    showResult(data);
}

async function uploadImage(input) {
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API}/analyze/upload`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    console.log("📦 RESPUESTA BACKEND:", data);
    showResult(data);
}

function showResult(data) {
    console.log("🧠 showResult recibe:", data);

    const label = document.getElementById("label");
    label.classList.remove("hidden");

    if (!data.fruit) {
        label.innerText = "No se detectó fruta 😢";
        return;
    }

    const fruitName = data.fruit.fruit;
    const confidence = (data.fruit.confidence * 100).toFixed(1);
    const ripeness = data.ripeness;

    label.innerHTML = `
        <strong>Fruta:</strong> ${fruitName}<br>
        <strong>Confianza:</strong> ${confidence}%<br>
        <strong>Madurez:</strong> ${ripeness}
    `;

    document.getElementById("feedback").classList.remove("hidden");
}

async function sendFeedback(correct) {
    await fetch(`${API}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correct, timestamp: Date.now() })
    });

    alert("¡Gracias por el feedback!");
}
