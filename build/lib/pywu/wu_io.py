import json
import numpy as np
from datetime import datetime, timezone, timedelta
import astropy.time
import math

# We use beijing time, so we need to convert it to UTC time
UTC_OFFSET = 8
CHANNELS = 256
FRAME_SIZE = CHANNELS * 2
FS = 1000 * 10**6
FFT_POINT = 65536
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
    def __init__(self, filename):
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

    def dread(self, nsec=-1, skip=0):
        """
        Description:
            read data from data file
        Inputs:
            - nsec(int):

            - skip(int):

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
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.metadata = json.load(f)
        for md in self.metadata:
            md['TimeStamp'] = float(md['TimeStamp'])/1000.0
    
    def seekcood(self, b, t, l):
        start = self.metadata[0]['TimeStamp']
        offset = 0
        for md in self.metadata:
            if(abs(md['TimeStamp'] - t)<=0.5):
                break
            offset += 1
        cood = []
        for i in range(l):
            time = self.metadata[i+offset]['TimeStamp']
            beam = 'SDP_Beam%02d_RA'%(b)
            ra = self.metadata[i+offset][beam]
            dec = self.metadata[i+offset][beam]
            md = {
                'class' : 'xml_base', \
                'time'  : time, \
                'ra'    : ra, \
                'dec'   : dec
            }
            cood.append(md)
        return np.array(cood)