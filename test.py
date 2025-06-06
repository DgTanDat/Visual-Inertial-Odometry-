from camera import *
import cv2

cam = RPiCamera(640, 480, 970, 961, 320, 240)
cam.PiCamera_Init()
while True:
    cam.capture_img()