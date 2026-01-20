
print("Start")
try:
    import os
    print("Imported os")
    import sys
    print("Imported sys")
    import tkinter
    print("Imported tkinter")
    import numpy
    print(f"Imported numpy {numpy.__version__}")
    import cv2
    print(f"Imported cv2 {cv2.__version__}")
    import psycopg2
    print("Imported psycopg2")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
print("End")
