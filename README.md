# AACRE
Summer 2021 work for Stanford NAVLab through AACRE

ublox_unit_test1:
1. Preprocesses raw csv data to add column headers if needed to account for max. satellites per row in file
2. Sets initial time to 0
3. Plots number of satellites against time
4. Checks for code carrier correlation with multiplier [0.19m]
  a. equivalency
  b. perfect multiple
  
ublox_unit_test2 [INCOMPLETE]:
1. Converts raw latitude-longitude-altitude coordinates into east-north-up (ENU) coordinates
2. Rewrites time to start from 0 and increase in 0.05s increments
3. TODO:
  a. make sure the plots above are actually correct. They all look the same,
     and it takes forever (up to 10 minutes) for them to generate on my computer,
     regardless of which method I use (plotting df or array)
  b. fix labels so they're not all overlapping each other
  c. overlay coordinates on Google Maps (currently not included in this file)
