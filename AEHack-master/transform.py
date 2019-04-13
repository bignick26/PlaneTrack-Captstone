import math
import pyproj
R = 6378137  # meters
f_inv = 298.257224
f = 1.0 / f_inv
e2 = 1 - (1 - f) * (1 - f)

latRef = 33.774502
lngRef = -84.3970796
altRef = 283.0  # meters

def gps_to_ecef_pyproj(lat, lon, alt):
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    x, y, z = pyproj.transform(lla, ecef, lon, lat, alt, radians=False)
    return x, y, z

def gps_to_ecef(latitude, longitude, altitude):
    # (lat, lon) in WSG-84 degrees
    # h in meters
    cosLat = math.cos(latitude * math.pi / 180)
    sinLat = math.sin(latitude * math.pi / 180)
    cosLong = math.cos(longitude * math.pi / 180)
    sinLong = math.sin(longitude * math.pi / 180)

    c = 1 / math.sqrt(cosLat * cosLat + (1 - f) * (1 - f) * sinLat * sinLat)
    s = (1 - f) * (1 - f) * c

    x = (R*c + altitude) * cosLat * cosLong
    y = (R*c + altitude) * cosLat * sinLong
    z = (R*s + altitude) * sinLat

    return x, y, z

# ecef2enu

def ecef_to_enu(x, y, z, latRef, longRef, altRef):

    cosLatRef = math.cos(latRef * math.pi / 180)
    sinLatRef = math.sin(latRef * math.pi / 180)
    cosLongRef = math.cos(longRef * math.pi / 180)
    sinLongRef = math.sin(longRef * math.pi / 180)

    cRef = 1 / math.sqrt(cosLatRef * cosLatRef + (1 - f)
                         * (1 - f) * sinLatRef * sinLatRef)

    x0 = (R*cRef + altRef) * cosLatRef * cosLongRef
    y0 = (R*cRef + altRef) * cosLatRef * sinLongRef
    z0 = (R*cRef*(1-e2) + altRef) * sinLatRef

    xEast = (-(x-x0) * sinLongRef) + ((y-y0)*cosLongRef)

    yNorth = (-cosLongRef*sinLatRef*(x-x0)) - \
        (sinLatRef*sinLongRef*(y-y0)) + (cosLatRef*(z-z0))

    zUp = (cosLatRef*cosLongRef*(x-x0)) + \
        (cosLatRef*sinLongRef*(y-y0)) + (sinLatRef*(z-z0))

    return xEast, yNorth, zUp


def geodetic_to_enu(lat, lon, h, lat_ref, lon_ref, h_ref):
    x, y, z = gps_to_ecef(lat, lon, h)
    return ecef_to_enu(x, y, z, lat_ref, lon_ref, h_ref)

def convert_to_elv_az(latTar, lngTar, altTar):
    # latTar = 33.772018
    # lngTar = -84.252749
    # altTar = 3489.96 # meters

    # latTar = 33.732971
    # lngTar = -84.441703
    # altTar = 2270.76 # meters

    # video started at 19:03:44
    # frame 397 puts us at azimuth 170 at 19:03:57

    x, y, z = gps_to_ecef_pyproj(latRef, lngRef, altRef)
    xp, yp, zp = gps_to_ecef_pyproj(latTar, lngTar, altTar)

    dx = xp - x
    dy = yp - y
    dz = zp - z

    # https://gis.stackexchange.com/questions/58923/calculate-view-angle
    elevation = math.acos((x*dx + y*dy + z*dz) /
                          math.sqrt((x**2 + y**2 + z**2) * (dx**2 + dy**2 + dz**2)))
    # print(math.degrees(elevation))

    azimuth_cos = (-z*x*dx - z*y*dy + (x**2 + y**2) * dz) / \
        math.sqrt((x**2 + y**2) * (x**2 + y**2 + z**2)
                  * (dx**2 + dy**2 + dz**2))
    azimith_sin = (-y*dx + x*dy) / math.sqrt((x**2 + y**2)
                                             * (dx**2 + dy**2 + dz**2))
    azimuth = math.atan2(azimith_sin, azimuth_cos)
    # print(-math.degrees(azimuth))

    deg_elevation = math.degrees(elevation)
    deg_azimuth = math.degrees(azimuth)

    if deg_azimuth < 0:
        deg_azimuth += 360

    return (90.0-deg_elevation, deg_azimuth)

    # azimuth = math.acos((-z*x*dx - z*y*dy + (x^2+y^2)*dz) / math.sqrt((x^2+y^2)(x^2+y^2+z^2)(dx^2+dy^2+dz^2)))
    # xF,yF,zF = gps_to_ecef(pt[0], pt[1], pt[2])

    # print("pyproj (XYZ)\t = ", xPy, yPy, zPy)
    # # print("ECEF (XYZ)\t = ", xF, yF, zF)

    # xE, yN, zU = ecef_to_enu(xPy,yPy,zPy, latRef, lngRef, altRef)
    # print('ENU (XYZ) \t = ', xE, yN, zU)

    # print(math.asin(xE/zU))

    # print("-------------------------------------------------")
