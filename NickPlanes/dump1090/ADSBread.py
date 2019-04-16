import subprocess
import serial
import time
import math

latH = 33.250
longH = -84.401
altH = 820

count = 0
gpsH = [latH,longH,altH]

#lat = 33.250
#lon = -84.3
#alt = 30000
#gpsPlane = [lat, lon, alt]

fletchHex = 0

arduino = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,timeout=3.0)
gpsP = []

numF = 0 #number of flights
flts = [] # [[hex,timeRx,timeTx,fltnum,alt,speed,heading,lat,long],[]]
hexVal = []
hexInd = 0
tri = 1; tti = 2; fi =3; ai = 4; si = 5; hi = 6; lati = 7; longi = 8; #indexes

time.sleep(3)

command = ['./dump1090', '--net', '--quiet']
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
    
#  print(flts)ls
  if (flts[hexInd][0] == 'A667F2'):
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
    print(yaw)
    print(pitch)
    
    if count > 100:
      cmd = "{},{}".format(yaw,pitch).encode('utf-8')
    # count = 0
      arduino.write(cmd)
    else:
      count += 1
    
  except KeyboardInterrupt:
    try:
      subP.terminate()
    except OSError as e:
      print("here")
      print(str(e))
    subP.wait()
  except Exception as e:
    print(str(e))
    
    
