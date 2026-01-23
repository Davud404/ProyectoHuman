import torch
import torch.nn as nn
from torchvision import transforms
import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
IMG_SIZE = 100
WINDOW_W, WINDOW_H = 800, 600

directorio_actual = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(directorio_actual, 'best_model_sgd.pth')
DEVICE = torch.device("cpu")

# ===============================
# CLASES DEL MODELO (21)
# ===============================
CLASS_NAMES = [
    'Apple', 'Apricot', 'Avocado', 'Banana', 'Dragonfruit', 'Kiwi',
    'Lemon', 'Lemon Meyer', 'Limes', 'Mandarine', 'Mango', 'Mango Red',
    'Orange', 'Papaya', 'Peach', 'Pear', 'Plum', 'Pomelo',
    'Strawberry', 'Tomato', 'Watermelon'
]

# ===============================
# DEFINICIÓN DEL MODELO CNN
# ===============================
class FruitCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 22 * 22, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 21)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 16 * 22 * 22)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# ===============================
# CARGAR MODELO
# ===============================
model = FruitCNN().to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()

# ===============================
# TRANSFORMACIÓN DE IMAGEN
# ===============================
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((100,100)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
])

# ===============================
# ANÁLISIS DE MADUREZ HSV
# (21 CLASES – UNA POR UNA)
# ===============================
def procesar_hsv(img_bgr_100, clase):
    hsv = cv2.cvtColor(img_bgr_100, cv2.COLOR_BGR2HSV)
    h = np.mean(hsv[:, :, 0])
    s = np.mean(hsv[:, :, 1])
    v = np.mean(hsv[:, :, 2])

    # ---- MANZANA ----
    if clase == "Apple":
        return "Maduro" if (h < 15 or h > 160) else "Verde"

    # ---- ALBARICOQUE ----
    if clase == "Apricot":
        return "Maduro" if s > 80 else "Verde"

    # ---- AGUACATE ----
    if clase == "Avocado":
        return "Maduro" if v < 110 else "Verde"

    # ---- BANANO ----
    if clase == "Banana":
        if h < 25:
            return "Pasado"
        elif h < 40:
            return "Maduro"
        else:
            return "Verde"

    # ---- DRAGON FRUIT ----
    if clase == "Dragonfruit":
        return "Maduro" if h < 20 else "Verde"

    # ---- KIWI ----
    if clase == "Kiwi":
        return "Maduro" if v < 120 else "Verde"

    # ---- LIMÓN ----
    if clase == "Lemon":
        return "Maduro" if h < 35 else "Verde"

    # ---- LIMÓN MEYER ----
    if clase == "Lemon Meyer":
        return "Maduro" if h < 35 else "Verde"

    # ---- LIMES ----
    if clase == "Limes":
        return "Verde" if h > 40 else "Maduro"

    # ---- MANDARINA ----
    if clase == "Mandarine":
        return "Maduro" if h < 30 else "Verde"

    # ---- MANGO ----
    if clase == "Mango":
        return "Maduro" if h < 35 else "Verde"

    # ---- MANGO ROJO ----
    if clase == "Mango Red":
        return "Maduro" if h < 25 else "Verde"

    # ---- NARANJA ----
    if clase == "Orange":
        return "Maduro" if h < 30 else "Verde"

    # ---- PAPAYA ----
    if clase == "Papaya":
        return "Maduro" if h < 35 else "Verde"

    # ---- DURAZNO ----
    if clase == "Peach":
        return "Maduro" if s > 85 else "Verde"

    # ---- PERA ----
    if clase == "Pear":
        return "Maduro" if s > 80 else "Verde"

    # ---- CIRUELA ----
    if clase == "Plum":
        return "Maduro" if s > 90 else "Verde"

    # ---- POMELO ----
    if clase == "Pomelo":
        return "Maduro" if h < 35 else "Verde"

    # ---- FRESA ----
    if clase == "Strawberry":
        return "Maduro" if h < 15 else "Verde"

    # ---- TOMATE ----
    if clase == "Tomato":
        if h < 10:
            return "Maduro"
        elif h < 20:
            return "Pasado"
        else:
            return "Verde"

    # ---- SANDÍA ----
    if clase == "Watermelon":
        return "Maduro" if v < 120 else "Verde"

    return "Verde"

# ===============================
# FUNCIÓN PRINCIPAL
# ===============================
def analizar_imagen(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor = transform(img_rgb).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        pred = torch.argmax(output, dim=1).item()
        clase = CLASS_NAMES[pred]

    estado = procesar_hsv(img, clase)
    visualizar_resultado(img, clase, estado)

# ===============================
# VISUALIZACIÓN FINAL (CANVAS)
# ===============================
def visualizar_resultado(img_100, clase, estado):
    canvas = np.full((WINDOW_H, WINDOW_W, 3), (230, 230, 230), dtype=np.uint8)

    FRUIT_SIZE = 300
    img_vis = cv2.resize(img_100, (FRUIT_SIZE, FRUIT_SIZE), interpolation=cv2.INTER_CUBIC)

    x0 = (WINDOW_W - FRUIT_SIZE) // 2
    y0 = (WINDOW_H - FRUIT_SIZE) // 2

    canvas[y0:y0+FRUIT_SIZE, x0:x0+FRUIT_SIZE] = img_vis

    colores = {
        "Verde": (0, 180, 0),
        "Maduro": (0, 200, 200),
        "Pasado": (0, 0, 200)
    }
    color = colores.get(estado, (0, 0, 0))

    cv2.rectangle(canvas, (x0-6, y0-6), (x0+FRUIT_SIZE+6, y0+FRUIT_SIZE+6), color, 4)

    label = f"{clase} - {estado}"
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)

    tx = (WINDOW_W - tw) // 2
    ty = y0 - 20

    cv2.rectangle(canvas, (tx-10, ty-th-10), (tx+tw+10, ty+5), color, -1)
    cv2.putText(canvas, label, (tx, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow("Sistema Hibrido CNN + Percepcion del Color", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename()
    if ruta:
        analizar_imagen(ruta)
