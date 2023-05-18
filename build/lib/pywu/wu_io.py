"""
The module provides methods for parsing/reading raw PFB data files and redis info file.
"""
import json
import numpy as np
from datetime import datetime, timezone, timedelta
import astropy.time
import math

# We use beijing time, so we need to convert it to UTC time
UTC_OFFSET = 8
# We recorded 256 channels of data
CHANNELS = 256
# We recorded re and im in byte
FRAME_SIZE = CHANNELS * 2
# ADC sampling freq
FS = 1000 * 10**6
# FFT points
FFT_POINT = 65536
# The data size we expected in one second
FRAME_SIZE_PER_SEC = math.floor(FS/FFT_POINT)*FRAME_SIZE

info = {
    'sw'        : '', \
    'node'      : '', \
    'band'      : '', \
    'receiver'  : '', \
    'beam'      : '', \
    'pol'       : '', \
    'date'      : '', \
    'time'      : '', \
    'nanosec'   : ''
}

class dfile(object):
    """
    Description:
        The dfile class parses the raw PFB data file name,
        and read data from the file. 
    """
    def __init__(self, filename):
        """
        Description:
            Create a dfile object based on the filename.
            It will also parse the filename, and get the info from the filename.
        Inputs:
            - filename(str): Data file name.
                Default=None
        """
        self.filename = filename
        self.info = info
        try:
            self.fp = open(self.filename, 'rb')
        except:
            raise Exception('File does not exist!')
        self.data = 0
        # parse the file name
        fnstr = self.filename.split('/')[-1].strip('.dat').split('_')
        i = 0
        for k in self.info:
            self.info[k] = fnstr[i]
            i += 1
        datetime_str = self.info['date'] + self.info['time']
        tz = timezone(timedelta(hours=UTC_OFFSET))
        self.info['datetime'] = datetime.strptime(datetime_str, '%Y%m%d%H%M%S').replace(tzinfo=tz)
        self.info['timestamp'] = self.info['datetime'].timestamp() + int(self.info['nanosec'])/10**9
        self.info['time_recorded'] = datetime.strftime(self.info['datetime'],"%a %b %d %H:%M:%S %Y")
        t = astropy.time.Time(self.info['datetime'])
        self.info['time_recorded_jd'] = t.jd
        self.info['beam'] = int(self.info['beam'])
        self.info['pol'] = int(self.info['pol'])

    def dread(self, nsec, skip=0):
        """
        Description:
            read data from data file
        Inputs:
            - nsec(int): The length of data in seconds.
                Default=None
            - skip(int): Before reading data out, skip the data in frame.
                Default=0
        Output:
            - d(np.ndarray):
                returns nsec seconds of data in 256 channels.
                d[0] is the first channel of data,
                d[1] is the second channel of data,
                ...
                d[255] is the last channel of data.
        """
        # little-endian integer-16
        dtype = np.dtype('<u2')
        start = skip * FRAME_SIZE
        self.fp.seek(start,1)
        nbytes = nsec * FRAME_SIZE_PER_SEC
        d = np.frombuffer(self.fp.read(nbytes), dtype=dtype)
        d.shape = (-1,CHANNELS)
        return d.transpose()
    


class redis_info(object):
    """
    Description:
        The redis_info class loads redis_info.json, 
        which is genetated when we were observing.
    """
    def __init__(self, filename):
        """
        Description:
            Create a redis_info object based on the filename.
        Input:
            - filename(str): redis_info.json
                Default=None
        """
        self.filename = filename
        with open(self.filename) as f:
            self.metadata = json.load(f)
        for md in self.metadata:
            md['TimeStamp'] = float(md['TimeStamp'])/1000.0
    
    def seekcoord(self, b, t, l):
        """
        Description:
            seek for the coord by beam number, start time and length.
        Inputs:
            - b(int): Beam number, which should range from 0-18 for FAST MB receiver.
                Default=None
            - t(float): Start time for the observation, which is from the file name of raw PFB data.
                Default=None
            - l(int): It means how many seconds of coord we want.
                Default=None
        Output:
            - coords(list): 
                It's a list of coords, and each item is a dict, which contains time, ra and dec.
        """
        start = self.metadata[0]['TimeStamp']
        offset = 0
        for md in self.metadata:
            if(abs(md['TimeStamp'] - t)<=0.5):
                break
            offset += 1
        coords = []
        for i in range(l):
            time = self.metadata[i+offset]['TimeStamp']
            beam = 'SDP_Beam%02d_RA'%(b)
            ra = self.metadata[i+offset][beam]
            dec = self.metadata[i+offset][beam]
            coord = {
                'class' : 'xml_base', \
                'time'  : time, \
                'ra'    : ra, \
                'dec'   : dec
            }
            coords.append(coord)
        return np.array(coords)