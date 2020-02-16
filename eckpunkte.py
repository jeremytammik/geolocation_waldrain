#!/usr/bin/env python3
# eckpunkte.py - define waldrain corner points and measure edge lengths
# Copyright (C) 2020 by Jeremy Tammik, Autodesk Inc.

import math, numpy

def lat_lon_dist_1(lat1, lon1, lat2, lon2):
  """Return distance between to latitude longtitude points.
  
  Generally used geo measurement function from:
  
  [How to convert latitude or longitude to meters?](https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters)
  [Calculate distance, bearing and more between Latitude/Longitude points](http://www.movable-type.co.uk/scripts/latlong.html)
  
  Apply the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).
  
  The simplest way to do it, assuming that the Earth is a sphere with a circumference of 40075 km.
  
  Length in meters of 1 degree of latitude = always 111.32 km
  
  Length in meters of 1 degree of longitude = 40075 km * cos( latitude ) / 360
  
  c is the angular distance in radians, and a is the square of half the chord length between the points.
  """
  deg2rad = math.pi / 180
  R = 6378.137 # Radius of earth in KM
  phi1 = lat1 * deg2rad
  phi2 = lat2 * deg2rad
  dphi = (lat2 - lat1) * deg2rad
  dlam = (lon2 - lon1) * deg2rad
  a = math.sin(dphi/2) * math.sin(dphi/2) \
    + math.cos(phi1) * math.cos(phi2) \
      * math.sin(dlam/2) * math.sin(dlam/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c
  return d * 1000 # meters

def lat_lon_dist_2(lat1, lon1, lat2, lon2):
  """Return distance between to latitude longtitude points.
  
  Answer numer 2 for the same StackOverflow question:  
  [How to convert latitude or longitude to meters?](https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters)
  [Geographic coordinate system](https://en.wikipedia.org/wiki/Geographic_coordinate_system)
  
  The wikipedia entry states that the distance calcs are within 0.6m for 100km longitudinally and 1cm for 100km latitudinally.
  """
  deg2rad = math.pi / 180
  
  phi = (lat1+lat2) * deg2rad / 2.0 # or just use lat1 for slightly less accurate estimate

  m_per_deg_lat = 111132.954 - 559.822 * math.cos( 2.0 * phi ) + 1.175 * math.cos( 4.0 * phi)
  m_per_deg_lon = deg2rad * 6367449 * math.cos ( phi );

  dlat = abs(lat2 - lat1) 
  dlon = abs(lon2 - lon1) 

  dist_m = math.sqrt( pow( dlat * m_per_deg_lat,2) + pow( dlon * m_per_deg_lon, 2) )
  
  return dist_m

def lat_lon_dist_3(lat1, lon1, lat2, lon2):
  """Return distance between to latitude longtitude points from
  [understanding terms in Length of Degree formula](https://gis.stackexchange.com/questions/75528/understanding-terms-in-length-of-degree-formula/75535#75535)
  """
  deg2rad = math.pi / 180
  
  lat = (lat1+lat2) * deg2rad / 2.0 # or just use lat1 for slightly less accurate estimate

  m1 = 111132.92
  m2 = -559.82
  m3 = 1.175
  m4 = -0.0023
  p1 = 111412.84
  p2 = -93.5
  p3 = 0.118

  # Calculate the length of a degree of latitude and longitude in meters
  
  latlen = m1 \
    + (m2 * math.cos(2 * lat)) \
    + (m3 * math.cos(4 * lat)) \
    + (m4 * math.cos(6 * lat))
  longlen = (p1 * math.cos(lat)) \
    + (p2 * math.cos(3 * lat)) \
    + (p3 * math.cos(5 * lat))

  dlat = abs(lat2 - lat1) 
  dlon = abs(lon2 - lon1) 

  dist_m = math.sqrt( pow( dlat * latlen, 2) + pow( dlon * longlen, 2) )
  
  return dist_m

pts = [
  [47.61240287934088,7.668455564143808],
  [47.61238603493116,7.66886803694362],
  [47.61227235282722,7.668805013356426],
  [47.612081232450755,7.668710772100395],
  [47.61209766306042,7.668317607008359],
  [47.612263038360155,7.668392271613928]]

tags = ['NW','NO','OM','SO','SW','WM']

edge_length = [ # in metres
  31.10, # Nord
  13.34, 22.51, # Ost
  29.63, # Sued
  19.26, 16.24 ] # West

area = 1043 # square metres

n = len(pts)

print( n, 'points:')

for i in range(n):
  print(' ', tags[i],pts[i])

xs = [p[0] for p in pts]
ys = [p[1] for p in pts]

centre_point = [numpy.mean(xs), numpy.mean(ys)]

print('centre point:\n ', centre_point)

#print('offsets from centre point:\n ', centre_point)

#edge_lengths = [lat_lon_dist(pts[i-1][0], pts[i-1][1], pts[i][0], pts[i][1]) for i in range(n)]

#print('edge lengths:\n ', edge_lengths)

print('edge lengths:')

def sreal(x):
  "Format real numer to two decimanl places."
  return '{0:.2f}'.format( x )

def calculate_and_compare(f,i,j,e):
  "Return string result for calculating and comparing with expected result"
  d = f( pts[i][0], pts[i][1], pts[j][0], pts[j][1])
  return sreal(d) + ' (' + sreal(abs(d-e)) + ')'

for i in range(n):
  j = i + 1
  if j >= n: j -= n
  e = edge_length[i]
  print(tags[i], '-', tags[j] + ':', sreal(e),
    calculate_and_compare( lat_lon_dist_1, i, j, e ),
    calculate_and_compare( lat_lon_dist_2, i, j, e ),
    calculate_and_compare( lat_lon_dist_3, i, j, e ))

