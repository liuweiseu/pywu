"""
The module provides methods for parsing/reading raw PFB data files and redis info file.
"""
import json
import numpy as np
from datetime import datetime, timezone, timedelta
import astropy.time
import math

from .obs_config import *

info = {
    'fn'        : '', \
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
        

    def dparse(self):
        """
        Description:
            parse the raw data filename, getting starting time, beam No...from the filename. 
        """
        try:
            self.fp = open(self.filename, 'rb')
        except:
            raise Exception('File does not exist!')
        self.data = 0
        # parse the file name
        fnstr = self.filename.split('/')[-1].strip('.dat').split('_')
        i = 0
        for k in self.info:
            if(k == 'fn'):
                continue
            self.info[k] = fnstr[i]
            i += 1
        self.info['fn'] = self.filename.split('/')[-1].strip('.dat')
        datetime_str = self.info['date'] + self.info['time']
        tz = timezone(timedelta(hours=UTC_OFFSET))
        self.info['datetime'] = datetime.strptime(datetime_str, '%Y%m%d%H%M%S').replace(tzinfo=tz)
        self.info['timestamp'] = self.info['datetime'].timestamp() + int(self.info['nanosec'])/10**9
        self.info['time_recorded'] = datetime.strftime(self.info['datetime'],"%a %b %d %H:%M:%S %Y")
        t = astropy.time.Time(self.info['datetime'])
        self.info['time_recorded_jd'] = t.jd
        self.info['beam'] = int(self.info['beam']) - 1
        self.info['pol'] = int(self.info['pol'])
        return self.info
    
    def dread(self, nsamples, skip=0, channels=CHANNELS):
        """
        Description:
            read data from data file
        Inputs:
            - nsamples(int): The number of samples.
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
        # TODO: double check the dtype here, and check if it's big-endian or litter endian.
        #       what we expected is real part in low address  
        dtype = np.dtype('<u2')
        sample_size = channels * BYTES_PER_SAMPLE
        start = skip * sample_size
        self.fp.seek(start,1)
        nbytes = nsamples * sample_size
        if(nsamples == -1):
            d = np.frombuffer(self.fp.read(), dtype=dtype)
        else:
            d = np.frombuffer(self.fp.read(nbytes), dtype=dtype)
        d.shape = (-1,channels)
        return d.transpose()
    

def jsonfix(filename):
    """
    Description:
        This method is used for fix json format.
        The origianl format of redis_info.json is not standard json.
    Input:
        - filename(str): the json file.
    """
    f = open(filename,'r+')
    content = f.read()
    content = content.replace('}{','},{')
    f.seek(0,0)
    f.write('[\n'+content+'\n]')
    f.close()
    
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
        try:
            with open(self.filename) as f:
                self.metadata = json.load(f)
        except:
            jsonfix(self.filename)
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
        offset = 0
        for md in self.metadata:
            if(abs(md['TimeStamp'] - t)<=1):
                break
            offset += 1
        coords = []
        i = 0
        #for i in range(l):
        while True:
            timestamp = self.metadata[i+offset]['TimeStamp']
            i = i + 1
            if((timestamp - t - l) >= 1):
                break
            t_dt = datetime.utcfromtimestamp(float(timestamp))
            t_astro = astropy.time.Time(t_dt)
            s = 'SDP_Beam%02d_RA'%(b)
            ra = self.metadata[i+offset][s]
            s = 'SDP_Beam%02d_DEC'%(b)
            dec = self.metadata[i+offset][s]
            coord = {
                'class' : 'xml_base', \
                'tag'   : 'coordinate_t', \
                'time'  : t_astro.jd, \
                'ra'    : ra, \
                'dec'   : dec
            }
            coords.append(coord)
        return np.array(coords)