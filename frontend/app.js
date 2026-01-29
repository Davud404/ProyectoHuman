console.log("✅ app.js cargado correctamente");

const API = "http://localhost:8000";

async function captureImage() {
    showLoading();

    const img = document.getElementById("cameraFeed");
    img.src = `${API}/video_feed?${Date.now()}`; // congela

    const res = await fetch(`${API}/analyze/capture`, { method: "POST" });
    const data = await res.json();

    hideLoading();
    console.log("📦 RESPUESTA BACKEND:", data);
    showResult(data);
}


function showLoading() {
    document.getElementById("loading").classList.remove("hidden");
}

function hideLoading() {
    document.getElementById("loading").classList.add("hidden");
}


async function uploadImage(input) {
    const file = input.files[0];
    if (!file) return;

    showLoading();

    // Mostrar imagen subida en el recuadro
    const img = document.getElementById("cameraFeed");
    img.src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API}/analyze/upload`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    hideLoading();
    console.log("📦 RESPUESTA BACKEND:", data);
    showResult(data);
}


function showResult(data) {
    const label = document.getElementById("label");
    label.classList.remove("hidden");

    if (!data.fruit) {
        label.innerText = "No se detectó fruta 😢";
        return;
    }

    const fruit = data.fruit;
    const confidence = (data.confidence * 100).toFixed(1);
    const maturity = data.maturity.toLowerCase();

    label.className = "label"; // reset
    if (maturity.includes("verde")) label.classList.add("verde");
    else if (maturity.includes("maduro")) label.classList.add("maduro");
    else if (maturity.includes("sobremaduro")) label.classList.add("sobremaduro");
    else if (maturity.includes("podrido")) label.classList.add("podrido");
    else label.classList.add("desconocido");

    label.innerHTML = `
        🍎 <strong>Fruta:</strong> ${fruit}<br>
        🟡 <strong>Madurez:</strong> ${data.maturity}
    `;

    document.getElementById("feedback").classList.remove("hidden");
}

function resetFeedback() {
    document.getElementById("feedback").classList.add("hidden");
    document.getElementById("feedback-main").classList.remove("hidden");
    document.getElementById("feedback-detail").classList.add("hidden");
}

async function sendFeedback(correct) {
    await fetch(`${API}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            fruit_correct: true,
            maturity_correct: true,
            timestamp: Date.now()
        })
    });

    resetFeedback();
    alert("¡Gracias por el feedback!");
}

async function sendDetailedFeedback(fruitCorrect, maturityCorrect) {
    await fetch(`${API}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            fruit_correct: fruitCorrect,
            maturity_correct: maturityCorrect,
            timestamp: Date.now()
        })
    });

    resetFeedback();
    alert("¡Gracias por el feedback!");
}

function showDetailedFeedback() {
    document.getElementById("feedback-main").classList.add("hidden");
    document.getElementById("feedback-detail").classList.remove("hidden");
}
