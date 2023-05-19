"""
All of the hardware info is here.
"""
# We use beijing time, so we need to convert it to UTC time
UTC_OFFSET = 8
# We recorded 256 channels of data
CHANNELS = 256
# We recorded re and im in byte
FRAME_SIZE = CHANNELS * 2
# lo freq
LO = 1000
# ADC sampling freq
FS = 1000 * 10**6
# FFT points
FFT_POINT = 65536
