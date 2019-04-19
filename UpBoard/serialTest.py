import serial
import time
from datetime import datetime, timedelta

port = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,timeout=3.0)
pitch = 0
yaw = 180

period = timedelta(milliseconds = 50)
next_time = datetime.now() + period
  
try:
  while 1:
    #time.sleep(.25)
    cmd = "{},{}n".format(yaw, pitch)
    
    if next_time <= datetime.now():
      pitch+=1
      next_time += period
      port.write(cmd.encode('utf-8'))
      print(cmd)
    
except KeyboardInterrupt:
  cmd = "sleep"
  port.write(cmd.encode('utf-8'))
  print("Bye Bye")
