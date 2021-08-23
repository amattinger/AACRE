"""
    u-blox gps unit test 3:
    this script explores the covariance fields and assumes there are three 
        [posn_covariance0, 4 and 8]
    1. plot the position covariance fields in a single plot vs time
    2. plot cov0, cov4, and cov8 as three separate subplots
       look at num sats and pDOP to see if any connection to one another and/or to covariance
    3. plot number of satellites vs time 
    4. plot position dilution of precision vs time
    5. print some basic stats [mean, min, max]
    6. plot covariances across three limited ranges [x<100, 100<x<1000, x>1000]
"""

import pandas as pd
import matplotlib.pyplot as plt

from data_files import DELIMITER, FIX_FILE, RXM_FILE, SOL_FILE, PROCESSED_FILE

def main():
    """
    begin code for unit test 3
    0. preprocess rxmraw file by adding column headers; turn FIX, SOL,
    and RXM files into dfs
    assumption: files are synchronized
    """
    # fixFile directly to df
    fix_df = pd.read_csv(FIX_FILE)
    sol_df = pd.read_csv(SOL_FILE)
    max_cols = 0

    # preprocess rxmFile
    # loop through data lines
    with open(RXM_FILE, 'r') as temp:
        lines = temp.readlines()
        for line in lines:
            # count columns in current line
            col_count = len(line.split(DELIMITER)) + 1
            # Set the new most column count
            max_cols = col_count if max_cols < col_count else max_cols

    # set column names
    col_names = ['%time', 'rcvTOW', 'week', 'numSV', 'reserved1']
    # generate column names for each satellite
    i = 0
    for _ in range(5, max_cols - 1, 7):
        n = str(i)
        col_names.extend(['sv' + n + '.cpMes', 'sv' + n + '.prMes', 'sv' + n + '.doMes',
                          'sv' + n + '.sv', 'sv' + n + '.mesQI', 'sv' + n + '.cno',
                          'sv' + n + '.lli'])
        i += 1

    # turn csv into a data file now that column names have been added
    rxm_df = pd.read_csv(RXM_FILE, header=None, delimiter=DELIMITER, names=col_names)
    rxm_df.drop(index=rxm_df.index[0], axis=0, inplace=True)  # pylint: disable=no-member
    # print(df)

    # save as csv, read into df
    rxm_df.to_csv(PROCESSED_FILE, index=False)  # pylint: disable=no-member
    rxm_df = pd.read_csv(PROCESSED_FILE)

    # 1. plot position covariance fields in one plot vs time

    # initialize with field names
    # assumes three covariance fields 0, 4, 8 by default; change as needed
    time = '%time'
    cov0 = 'field.position_covariance0'
    cov4 = 'field.position_covariance4'
    cov8 = 'field.position_covariance8'
    num_sats = 'numSV'
    p_dop = 'field.pDOP'

    # subtract first time from all subsequent times [i.e., start at t=0]
    fix_df[time] = fix_df[time].subtract(fix_df[time][0])
    rxm_df[time] = rxm_df[time].subtract(rxm_df[time][0])

    # plot cov0, cov4, and cov8 together in same plot
    _, ax0 = plt.subplots()
    ax0.set_title('Position Covariances vs Time [Plotted Together]')
    ax0.plot(fix_df[time], fix_df[cov0], label="cov0")
    ax0.plot(fix_df[time], fix_df[cov4], label="cov4")
    ax0.plot(fix_df[time], fix_df[cov8], label="cov8")
    ax0.legend()
    ax0.set_xlabel("time")
    ax0.set_ylabel("covariance")

    # 2. plot cov0, cov4, and cov8 as three separate subplots
    _, (ax_a, ax_b, ax_c) = plt.subplots(3, figsize=(15, 15))
    ax_a.set_title('Position Covariances vs Time [Plotted Separately]\nCovariance 0')
    ax_a.plot(fix_df[time], fix_df[cov0], label="cov0")
    ax_a.set_xlabel("time")
    ax_b.set_ylabel("cov0")
    ax_b.set_title('Covariance 4')
    ax_b.plot(fix_df[time], fix_df[cov4], label="cov4", color='darkorange')
    ax_b.set_xlabel("time")
    ax_b.set_ylabel("cov4")
    ax_c.set_title('Covariance 8')
    ax_c.plot(fix_df[time], fix_df[cov8], label="cov8", color='green')
    ax_c.set_xlabel("time")
    ax_c.set_ylabel("cov8")
    # plt.legend()

    # 3. plot number of satellites vs time
    _, ax1 = plt.subplots()
    ax1.scatter(rxm_df[time], rxm_df[num_sats], label="no. SVs")
    ax1.set_title('Number of Satellites vs. Time')
    plt.xlabel("time")
    plt.ylabel("No. SVs")

    # 4. plot position dilution of precision vs time
    _, ax2 = plt.subplots()
    ax2.scatter(sol_df[time], sol_df[p_dop], label="pDOP")
    ax2.set_title('pDOP vs. Time')
    plt.xlabel("time")
    plt.ylabel("pDOP")

    # arr = df.to_array()

    # 5. print some basic stats [mean, min, max]
    print("Position Covariance:")
    print("           cov0     cov4     cov8")
    print('Mean: {:9.2f}'.format(fix_df[cov0].mean()) + '{:9.2f}'.format(fix_df[cov4].mean()) +
          '{:9.2f}'.format(fix_df[cov8].mean()))
    print('Min: {:10.2f}'.format(fix_df[cov0].min()) + '{:9.2f}'.format(fix_df[cov4].min()) +
          '{:9.2f}'.format(fix_df[cov8].min()))
    print('Max: {:10.2f}'.format(fix_df[cov0].max()) + '{:9.2f}'.format(fix_df[cov4].max()) +
          '{:9.2f}'.format(fix_df[cov8].max()))

    print("              mean      min      max")
    print('no. SVs: {:9.2f}'.format(rxm_df[num_sats].mean()) +
          '{:9}'.format(rxm_df[num_sats].min()) + '{:9}'.format(rxm_df[num_sats].max()))

    # 6. plot covariances across three limited ranges [x<100, 100<x<1000, x>1000]

    # find largest maximum b/t cov0, cov4, cov8 [for upper bound on large range plot]
    if (fix_df[cov8].max() >= fix_df[cov0].max()) and (fix_df[cov8].max() >= fix_df[cov4].max()):
        max_max = fix_df[cov8].max()
    elif fix_df[cov0].max() >= fix_df[cov4].max():
        max_max = fix_df[cov0].max()
    else:
        max_max = fix_df[cov4].max()

    # small range plot [x<100]
    _, (ax_s, ax_m, ax_l) = plt.subplots(3, figsize=(15, 15))
    ax_s.set_title('Position Covariances vs Time [Segmented Ranges]\nSmall: 0-100')
    ax_s.plot(fix_df[time], fix_df[cov0], label="cov0")
    ax_s.plot(fix_df[time], fix_df[cov4], label="cov4")
    ax_s.plot(fix_df[time], fix_df[cov8], label="cov8")
    ax_s.set_ylim([0, 100])
    ax_s.legend()

    # medium range plot [100<x<1000]
    ax_m.set_title('Medium: 100-1000')
    ax_m.plot(fix_df[time], fix_df[cov0], label="cov0")
    ax_m.plot(fix_df[time], fix_df[cov4], label="cov4")
    ax_m.plot(fix_df[time], fix_df[cov8], label="cov8")
    ax_m.set_ylim([100, 1000])
    ax_m.legend()

    # large range plot [x>1000]
    ax_l.set_title('Large: 1000+')
    ax_l.plot(fix_df[time], fix_df[cov0], label="cov0")
    ax_l.plot(fix_df[time], fix_df[cov4], label="cov4")
    ax_l.plot(fix_df[time], fix_df[cov8], label="cov8")
    ax_l.set_ylim([1000, max_max])
    ax_l.legend()


if __name__ == '__main__':
    main()
