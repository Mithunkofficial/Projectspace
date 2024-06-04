import cv2
import threading

from deepface import DeepFace

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 490)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 650)

counter = 0
face_match = False

ref = cv2.imread('test1.jpg')