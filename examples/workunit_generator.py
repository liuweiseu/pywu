#! /usr/bin/env python

import sys, os
from datetime import datetime
import numpy as np

import pywu

def main():
    # open data file
    f = pywu.io.dfile('../data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat')
    info = f.info
    # get metadata from redis_info.json
    r = pywu.io.redis_info('../data_example/redis_info_20230511.json')
    # seek coord from redis, and read data from the data file
    nsec = 2
    coord = r.seekcood(0,f.info['timestamp'], 6)
    d = f.dread(nsec)
    # put data into the file
    pywu.data['values'] = d[0]
    # generate workunit
    ch = 2
    wu = pywu.wu_file('workunit.sah')
    wu.init_header(info, coord, ch)
    wu.set_data(d[ch])
    wu.gen()

if __name__ == '__main__':
    main()