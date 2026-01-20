
import cv2
import numpy as np

class CameraUtils:
    
    @staticmethod
    def detect_face(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Load cascade. Ensure opencv-data is installed or path is correct. 
        # Using cv2.data.haarcascades handles path issues usually.
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None, None
        (x, y, w, h) = faces[0]
        # Return only the face area and the rect
        return gray[y:y+h, x:x+w], (x, y, w, h)

    @staticmethod
    def image_to_bytes(image):
        if image is None:
            return None
        success, encoded_image = cv2.imencode('.jpg', image)
        if success:
            return encoded_image.tobytes()
        return None

    @staticmethod
    def bytes_to_image(image_bytes):
        if image_bytes is None:
            return None
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        return img
