
import cv2
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("SUCCESS: LBPHFaceRecognizer found.")
except AttributeError:
    print("ERROR: module 'cv2.face' has no attribute 'LBPHFaceRecognizer_create'")
except Exception as e:
    print(f"ERROR: {e}")
