Summer 2021 unit tests for Stanford NAVLab TRI project through AACRE //
Author: Anna Mattinger

ublox_unit_test1:
1. Preprocesses raw csv data to add column headers if needed to account for max. satellites per row in file
2. Sets initial time to 0
3. Plots number of satellites against time
4. Checks for code carrier correlation with multiplier [0.19m]
  a. equivalency
  b. perfect multiple
  
ublox_unit_test2:
Requires API key for test 4
1. Converts raw latitude-longitude-altitude coordinates into east-north-up (ENU) coordinates
2. Rewrites time to start from 0 and increase in 0.05s increments
3. Plots east, north, and up coordinates each vs. time.
4. Overlays lat/lon coordinates on Google Maps

oxts_unit_test:
Requires an API Key for test 1
1. Plots lat/lon and creates Google Maps overlay
2. Plots velocity (north, east, and down) as a function of time 
  NOTE: requires user set-up based on whether there are preexisting velE/N/D fields
3. Plots velocity (forward and lateral) as a function of time
4. Plots linear acceleration (x, y, and z) as a function of time
5. Plots number of gps satellites as a function of time, outputs mean # of sats

ublox_unit_test3:
Explores the covariance fields and assumes there are three (posn_covariance0, 4 and 8) including looking at 
num sats and pDOP to see if any connection to one another and/or to covariance
Uses three corresponding ROS topics
0. Preprocesses rxmraw file by adding column headers; turns fixFile, solFile, and rxmFile into dfs
1. Plots the position covariance fields in a single plot vs time
2. Plots cov0, cov4, and cov8 as three separate subplots
3. Plots number of satellites vs time 
4. Plots position dilution of precision vs time
5. Prints some basic stats (mean, min, max)
6. Plots covariances across three limited ranges (x<100, 100<x<1000, x>1000)
