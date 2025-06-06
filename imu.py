
import simplepyble
import struct
from global_interface import *
import time

# Config BLE
bleServerName = "Movella DOT"

configServiceUUID = "15171000-4947-11e9-8646-d663bd873d93"
measurementServiceUUID = "15172000-4947-11e9-8646-d663bd873d93"

devicectrlCharacteristicUUID = "15171002-4947-11e9-8646-d663bd873d93"
measureCtrlCharacteristicUUID = "15172001-4947-11e9-8646-d663bd873d93"
medPayLoadCharacteristicUUID = "15172003-4947-11e9-8646-d663bd873d93"


# Convert binary data to float
def convertData(data, index):
    float_value = struct.unpack('<f', data[index:index+4])[0]
    return float_value


class IMUManager:
    def __init__(self, freq):
        self.peripheral = None
        self.packageCounter = 3*freq 
        self.count = 0

    def imu_init(self):
        adapters = simplepyble.Adapter.get_adapters()

        if len(adapters) == 0:
            print("No adapters found")

        adapter = adapters[0]

        print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

        adapter.set_callback_on_scan_start(lambda: print("Scan started."))
        adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
        adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

        # Scan for 5 seconds
        adapter.scan_for(5000)

        peripherals = adapter.scan_get_results()
        selectIndex = -1

        for index, peripheral in enumerate(peripherals):
            if peripheral.identifier() == bleServerName:
                selectIndex = index

        self.peripheral = peripherals[selectIndex]

        print(f"Connecting to: {self.peripheral.identifier()} [{self.peripheral.address()}]")
        self.peripheral.connect()

        print("Successfully connected")

        # Ensure the characteristic supports notifications before starting
        try:
            contents = self.peripheral.notify(measurementServiceUUID, medPayLoadCharacteristicUUID, lambda data: self.notifyProcess(data))
            print("Notifications started successfully.")
            text = self.peripheral.read(measurementServiceUUID, measureCtrlCharacteristicUUID)
            print(text)
            start_mess = b'\x01\x01\x16'
            self.peripheral.write_command(measurementServiceUUID, measureCtrlCharacteristicUUID, start_mess)
            initState = nextStateQueue.get()
            lastStateQueue.put(initState)
        except RuntimeError as e:
            print(f"Error starting notifications: {e}")

    # Notification handler
    def notifyProcess(self, data):
        ts = time.time()
        if self.count >= self.packageCounter:
            # notifyQueue.put(data)
            imu_queue.append((ts, data))
            # print(f"[BLE] imu_queue size: {imu_queue.qsize()}")
        else:
            self.count += 1

    def disconnect(self):
        if self.peripheral and self.peripheral.is_connected():
            self.peripheral.disconnect()
            print("Disconnected from device.")

