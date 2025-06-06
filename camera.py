import numpy as np
from picamera2 import Picamera2
from global_interface import *
import time

# Initialize camera
class RPiCamera:
    def __init__(self, width, height, fx, fy, cx, cy, 
				k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0):
        self.picam = None
        self.width = width
        self.height = height
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.distortion = (abs(k1) > 0.0000001)
        self.d = [k1, k2, p1, p2, k3]
        
    def PiCamera_Init(self):
        self.picam = Picamera2()
        config = self.picam.create_video_configuration(
            main={"size": (self.width, self.height), "format": "RGB888"},
            controls={"FrameRate": 60}
        )
        self.picam.configure(config)
        self.picam.set_controls({
            "AfMode": 2,           # Lấy nét tự động liên tục
            "AfSpeed": 1,          # Tốc độ lấy nét nhanh
            "ExposureTime": 4000,  # Tốc độ màn trập 8ms
            "Sharpness": 2.0,      # Tăng độ sắc nét
            "Brightness": 0.2,     # Tăng độ sáng
            "Contrast": 1.5,       # Tăng độ tương phản
        })

        time.sleep(1)

    def start_camera(self):
        self.picam.start()

    def stop_camera(self):
        self.picam.stop()

    def picamera_start_record(self, filepath):
        self.picam.start_and_record_video(filepath)

    def picamera_stop_record(self):
        self.picam.stop_recording()

    def capture_img(self):
        frame = self.picam.capture_array()
        ts = time.time()  
        # image_queue.put((ts, frame))
        return ts, frame






