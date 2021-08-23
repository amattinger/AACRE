"""
    oxts gps system unit test:
    USER: initialize field names, as they vary file-to-file
    1. plot lat/lon and create google maps overlay
    2. plot velocity [north, east, and down] as a function of time in 3 different sub-plots 
    USER: check whether velE/N/D already exist, set up test 2 accordingly
    3. plot velocity [forward and lateral] as a function of time
    4. plot linear acceleration [x, y, and z] as a function of time
    5. plot number of gps satellites as a function of time, output mean # of sats
"""

import pandas as pd  
import matplotlib.pyplot as plt
import gmplot as gmp
import pymap3d as pm # for test 2 if enu needed

from data_files import API_KEY, DATA_DIR, SAVED_MAP

# USER: change suffix if using one of the other sample files
DATA_FILE = DATA_DIR + '210720_182517.xcom.NCOM0SummaryPage.csv'  


def main():
    """
    begin code for oxts unit test 1
    """
    # USER: set field names [variation b/t files]
    time = ' Time from start of region()'
    #delimiter = ','
    lat_col = ' Latitude(deg)'
    lon_col = ' Longitude(deg)'
    alt_col = ' Altitude(m)'
    # test 2
    vel_down = ' Velocity down(m/s)'
    vel_north = ''
    vel_east = ''
    # test 3
    vel_fwd = ' Velocity forward(m/s)'
    vel_lat = ' Velocity lateral(m/s)'
    # test 4
    x_accel = ' Acceleration Xv(m/s²)'
    y_accel = ' Acceleration Yv(m/s²)'
    z_accel = ' Acceleration Zv(m/s²)'
    # test 5
    num_sats = ' Number of GPS satellites used()'

    df = pd.read_csv(DATA_FILE) 

    # 1. plot lat/lon and create google maps overlay

    # set origin
    lat0 = df[lat_col][0]
    lon0 = df[lon_col][0]
    alt0 = df[alt_col][0]

    zoom = 17 # default zoom, change as desired 
    gmap = gmp.GoogleMapPlotter(lat0, lon0, zoom) # create map at origin

    # overlay coordinate points onto map
    lats = df[lat_col]
    lons = df[lon_col]
    xth = 2000 # default 1, increase as needed for bigger files

    gmap.scatter(lats[::xth], lons[::xth], size = 1, 
                  linewidth = 1, marker = False) 

    # draw blue line b/t given coordinate points
    gmap.plot(df[lat_col], df[lon_col],
               color = 'cornflowerblue', edge_width = 2.5)

    # note: as of june 2018, google requires making an api key to use maps
    gmap.apikey = API_KEY

    gmap.draw(SAVED_MAP)

    # 2. plot velocity [north, east, and down] as a function of time 

    # if missing vel east/north/down fields, get enu coords then take Δpos/Δtime

    # convert lat/lon data to enu coordinates

    enu = []

    for i in range(len(df.index)):
        lat = df[lat_col][i]
        lon = df[lon_col][i]
        alt = df[alt_col][i]
        enu.append({'enu': str(pm.geodetic2enu(lat, lon, alt, lat0, lon0, alt0))})

    # make a new dataframe w/ enu coordinates
    enu_df = pd.DataFrame(enu)

    # split ENU coordinates from one column into three separate columns
    enu_df = enu_df['enu'].str.strip('()')\
                .str.split(', ', expand=True)\
                .rename(columns={0:'east', 1:'north', 2:'up'})

    # insert time column to get 4 column df, start time at 0 and use +0.05s increments
    #enuDf.insert(0, "time", df['time'], True)
    time_increment = 0.05
    enu_df.insert(0, 'time', True)
    enu_df['time'] = df.index * time_increment

    # fix enu coords so they're not strings [else y-axis would be unordered in plot]
    enu_df["east"] = pd.to_numeric(enu_df["east"], downcast="float", errors='coerce')
    enu_df["north"] = pd.to_numeric(enu_df["north"], downcast="float", errors='coerce')
    enu_df["up"] = pd.to_numeric(enu_df["up"], downcast="float", errors='coerce')

    # now that we have enu positional coordinates, compute Δpos/Δtime
    enu_df.insert(4, 'velEast', True)
    enu_df.insert(5, 'velNorth', True)
    #enu_df.insert(6, 'velDown', True)
    for i in range(1, len(df.index)):
        enu_df['velEast'] = (enu_df['east'][i] - enu_df['east'][i-1])/time_increment
        enu_df['velNorth'] = (enu_df['north'][i] - enu_df['north'][i-1])/time_increment
        #enu_df['velDown'] = (enu_df['up'][i-1] - enu_df['up'][i])/time_increment # note: down, not up

    vel_east = 'velEast'
    vel_north = 'velNorth'
    #vel_down = 'velDown'

    # USER: if already have velEast, velNorth, and velDown fields, can remove or comment 
    # out everything b/t test 2's description/header comment and here

    # for each: set df or enu_df according to whether field existed in original file
    t = df[time]
    e = enu_df[vel_east]
    n = enu_df[vel_north]
    d = df[vel_down]

    fig0, (ax0, ax1, ax2) = plt.subplots(3)
    ax0.title.set_text('Velocity [east, north, down] vs. Time')
    nth = 2000 # for simplicity, only every nth pt is plotted; change as needed.
    ax0.plot(t[::nth], e[::nth]) # set df or enuDf
    ax0.set(xlabel='time [s]', ylabel='east v [m/s]')
    ax1.plot(t[::nth], n[::nth]) # set df or enuDf 
    ax1.set(xlabel='time [s]', ylabel='north v [m/s]')
    ax2.plot(t[::nth], d[::nth]) # set df or enuDf 
    ax2.set(xlabel='time [s]', ylabel='down v [m/s]')
    fig0.tight_layout() # fixes overlap b/t subplots

    # 3. plot velocity [forward and lateral] as a function of time

    fig1, (ax3, ax4) = plt.subplots(2)
    ax3.title.set_text('Velocity [fwd, lateral] vs. Time')
    ax3.plot(df[time], df[vel_fwd])
    ax3.set(xlabel='time [s]', ylabel='forward v [m/s]')
    ax4.plot(df[time], df[vel_lat])
    ax4.set(xlabel='time [s]', ylabel='lateral v [m/s]')

    # 4. plot linear acceleration [x, y, and z] as a function of time
    t = df[time]
    x = df[x_accel]
    y = df[y_accel]
    z = df[z_accel]

    fig2, (ax5, ax6, ax7) = plt.subplots(3)
    ax5.title.set_text('Acceleration [x, y, z] vs. Time')
    ax5.plot(t[::nth], x[::nth], 'tab:red')
    ax5.set(xlabel='time [s]', ylabel='x accel [m/s²]')
    ax6.plot(t[::nth], y[::nth], 'tab:green')
    ax6.set(xlabel='time [s]', ylabel='y accel [m/s²]')
    ax7.plot(t[::nth], z[::nth], 'tab:blue')
    ax7.set(xlabel='time [s]', ylabel='z accel [m/s²]')
    fig2.tight_layout() # fixes overlap b/t subplots

    # 5. plot number of gps satellites as a function of time, output mean # of sats
    fig3, ax8 = plt.subplots()
    ax8.title.set_text('GPS Number of Satellites vs. Time')
    ax8.scatter(df[time], df[num_sats], s=1)
    ax8.set(xlabel='time [s]', ylabel='no. SVs')

    # average number of satellites
    print("\nAverage number of satellites:", format(df[num_sats].mean(), '.2f'))

    
if __name__ == '__main__':
    main()
