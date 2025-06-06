# from picamera2 import Picamera2
# import cv2
# import numpy as np
# import os
# import time

# # Output directory and image counter
# output_dir = "calib_images"
# os.makedirs(output_dir, exist_ok=True)
# img_counter = 47

# # Initialize camera
# picam = Picamera2()
# config = picam.create_video_configuration(
#     main={"size": (640, 480), "format": "RGB888"},
#     controls={"FrameRate": 60}
# )
# picam.configure(config)
# picam.start()

# print("Press 'c' to capture calibration image, 'q' to quit.")

# try:
#     while True:
#         frame = picam.capture_array()

#         # Show camera feed
#         cv2.imshow("Pi Camera V3 - Calibration Mode", frame)

#         key = cv2.waitKey(1) & 0xFF

#         if key == ord('c'):
#             # Save image
#             img_counter += 1
#             filename = os.path.join(output_dir, f"calib_{img_counter:02d}.jpg")
#             cv2.imwrite(filename, frame)
#             print(f"Saved image: {filename}")

#         elif key == ord('q'):
#             break

# except KeyboardInterrupt:
#     print("Interrupted")

# # Cleanup
# picam.stop()
# cv2.destroyAllWindows()

from picamera2 import Picamera2
import cv2
import numpy as np
import os
import time

# Output directory and image counter
output_dir = "calib_images"
os.makedirs(output_dir, exist_ok=True)
img_counter = 47

# Initialize camera
picam = Picamera2()
# configs = picam.sensor_modes

# for mode in configs:
#     print(mode)

config = picam.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    queue=False,
    controls={"FrameRate": 60}
)
picam.configure(config)
picam.set_controls({"AfSpeed": 1})  # 1 = Fast autofocus
picam.start()


print("Press 'c' to capture calibration image, 'q' to quit.")

# Variables for FPS calculation
prev_time = time.time()
fps = 0

try:
    while True:
        start_exe = time.perf_counter()
        frame = picam.capture_array()
        end_exe = time.perf_counter()
        print("exe time: ", end_exe - start_exe)

        # Calculate FPS
        current_time = time.time()
        fps = 1.0 / (current_time - prev_time)
        prev_time = current_time

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show camera feed
        cv2.imshow("Pi Camera V3 - Calibration Mode", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # Save image
            img_counter += 1
            filename = os.path.join(output_dir, f"calib_{img_counter:02d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved image: {filename}")

        elif key == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted")

# Cleanup
picam.stop()
cv2.destroyAllWindows()
