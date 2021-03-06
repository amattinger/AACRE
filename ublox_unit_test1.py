"""
    u-blox gps unit test 1:
    0. preprocess data in case variable number of columns/missing column headers
    1. plot number of satellites against time
    2. code carrier relation:
    2a. count times per sat that
        code [pseudorange/prMes] - absval carrier [cpMes]*0.19m = 0
    2b. check that prMeas is not a perfect multiple of 0.19*cpMeas
"""

import pandas as pd
import matplotlib.pyplot as plt

from data_files import DELIMITER, PROCESSED_FILE, RXM_FILE

DATA_FILE = RXM_FILE # input file


def main():
    """
    begin code for unit test 1
    """
    max_cols = 0
    # 0. preprocess data in case variable number of columns/missing column headers
    # loop through data lines
    with open(DATA_FILE, 'r') as temp:
        lines = temp.readlines()
        for line in lines:
            # count columns in current line
            col_count = len(line.split(DELIMITER)) + 1
            # Set the new most column count
            max_cols = col_count if max_cols < col_count else max_cols

    # set column names
    col_names = ['time', 'rcvTOW', 'week', 'numSV', 'reserved1']
    # generate column names for each satellite
    i = 0
    for col in range(5, max_cols - 1, 7):
        n = str(i)
        col_names.extend(['sv'+n+'.cpMes', 'sv'+n+'.prMes', 'sv'+n+'.doMes',
                          'sv'+n+'.sv', 'sv'+n+'.mesQI', 'sv'+n+'.cno',
                          'sv'+n+'.lli'])
        i += 1

    # turn csv into a data file now that column names have been added
    data_frame = pd.read_csv(DATA_FILE, header=None, delimiter=DELIMITER,
                             names=col_names)
    data_frame.drop(index=data_frame.index[0],  # pylint: disable=no-member
                    axis=0, inplace=True)

    # save as csv, read into data_frame
    data_frame.to_csv(PROCESSED_FILE, index=False)  # pylint: disable=no-member
    data_frame = pd.read_csv(PROCESSED_FILE)

    # 1. plot number of satellites against time, output mean

    # subtract first time from all subsequent times [i.e., start at t=0]
    data_frame['time'] = data_frame['time'].subtract(data_frame['time'][0])

    plt.scatter(data_frame['time'], data_frame['numSV'], s=1)
    plt.xlabel('time [s]')
    plt.ylabel('no. SVs')

    # average number of satellites
    print("\nAverage number of satellites:", format(data_frame['numSV'].mean(),
                                                    '.2f'))

    def x(a):
        return 0.19 * abs(a)

    # 2. code carrier relation:
    # 2a. count times per sat that
    #     code [pseudorange/prMes] - absval carrier [cpMes]*0.19m = 0 
    #     else correlations = 0 [which is good]
    codes = [col for col in data_frame.columns if 'prMes' in col]
    carriers = [col for col in data_frame.columns if 'cpMes' in col]

    print("\nFirst test: difference equals zero")
    for num, code in enumerate(codes):
        data_frame['sv' + str(num) + '.zeroCorr'] = (data_frame[code] -
                                                     x(data_frame[carriers[num]]) == 0)
        print(data_frame['sv' + str(num) + '.zeroCorr'].value_counts())

    # 2b. check that prMeas is not a perfect multiple of 0.19*cpMeas
    print("\nSecond test: perfect multiplier")
    for num, code in enumerate(codes):
        data_frame['sv' + str(num) + '.perfMult'] = (data_frame[code] %
                                                     x(data_frame[carriers[num]]) == 0)
        print(data_frame['sv' + str(num) + '.perfMult'].value_counts())


if __name__ == '__main__':
    main()
