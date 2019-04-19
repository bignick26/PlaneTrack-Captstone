
#import serial
import subprocess

#ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
subprocess.check_output('dump1090')
#subprocess.run('/home/up/Documents/NickPlanes/dump1090-serial/dump1090 --serial-port /dev/ttyS0 -format 0')
#while true:
#	print(repr(ser.read(10))
