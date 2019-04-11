#!/usr/bin/python3

import sys
from enum import Enum
from datetime import datetime, timedelta
from transform import convert_to_elv_az
import serial
import time
import math

PI = 1

ser = None
if PI:
  ser = serial.Serial('/dev/serial0', 115200)

start = datetime.now()

current_str = ""

filter_icao = None
if len(sys.argv) != 2:
  print("Please call with {} <icao>".format(sys.argv[0]))
  exit(2)
else:
  filter_icao = sys.argv[1].lower().rstrip().strip()
  print("Python searching for {}".format(filter_icao))

class ADSBDecodeState(Enum):
  CRC = 0
  RSSI = 1
  TIME = 2
  MESSAGE_TYPE = 3
  CAPABILITY = 4
  ICAO_ADDR = 5
  ALTITUDE = 6
  LATITUDE = 7
  LONGITUDE = 8

TOP = 9
BOTTOM = 10

def constrain(val, min_val, max_val):
  return min(max_val, max(min_val, val))

class ADSBMessage():
  def __init__(self, icao_filter, start):

    self.icao_filter = icao_filter
    self.base_time = start
    self.current_state = ADSBDecodeState.CRC
    
    self.crc = ""
    self.rssi = ""
    self.time = ""
    self.message_type = ""
    self.icao_addr = ""
    self.altitude = 0 # feet
    self.latitude = 0.0 # decimal
    self.longitude = 0.0 # decimal

    self.elv_az = (0.0, 0.0)

  # returns -1 if current packet should be tossed
  # returns 0 if current packet is indeterminant
  # returns 1 if packet is correct alt/lat/long baro altitude format
  def parse_line(self, raw):

    #print(filter_icao)
    
    line = raw.lower().rstrip()

    # print(self.current_state)

    if self.current_state == ADSBDecodeState.CRC and "crc" in line:
      self.crc = line
      self.current_state = ADSBDecodeState.RSSI

    elif self.current_state == ADSBDecodeState.RSSI and "rssi" in line:
      self.rssi = line
      self.current_state = ADSBDecodeState.TIME

    elif self.current_state == ADSBDecodeState.TIME and "time" in line:
      raw_time = line.split(':')[1].strip()
      isolated_time = float(raw_time.split('us')[0])
      self.time = self.base_time + timedelta(microseconds=isolated_time)
      self.current_state = ADSBDecodeState.MESSAGE_TYPE

    elif self.current_state == ADSBDecodeState.MESSAGE_TYPE:
      if "df 17:" in line:
        self.message_type = line
        self.current_state = ADSBDecodeState.ICAO_ADDR
      else:
        return -1

    elif self.current_state == ADSBDecodeState.ICAO_ADDR and "icao address" in line:
      # print(line)
      if self.icao_filter in line:
        # print("matched icao")
        self.icao_addr = line.split(':')[1].strip()
        self.current_state = ADSBDecodeState.ALTITUDE
      else:
        return -1

    elif self.current_state == ADSBDecodeState.ALTITUDE and "feet" in line:
      # print(line)
      # self.altitude = line
      raw_altitude = line.split(':')[1].strip()
      isolated_altitude = int(raw_altitude.split(' ')[0].strip())
      self.altitude = isolated_altitude
      self.current_state = ADSBDecodeState.LATITUDE

    elif self.current_state == ADSBDecodeState.LATITUDE and "latitude" in line:
      # print(line)
      raw_latitude = line.split(':')[1].strip()
      isolated_latitude = float(raw_latitude.split(' ')[0].strip())
      self.latitude = isolated_latitude
      self.current_state = ADSBDecodeState.LONGITUDE

    elif self.current_state == ADSBDecodeState.LONGITUDE and "longitude" in line:
      raw_longitude = line.split(':')[1].strip()
      isolated_longitude = float(raw_longitude.split(' ')[0].strip())
      self.longitude = isolated_longitude
      # print(line)

      self.elv_az = convert_to_elv_az(self.latitude, self.longitude, self.altitude)
      
      if math.isnan(self.elv_az[0]) or math.isnan(self.elv_az[1]):
        return -1

      return 1

    elif not line:
      return -1

  def __str__(self):
    return "ICAO:\t'{}'\nTIME:\t{}\nALT:\t{}\nLAT:\t{}\nLONG:\t{}\nELV:\t{}\nAZ: \t{}".format(
      self.icao_addr,
      self.time,
      self.altitude,
      self.latitude,
      self.longitude,
      self.elv_az[0],
      self.elv_az[1])

msg = ADSBMessage(filter_icao, start)
throw_away = False



for line in sys.stdin:
  # print(line)

  if throw_away:
    if not line.lower().rstrip():
      throw_away = False

  current_str += line

  rtn = msg.parse_line(line.lower().rstrip())

  if rtn == 1:

    cmd_elv = int(msg.elv_az[0])

    if PI:
      ser.write(cmd_elv)

    # translate command from 0-360 to 90-180
    cmd_az = int(msg.elv_az[1]) - 90
    cmd_az = constrain(cmd_az, 0, 180)

    cmd_str = "{},{}\n".format(cmd_elv, cmd_az)
    if PI:
      ser.write(cmd_str.encode('utf-8'))
      time.sleep(1)

    print("message received, commanding mount elv: {}, az: {}".format(cmd_elv, cmd_az))
    print(msg)
    print("")

  elif rtn == -1:
    msg = ADSBMessage(filter_icao, start)

  else:
    throw_away = True   
