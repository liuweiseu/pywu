#! /usr/bin/env python

import pywu

def main():

    # open data file
    f = pywu.io.dfile('../data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat')
    info = f.info
    t = info['timestamp']
    beam = info['beam']
    # get metadata from redis_info.json
    r = pywu.io.redis_info('../data_example/redis_info.json')
    # seek coord from redis, and read data from the data file
    # we only get 2 seconds of data for test
    nsec = 2
    coord = r.seekcoord(beam, t, nsec)
    d = f.dread(nsec)
    # generate workunit for channel 0
    ch = 0
    wu = pywu.wu_file('workunit_example.sah')
    wu.init_header(info, coord, ch)
    wu.set_data(d[ch])
    wu.gen()

if __name__ == '__main__':
    main()