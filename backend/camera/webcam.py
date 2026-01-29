import cv2

camera = cv2.VideoCapture(1)

def get_frame():
    success, frame = camera.read()
    if not success:
        return None
    return frame


def capture_image(path="temp/capture.jpg"):
    ret, frame = camera.read()
    if not ret:
        return None

    cv2.imwrite(path, frame)
    return path
