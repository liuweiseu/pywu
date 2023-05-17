#! /usr/bin/env python

import os, sys

sys.path.insert(0, '../pywu/')

from data_parse import dfile,redis_info

def main():
    r = redis_info('../data_example/redis_info_20230511.json')
    print(r.metadata[0]['TimeStamp'])
    f = dfile('../data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat')
    print(f.info)
    coord = r.seekcood(0,f.info['timestamp'], 6)
    print(coord)

if __name__ == '__main__':
    main()
