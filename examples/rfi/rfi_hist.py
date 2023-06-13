#! /usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import pywu
import struct

# we will use the follwing 2 files
dfile = "../../data_example/serendip6_m15_1.05G-1.45G_MB_03_00_20230613_080541_546953427_raw.dat"
# open data file
f = pywu.io.dfile(dfile)
info = f.dparse()

# read data out
nsamples = 1048576
channels = 4
d = f.dread(nsamples, channels=channels)

fig = plt.figure()

for i in range(channels):
    dbytes = struct.pack('<%dH'%(nsamples),*d[i])
    data = struct.unpack('%db'%(nsamples*2), dbytes)
    data = np.array(data)
    data.shape = (2,-1)
    subplot = fig.add_subplot(channels, 2, 2*i+1)
    subplot.hist(data[0], bins=np.arange(-128,128),color='red')
    subplot.set_title('CH-%d-Re'%(i))
    #subplot.set_xlabel('Values')
    subplot.set_ylabel('Numbers')
    subplot = fig.add_subplot(channels, 2, 2*i+2)
    subplot.set_title('CH-%d-Im'%(i))
    #subplot.set_xlabel('Values')
    subplot.set_ylabel('Numbers')
    subplot.hist(data[1], bins=np.arange(-128,128),color='blue')
fig.suptitle('Histogram of PFB Output')
#fig.tight_layout()
plt.show()

