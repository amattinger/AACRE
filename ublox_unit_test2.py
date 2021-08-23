"""
    u-blox gps unit test 2:
    1. converts raw latitude-longitude-altitude coordinates into east-north-up (enu) coordinates
    2. rewrites time to start from 0 and increase in 0.05s increments
    3. plots east, north, and up coordinates each vs. time.
    4. overlays lat/lon coordinates on google maps [USER: requires making an api key]
"""

import pandas as pd
import matplotlib.pyplot as plt
import gmplot as gmp
import numpy as np
import pymap3d as pm

from data_files import API_KEY, FIX_FILE, MAP_LOC

DATA_FILE = FIX_FILE

LAT_COL = 'field.latitude'
LON_COL = 'field.longitude'
ALT_COL = 'field.altitude'


def main():
    """
    begin code for unit test 2
    """
    df = pd.read_csv(DATA_FILE)
    # print(df)

    # set origin [default: use starting coordinates]
    lat0 = df[LAT_COL][0]
    lon0 = df[LON_COL][0]
    alt0 = df[ALT_COL][0]

    # 1. get enu [east north up] coordinates and plot each vs time

    # convert lat/lon data to ENU
    enu = []

    for i in range(len(df.index)):
        lat = df[LAT_COL][i]
        lon = df[LON_COL][i]
        alt = df[ALT_COL][i]
        enu.append({'enu': str(pm.geodetic2enu(lat, lon, alt, lat0, lon0, alt0))})

    # make a new dataframe w/ enu coordinates
    enu_df = pd.DataFrame(enu)

    # split enu coordinates from one column into three separate columns
    enu_df = enu_df['enu'].str.strip('()').str.split(', ', expand=True).rename(
        columns={0: 'east', 1: 'north', 2: 'up'})

    # insert time column, resulting in 4 column df, convert time so it
    # begins at 0 and increases by 0.05s increments
    # enu_df.insert(0, "time", df['time'], True)
    enu_df.insert(0, 'time', True)
    enu_df['time'] = df.index * 0.05  # pylint: disable=no-member

    # change enu coords from strings else y-axis will be unordered in plots
    enu_df["east"] = pd.to_numeric(enu_df["east"], downcast="float", errors='coerce')
    enu_df["north"] = pd.to_numeric(enu_df["north"], downcast="float", errors='coerce')
    enu_df["up"] = pd.to_numeric(enu_df["up"], downcast="float", errors='coerce')

    # plotting time vs east as array 
    enu = np.array(enu_df)
    t = enu[:, 0]
    e = enu[:, 1]
    n = enu[:, 2]
    u = enu[:, 3]

    x = 1  # for simplicity, only every x-th pt is plotted; change as needed.
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.plot(t[::x], e[::x], 'tab:red')
    ax1.set(xlabel='time [s]', ylabel='east')
    ax2.plot(t[::x], n[::x], 'tab:green')
    ax2.set(xlabel='time [s]', ylabel='north')
    ax3.plot(t[::x], u[::x], 'tab:blue')
    ax3.set(xlabel='time [s]', ylabel='up')
    fig.tight_layout()  # fixes overlap b/t subplots

    # 2. overlay lat/lon coordinates on Google Maps

    zoom = 17  # default zoom, change as desired
    gmap1 = gmp.GoogleMapPlotter(lat0, lon0, zoom)  # create map at origin

    # overlays coordinate points onto map
    gmap1.scatter(df[LAT_COL], df[LON_COL], size=1,
                  linewidth=1, marker=False)

    # draws a blue line b/t given coordinate points
    gmap1.plot(df[LAT_COL], df[LON_COL],
               color='cornflowerblue', edge_width=2.5)

    # google requires making an api key to use maps as of june 2018
    gmap1.apikey = API_KEY

    gmap1.draw(MAP_LOC)


if __name__ == '__main__':
    main()
