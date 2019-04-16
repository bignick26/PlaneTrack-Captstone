import serial
import time

port = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,timeout=3.0)
cmd = "190,40"
time.sleep(3)
port.write(cmd.encode('utf-8'))
