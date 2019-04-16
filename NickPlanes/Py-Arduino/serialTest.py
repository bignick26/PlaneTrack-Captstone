import serial
import time

port = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=3.0)

while True:
    yaw = input("Yaw: ")
    pitch = input("Pitch: ")
    cmd = "{},{}".format(yaw, pitch)
    port.write(cmd.encode('utf-8'))
    time.sleep(3)
