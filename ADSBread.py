import subprocess
import serial
import time
import math
from datetime import datetime, timedelta

#Fletchers House
latH = 33.250
longH = -84.401
altH = 820
gpsH = [latH,longH,altH]

fletchHex = 0 #indecx of plane to track

#arduino = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,timeout=3.0)
gpsP = []

numF = 0 #number of flights
flts = [] # [[hex,timeRx,timeTx,fltnum,alt,speed,heading,lat,long],[]]
hexVal = []
hexInd = 0
tri = 1; tti = 2; fi =3; ai = 4; si = 5; hi = 6; lati = 7; longi = 8; #indexes

#Delay for Motor Driving!
period = timedelta(milliseconds = 50)
next_time = datetime.now() + period

#Program:
command = ['./dump1090', '--net', '--quiet'] #writing to port 30003
subP = subprocess.Popen(command)

time.sleep(3)
reader = ['nc','127.0.0.1','30003'] # |egrep','--line','-buffered','MSG,1,|MSG,3,|MSG,4,']
p = subprocess.Popen(reader, stdout=subprocess.PIPE)
time.sleep(3)

#loop through and filter the output of dump1090 ported to 30003 and imported as subprocess p
while 1:

  line = p.stdout.readline().decode('utf-8')
  split = line.split(',') #make a list of each value (comma sperated)
  
  try: #search if hex value has been found before
    hexInd = hexVal.index(split[4])
    flts[hexInd][0] = hexVal[hexInd] #set the hex value based on hex index
    flts[hexInd][tri] = split[7]
    flts[hexInd][tti] = split[9]
    
    if split[1] == '1': #check if we get fltNum
      flts[hexInd][fi] = split[10]
    elif split[1] == '3': #check if we get atl,lat,long
      flts[hexInd][ai] = split[11]
      flts[hexInd][lati] = split[14]
      flts[hexInd][longi] = split[15]
    elif split[1] == '4': #check if we get speed, heading
      flts[hexInd][si] = split[12]
      flts[hexInd][hi] = split[13]
    
  except ValueError:
    hexInd = len(hexVal)
    hexVal.append(split[4])
    
    #add everything b/c of append calls suck
    flts.append([split[4],split[7],split[9],split[10],split[11],
    split[12],split[13],split[14],split[15]])
    
#  print(flts)
  if (flts[hexInd][0] == 'A7E276'):
    fletchHex = hexInd
  
#  print(flts[fletchHex])
  #hex = A667F2
  
  #GPS Calc
  try:
    latP = float(flts[fletchHex][lati])
    longP = float(flts[fletchHex][longi])
    altP = float(flts[fletchHex][ai]) 
    gpsP = [latP,longP,altP]
    dlat = (gpsP[0] - gpsH[0])
    dlon = (gpsP[1] - gpsH[1])
    dist = math.sqrt(((dlat*363815.46)*(dlat*363815.46)) + ((dlon*309172.01)*(dlon*309172.01)))
  
    dalt = (gpsP[2] - gpsH[2])
  
    pitch = round(math.degrees(math.atan(dalt/dist)))
    
    #assuming flat earth
    if (dlon>0): #if east 
      yaw = 180 - math.degrees(math.atan(dlat/dlon))
    elif ((dlon<0) & (dlat > 0)): #if west & north
      yaw = math.degrees(math.atan(dlat/dlon)) 
    elif ((dlon<0) & (dlat < 0)): 
      yaw = 360 - math.degrees(math.atan(dlat/dlon))
    elif ((dlon==0) & (dlat > 0)):
      yaw = 90
    elif ((dlon==0) & (dlat < 0)):
      yaw = 270
    
    yaw = round(yaw) 
    print('latP,longH,altH: ',latH,longH,altH)
    print('latP,longP,altP: ',latP,longP,altP)
    
    if next_time <= datetime.now():
      cmd = "{},{}n".format(yaw, pitch)
      arduino.write(cmd.encode('utf-8'))
      next_time += period
      print(pitch)
      print(yaw)
    
  except KeyboardInterrupt:
    try:
      subP.terminate()
      p.terminate() #check this line!!
    except OSError as e:
      print("here")
      print(str(e))
    subP.wait()
  except Exception as e:
    print(str(e))
  
#pitch



#  try:
#    if int(alt) < low:
#      low = int(alt)
#      lowInd = hexInd
#  except ValueError:
#    print('not an int?')
#    
#  ##Some Bullshit for GPS
#  if low < 300000:
#    try:
#      gpsPlane = [int(flts[lowInd][lati]),int(flts[lowInd][longi]),int(flts[lowInd][ai])]
#      if gpsPlane[1] > 0:
#        d = math.sqrt(((gpsHome[0]-gpsPlane[0])*120.628409*(gpsHome[0]-gpsPlane[0])**120.628409)
#        + ((gpsHome[1]-gpsPlane[1])*58.5553*(gpsHome[1]-gpsPlane[1])*58.5553)) # bad
#        d = d*5280
        
#        alpha = 20
#      math.degrees(math.atan(1.18))
#      cmd = "190,40" #"{},{}\n".format(cmd_elv, cmd_az)
#      arduino.write(cmd.encode('utf-8'))
#    except ValueError:
#      print('not an int?')
   

#filt = ['egrep','--line','-buffered','MSG,1,|MSG,3,|MSG,4,']
#p3 = subprocess.Popen(filt, stdout=subprocess.PIPE)
#egrep --line-buffered 'MSG,3,|MSG,4,'

##close? 
##lsof -i :30002
##kill PID number
