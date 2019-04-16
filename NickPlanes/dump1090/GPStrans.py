import math

lath = 33.250
lonh = -84.401
alth = 820
gpsHome = [lath,lonh,alth]

lat = 33.250
lon = -84.3
alt = 30000
gpsPlane = [lat, lon, alt]

#pitch
dlat = (lat - lath)
dlon = (lon - lonh)
dist = math.sqrt(((dlat*363815.46)*(dlat*363815.46)) + ((dlon*309172.01)*(dlon*309172.01)))

dalt = (alt - alth)

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


print(dist)
print(pitch)
print(yaw)


