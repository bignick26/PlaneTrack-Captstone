import serial
import time

ser = serial.Serial("/dev/ttyUSB1", 9600, timeout = 1)

readout = 0

print("Serial Communicator Running...")
connected = False
commandToSend = "abc"

while True:
    print("Writing: ", commandToSend)
    ser.write(str(commandToSend).encode())
    time.sleep(1)
    while True:
        try:
            print("Attempt to read")
            readOut = ser.readline().decode("ascii")
            time.sleep(1)
            print("Reading: ", readOut)
            break
        except:
            pass
    print("Restart")
    ser.flush()
