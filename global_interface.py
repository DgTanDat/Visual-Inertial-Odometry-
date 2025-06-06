from queue import Queue
from collections import deque


SYS_CNT = 0
STOP = 1
GOSTRAIGHT = 0
TURNLEFT = 2
TURNRIGHT = 3
NONE = -1
IS_RUNNING = True
IMU_FREQ = 60
delta_t = 1/IMU_FREQ 
# packageCounter = 3*IMU_FREQ 
# count = 0

notifyQueue = Queue(maxsize = 30)
stateQueue = Queue(maxsize = 30)
lastStateQueue = Queue(maxsize = 30)
nextStateQueue = Queue(maxsize = 180)

image_queue = deque(maxlen=60)
imu_queue = deque(maxlen=180)
synced_data = Queue(maxsize=200)