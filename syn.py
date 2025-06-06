import threading
import time
import cv2
import numpy as np
from camera import *
from imu import *
import struct
from global_interface import *


# ==== Thread: Đọc BLE IMU ====
def ble_thread():
    imu = IMUManager()
    imu.imu_init()

    while True:
        time.sleep(1)  # giữ kết nối BLE sống


def get_closest_imu(ts_frame):
    closest = None
    min_diff = float("inf")
    for ts_imu, imu_data in imu_queue:
        diff = abs(ts_imu - ts_frame)
        if diff < min_diff:
            min_diff = diff
            closest = (ts_imu, imu_data)
    return closest


# ==== Hàm chính ====
if __name__ == "__main__":
   
    t2 = threading.Thread(target=ble_thread, daemon=True)
    
    t2.start()

    cam = RPiCamera(640, 480, 970, 961, 320, 240)
    cam.PiCamera_Init()
    cam.start_camera()
    # while True:
    #     timestamp, frame  = cam.capture_img()
    #     imu_data = get_closest_imu(timestamp)
    #     if imu_data:
    #         ts_imu, data = imu_data
    #         curYaw      = convertData(data, 12)
    #         # Giả sử `data` là dict hoặc tuple, ví dụ: (ax, ay, az, gx, gy, gz)
    #         imu_text = f"IMU : {ts_imu:.3f}: {curYaw}"
    #     else:
    #         imu_text = "IMU: no data"

    #     # Vẽ chuỗi IMU lên frame
    #     cv2.putText(frame, imu_text, (10, 30),
    #                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                 fontScale=0.6, color=(0, 255, 0), thickness=2)

    #     # Hiển thị frame
    #     cv2.imshow("Camera + IMU", frame)

    #     # Thoát khi nhấn 'q'
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    #     # Delay để giữ ~60 FPS
    #     time.sleep(1 / 60.0)
    # prev_time = 0
    # while True:
    #     timestamp, frame = cam.capture_img()
    #     imu_data = get_closest_imu(timestamp)
    #     if imu_data:
    #         ts_imu, data = imu_data
    #         curYaw = convertData(data, 12)
    #         imu_text = f"IMU : {ts_imu:.3f}: {curYaw}"
    #     else:
    #         imu_text = "IMU: no data"

    #     # --- Tính FPS ---
    #     now = time.time()
    #     fps = 1.0 / (now - prev_time)
    #     prev_time = now
    #     fps_text = f"FPS: {fps:.2f}"

    #     # --- Vẽ IMU và FPS lên frame ---
    #     cv2.putText(frame, imu_text, (10, 30),
    #                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                 fontScale=0.6, color=(0, 255, 0), thickness=2)
    #     cv2.putText(frame, fps_text, (10, 60),
    #                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                 fontScale=0.6, color=(0, 255, 255), thickness=2)

    #     # Hiển thị frame
    #     cv2.imshow("Camera + IMU", frame)

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    #     # Không cần sleep nếu bạn tính FPS thực
    #     # time.sleep(1 / 60.0)


    # cam.stop_camera()
    # cv2.destroyAllWindows()
    prev_time = time.time()
    log_file = open("sync_log.txt", "w")

    while True:
        timestamp, frame = cam.capture_img()

        imu_data = get_closest_imu(timestamp)
        if imu_data:
            ts_imu, data = imu_data
            curYaw = convertData(data, 12)
            imu_text = f"IMU : {ts_imu:.3f}: {curYaw}"

            # Ghi vào file log
            log_file.write(f"{timestamp:.6f} {ts_imu:.6f} {curYaw:.3f}\n")
        else:
            imu_text = "IMU: no data"

        # Tính FPS
        now = time.time()
        fps = 1.0 / (now - prev_time)
        prev_time = now
        fps_text = f"FPS: {fps:.2f}"

        # Hiển thị overlay
        cv2.putText(frame, imu_text, (10, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.6, color=(0, 255, 0), thickness=2)

        cv2.putText(frame, fps_text, (10, 60),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.6, color=(0, 255, 255), thickness=2)

        cv2.imshow("Camera + IMU", frame)

        # Thoát bằng phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.stop_camera()
    log_file.close()
    cv2.destroyAllWindows()
        
 

