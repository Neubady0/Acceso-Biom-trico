
import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import numpy as np
import sys
import os

# Ensure src is in path if running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.usuario_dao import UsuarioDAO
from src.utiils.camera_utils import CameraUtils

class BioPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioPass DAO")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="BioPass System", font=("Arial", 16))
        self.label.pack(pady=20)

        self.btn_register = tk.Button(root, text="Registrar Usuario", width=20, height=2, command=self.register)
        self.btn_register.pack(pady=10)

        self.btn_login = tk.Button(root, text="Entrar (Login)", width=20, height=2, command=self.login)
        self.btn_login.pack(pady=10)

    def register(self):
        nombre = simpledialog.askstring("Registro", "Introduce tu nombre:")
        if not nombre:
            return

        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Instrucciones", "Se abrirá la cámara.\n\n1. Mira a la cámara.\n2. Cuando se detecte tu cara (cuadro verde), pulsa 's' para guardar.\n3. Pulsa 'q' si quieres cancelar.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            face_img, face_rect = CameraUtils.detect_face(frame)
            
            # Draw rectangle
            if face_rect is not None:
                (x, y, w, h) = face_rect
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Pulsa 's' para capturar", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Registro", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                if face_img is not None:
                    # Convert to bytes
                    foto_bytes = CameraUtils.image_to_bytes(face_img)
                    if foto_bytes:
                        if UsuarioDAO.registrar_usuario(nombre, foto_bytes):
                            messagebox.showinfo("Éxito", f"Usuario {nombre} registrado correctamente.")
                            break
                        else:
                            messagebox.showerror("Error", "Error al registrar en base de datos.")
                            break
                    else:
                        print("Error converting image to bytes.")
                else:
                    print("No face detected.")
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def train_model(self):
        usuarios = UsuarioDAO.obtener_todos()
        if not usuarios:
            return None, None
        
        faces = []
        labels = []
        names = {} # Map ID (int) -> Name (str)
        
        label_map_id = 0
        # LBPH needs integer labels. We might need to map DB IDs to small ints if DB IDs are large or sparse, 
        # but usually DB IDs are fine if they are ints. 
        # However, LBPH expects sequential or at least integer labels.
        # DB ID is SERIAL, so it is int.
        
        for user in usuarios:
            img_bytes = user['foto']
            img = CameraUtils.bytes_to_image(img_bytes)
            user_id = user['id']
            user_name = user['nombre']
            
            if img is not None:
                faces.append(img)
                labels.append(user_id)
                names[user_id] = user_name
        
        if not faces:
             return None, None

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(labels))
        return recognizer, names

    def login(self):
        # Train on the fly
        try:
            recognizer, names = self.train_model()
        except Exception as e:
            messagebox.showerror("Error", f"Error entrenando modelo: {e}")
            return

        if recognizer is None:
            messagebox.showwarning("Aviso", "No hay usuarios registrados para identificar.")
            return

        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Instrucciones", "Mira a la cámara.\nEl sistema intentará reconocerte.\nPulsa 'q' para salir.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            face_img, face_rect = CameraUtils.detect_face(frame)
            
            if face_rect is not None:
                (x, y, w, h) = face_rect
                
                # Predict
                try:
                    label_id, confidence = recognizer.predict(face_img)
                    
                    # Confidence interpretation for LBPH:
                    # 0 -> Exact match
                    # < 50 -> Good match
                    # < 100 -> Possible match
                    # > 100 -> No match usually
                    
                    # LBPH usage: 0 is perfect match. ~100 is no match.
                    # User request: "Coincidencia de mas del 70 por ciento".
                    # We map this as: Match_Percent = 100 - confidence
                    # We want Match_Percent > 70  =>  100 - confidence > 70  =>  confidence < 30
                    
                    match_percent = max(0, 100 - round(confidence))
                    
                    if match_percent > 69:
                        nombre = names.get(label_id, "Desconocido")
                        # Show the match on screen before stopping
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, f"Hola {nombre} ({match_percent}%)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        cv2.imshow("Login", frame)
                        cv2.waitKey(10) # Small delay to show the rectangle
                        
                        messagebox.showinfo("Bienvenido", f"Hola {nombre}")
                        break # Stop camera and "enter"
                    else:
                        display_text = f"Desconocido ({match_percent}%)"
                        color = (0, 0, 255)
                    
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        cv2.putText(frame, display_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                except Exception as e:
                    print(f"Prediction error: {e}")

            cv2.imshow("Login", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()
