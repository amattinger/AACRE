"""
    define directory and filenames of input data files and result file for
    oxts and ublox gps system unit tests
"""

# to create the maps, you need to make an api key [can setup with google cloud]
API_KEY = ''

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
