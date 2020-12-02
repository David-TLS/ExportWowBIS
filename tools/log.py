import logging
from time import gmtime, strftime

# file in file with datetime
def log(string):
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    logging.debug(time + ' - ' + string)
