#! /usr/bin/env python

from argparse import ArgumentParser
import numpy as np
import pywu

def main():
    # get parameters
    parser = ArgumentParser(description="Usage for setiathome workunit generation.")
    parser.add_argument('--file','-f',type=str, dest='dfile', \
                        default='../data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat', \
                        help='raw PFB data file.')
    parser.add_argument('--redis','-r',type=str, dest='rfile', \
                        default='../data_example/redis_info.json', \
                        help='redis info file.')
    parser.add_argument('--channel','-c',type=int, dest='channel', \
                        default=0, \
                        help='specify the channel No.')
    parser.add_argument('--output','-o',type=str, dest='ofile', \
                        default='workunit_example.sah',
                        help='output filename.')
    args = parser.parse_args()

    # open data file
    f = pywu.io.dfile(args.dfile)
    info = f.dparse()
    t = info['timestamp']
    beam = info['beam']
    # get metadata from redis_info.json
    r = pywu.io.redis_info(args.rfile)
    # seek coord from redis, and read data from the data file
    # we only get 2 seconds of data for test
    nsec = 70
    coord = r.seekcoord(beam, t, nsec)
    nsamples = nsec * pywu.SAMPLES_PER_SEC
    d = f.dread(nsamples)
    # generate workunit for channel 0
    ch = args.channel
    wu = pywu.wu_file(args.ofile)
    wu.init_header(info, coord, ch)
    # this is the fake data for test
    data = np.ones(1048576, dtype=np.int16)
    #wu.set_data(d[ch])
    wu.set_data(data)
    wu.gen()

if __name__ == '__main__':
    main()