#!/usr/bin/env python3
# hoehenversatz.py - sum up waldrain terrain model height offsets
# Copyright (C) 2020 by Jeremy Tammik, Autodesk Inc.

import math, numpy as np

# Input data:
# 10 height offsets along the N borderline in 3 metre spacing from E to W
# repeat offset 3 metres southwards, 12 times over

offsets = [
  [+0, 33, 54, 61, 54, 65, 51, 61, 67, 83, 68],
  [+2, 57, 42, 70, 57, 47, 62, 61, 72, 96, 80],
  [+0, 78, 45, 61, 54, 64, 50, 73, 90, 130, 40],
  [+0, 88, 68, 52, 37, 66, 61, 69, 96, 111, 28],
  [-5, 108, 56, 38, 52, 80, 51, 83, 144, 53, 29],
  [-3, 122, 51, 20, 99, 65, 73, 77, 123, 34, 37],
  [-5, 130, 64, 44, 74, 62, 59]]

print('Offsets from E to W at 3 metre distances:')

line_begin = 0
offset_south = 3
cm = 0.01
dsouth = 0
for line in offsets:
  line_in_metres = [dh * cm for dh in line]
  line_begin += line_in_metres[0]
  line_offsets = line_in_metres[1:]
  h = line_begin
  line_cumulative = [h]
  for dh in line_offsets:
    h -= dh
    line_cumulative.append(h)
  print('{:5d}'.format(dsouth), ' '.join(['{:5.2f}'.format(dh) for dh in line_in_metres]))
  print('  kum', ' '.join(['{:5.2f}'.format(dh) for dh in line_cumulative]))
  dsouth += offset_south

