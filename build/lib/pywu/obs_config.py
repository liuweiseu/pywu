"""
All of the hardware info is here.
"""
import math

# We use beijing time, so we need to convert it to UTC time
UTC_OFFSET = 8
# started recording channel
START_CH = 27392
# We recorded 256 channels of data
CHANNELS = 256
# Bytes pe samples
BYTES_PER_SAMPLE = 2
# lo freq
LO = 1000
# ADC sampling freq
FS = 1000 * 10**6
# FFT points
FFT_POINT = 65536
# The data size we expected in one second
SAMPLES_PER_SEC = math.floor(FS/FFT_POINT)
