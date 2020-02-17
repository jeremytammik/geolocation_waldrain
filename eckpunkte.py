#!/usr/bin/env python3
# eckpunkte.py - define waldrain corner points and measure edge lengths
# Copyright (C) 2020 by Jeremy Tammik, Autodesk Inc.

import math, numpy as np

# Input data

pts = [
  [47.61240287934088,7.668455564143808],
  [47.61238603493116,7.66886803694362],
  [47.612273612015436,7.668805013356426],
  [47.612081232450755,7.668710772100395],
  [47.61209766306042,7.668317607008359],
  [47.612263038360155,7.668392271613928]]

pts = [
  [47.61240288,7.66845556],
  [47.61238603,7.66886804],
  [47.61227361,7.66880501],
  [47.61208123,7.66871077],
  [47.61209766,7.66831761],
  [47.61226304,7.66839227]]

tags = ['NW','NO','OM','SO','SW','WM']

edge_length = [ # in metres
  31.10, # Nord
  13.34, 22.51, # Ost
  29.63, # Sued
  19.26, 16.24 ] # West

area = 1043 # square metres

deg2rad = math.pi / 180

# Three distance calculation functions

def lat_lon_dist_1(lat1, lon1, lat2, lon2):
  """Return distance between two latitude longtitude points.
  
  Generally used geo measurement function from:
  
  [How to convert latitude or longitude to meters?](https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters)
  [Calculate distance, bearing and more between Latitude/Longitude points](http://www.movable-type.co.uk/scripts/latlong.html)
  
  Apply the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).
  
  The simplest way to do it, assuming that the Earth is a sphere with a circumference of 40075 km.
  
  Length in meters of 1 degree of latitude = always 111.32 km
  
  Length in meters of 1 degree of longitude = 40075 km * cos( latitude ) / 360
  
  c is the angular distance in radians, and a is the square of half the chord length between the points.
  """
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
  """Return distance between two latitude longtitude points.
  
  Answer numer 2 for the same StackOverflow question:  
  [How to convert latitude or longitude to meters?](https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters)
  [Geographic coordinate system](https://en.wikipedia.org/wiki/Geographic_coordinate_system)
  
  The wikipedia entry states that the distance calcs are within 0.6m for 100km longitudinally and 1cm for 100km latitudinally.
  """
  phi = (lat1+lat2) * deg2rad / 2.0 # or just use lat1 for slightly less accurate estimate

  m_per_deg_lat = 111132.954 - 559.822 * math.cos( 2.0 * phi ) + 1.175 * math.cos( 4.0 * phi)
  m_per_deg_lon = deg2rad * 6367449 * math.cos ( phi );

  dlat = abs(lat2 - lat1) 
  dlon = abs(lon2 - lon1) 

  dist_m = math.sqrt( pow( dlat * m_per_deg_lat,2) + pow( dlon * m_per_deg_lon, 2) )
  
  return dist_m

def get_lat_len_to_metre_factors_at(lat):
  """Return the factors required to convert the length
  of a degree of latitude and longitude at the given
  latitude `lat` to meters from
  [understanding terms in length of degree formula](https://gis.stackexchange.com/questions/75528/understanding-terms-in-length-of-degree-formula/75535#75535)
  """
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

  # calculate correction for 14 cm error
  #print (latlen)
  #print ('deg lat per metre', 1/latlen)
  #print ('deg lat per cm', 0.01/latlen)
  #print ('deg lat for 12 cm', 0.12/latlen)
  #print (47.61227235282722 + 0.14/latlen)
  #exit(1)

  return (latlen,longlen)

def lat_lon_dist_3(lat1, lon1, lat2, lon2):
  """Return distance between two latitude longtitude points from
  [understanding terms in Length of Degree formula](https://gis.stackexchange.com/questions/75528/understanding-terms-in-length-of-degree-formula/75535#75535)
  """
  lat = (lat1+lat2) * deg2rad / 2.0 # or just use lat1 for slightly less accurate estimate
  
  (latlen,longlen) = get_lat_len_to_metre_factors_at(lat)

  dlat = abs(lat2 - lat1) 
  dlon = abs(lon2 - lon1) 

  dist_m = math.sqrt( pow( dlat * latlen, 2) + pow( dlon * longlen, 2) )
  
  return dist_m

def convert_lat_len_coords_to_metres():
  exit(1)

# Calculate polygon area

def polygon_area(x,y):
  """Return area of polygon enclosed by a series of x and y coordinates, c.f.
  https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates"""
  return 0.5 * np.abs( np.dot(x,np.roll(y,1)) - np.dot(y,np.roll(x,1)))

# Helper functions for real umber formatting

def s_real(x):
  "Format real number to two decimanl places."
  return '{0:.2f}'.format( x )

def s_signed_real(x):
  "Format real number to two decimanl places with leading plus or minus sign."
  s = s_real(x)
  if 0 <= x: s = '+' + s
  return s

# Calculate and compare distances

n = len(pts)

print( n, 'points:')

for i in range(n):
  print(' ', tags[i],pts[i])

xs = [p[0] for p in pts]
ys = [p[1] for p in pts]

centre_point = [np.mean(xs), np.mean(ys)]

print('centre point:\n ', centre_point)

print('edge lengths:')

def calculate_and_compare(f,i,j,e):
  "Return string result for calculating and comparing with expected result"
  d = f( pts[i][0], pts[i][1], pts[j][0], pts[j][1])
  return s_real(d) + ' (' + s_signed_real(d-e) + ')'

for i in range(n):
  j = i + 1
  if j >= n: j -= n
  e = edge_length[i]
  print(tags[i], '-', tags[j] + ':', s_real(e),
    calculate_and_compare( lat_lon_dist_1, i, j, e ),
    calculate_and_compare( lat_lon_dist_2, i, j, e ),
    calculate_and_compare( lat_lon_dist_3, i, j, e ))

# Convert the corner point coordinates to metres

lat = centre_point[0] * deg2rad / 2.0

(latlen,longlen) = get_lat_len_to_metre_factors_at(lat)

xs = [p[0] * latlen for p in pts]
ys = [p[1] * longlen for p in pts]

area_calculated = polygon_area(xs, ys)

print('area', area, 'error', s_signed_real(area_calculated, area))
