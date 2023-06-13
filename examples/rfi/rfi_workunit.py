#! /usr/bin/env python

# We recorded 4 channl of data for ~100s, and the channel numbers are 30583 ~ 30586.
# The frequency range is  466.659545898438MHz to 466.705322265625MHz.
# Due to the RFI from Roach2 board(133.33MHz x 11 = 1466.663MHz), we should be able to see some RFI signals from the 4 channels of data.

import pywu

# we will use the follwing 2 files
dfile = "../../data_example/serendip6_m15_1.05G-1.45G_MB_03_00_20230613_080541_546953427_raw.dat"
rfile = "../../data_example/redis_info.json"
start_ch = 30583 

# open data file
f = pywu.io.dfile(dfile)
info = f.dparse()
t = info['timestamp']
beam = info['beam']

# get metadata from redis_info.json
r = pywu.io.redis_info(rfile)

# seek coords from redis_info.json
nsec = 69
coord = r.seekcoord(beam, t, nsec)
# read data out
nsamples = 1048576
channels = 4
d = f.dread(nsamples, channels=channels)
# generate workunit for channel 0
for ch in range(4):
    ofile = 'workunit' + str(ch) + '.sah'
    wu = pywu.wu_file(ofile)
    wu.init_header(info, coord, ch)
    # recal the center_freq
    ch_center_freq = pywu.LO + pywu.FS/pywu.FFT_POINT*(ch + start_ch)
    pywu.subband_desc['number'] = ch + start_ch
    pywu.subband_desc['center'] = ch_center_freq
    pywu.subband_desc['base'] = ch_center_freq
    wu.set_data(d[ch])
    wu.gen()