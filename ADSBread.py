import subprocess
import serial
import time
import math

arduino = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,timeout=3.0)
gpsHome = [33.775949,-84.397141]
gpsPlane = []
low = 300000

numF = 0 #number of flights
flts = [] # [[hex,timeRx,timeTx,fltnum,alt,speed,heading,lat,long],[]]
hexVal = []
hexInd = 0
tri = 1; tti = 2; fi =3; ai = 4; si = 5; hi = 6; lati = 7; longi = 8; #indexes


command = ['./dump1090', '--net', '--quiet']
subprocess.Popen(command)

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
    
    if split[1] == 1: #check if we get fltNum
      flts[hexInd][fi] = split[10]
    elif split[1] == 3: #check if we get atl,lat,long
      flts[hexInd][ai] = split[11]
      flts[hexInd][lati] = split[14]
      flts[hexInd][longi] = split[15]
    elif split[1] == 4: #check if we get speed, heading
      flts[hexInd][si] = split[12]
      flts[hexInd][hi] = split[13]
    
  except ValueError:
    hexInd = len(hexVal)
    hexVal.append(split[4])
    
    #add everything b/c of append calls suck
    flts.append([split[4],split[7],split[9],split[10],split[11],
    split[12],split[13],split[14],split[15]])
    
  print(flts)
  
  alt = flts[i][ai]
  try:
    if int(alt) < low:
      low = int(alt)
      lowInd = hexInd
  except ValueError:
    print('not an int?')
    
  ##Some Bullshit for GPS
  if low < 300000:
    try:
      gpsPlane = [int(flts[lowInd][lati]),int(flts[lowInd][longi]),int(flts[lowInd][ai])]
      if gpsPlane[1] > 0:
        d = math.sqrt(((gpsHome[0]-gpsPlane[0])*120.628409*(gpsHome[0]-gpsPlane[0])**120.628409)
        + ((gpsHome[1]-gpsPlane[1])*58.5553*(gpsHome[1]-gpsPlane[1])*58.5553)) # bad
        d = d*5280
        
        alpha = 20
      math.degrees(math.atan(1.18))
      cmd = "190,40" #"{},{}\n".format(cmd_elv, cmd_az)
      arduino.write(cmd.encode('utf-8'))
    except ValueError:
      print('not an int?')
    
  
  

#filt = ['egrep','--line','-buffered','MSG,1,|MSG,3,|MSG,4,']
#p3 = subprocess.Popen(filt, stdout=subprocess.PIPE)
#egrep --line-buffered 'MSG,3,|MSG,4,'

##close? 
##lsof -i :30002
##kill PID number
