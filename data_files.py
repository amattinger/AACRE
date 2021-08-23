"""
    define directory and filenames of input data files and result file for
    oxts and ublox gps system unit tests
"""

# USER: to create maps [ublox2 and oxts], first need an api key [can create with google cloud]
API_KEY = ''

# USER: set first part of pathname to all downloaded files
DATA_DIR = './data/' 

# RUN_CODE = "15-53-28"
RUN_CODE = "16-10-12"

FIX_FILE = DATA_DIR + RUN_CODE + '_ublox_fix.csv'
RXM_FILE = DATA_DIR + RUN_CODE + '_ublox_rxmraw.csv'
SOL_FILE = DATA_DIR + RUN_CODE + '_ublox_navsol.csv'

PROCESSED_FILE = DATA_DIR + 'gps_data_processed.csv'

MAP_LOC = DATA_DIR + 'gmap_data.html'
SAVED_MAP = DATA_DIR + 'oxts_data_processed.html'  # for google maps overlay
DELIMITER = ','
