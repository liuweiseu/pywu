"""
workunit template in dict format.
"""
import numpy as np

"""
In the wu_dict.py, we have a bit dict, 
which contains all the info requried by a workunit file.
"""

"""
tape template
"""
tape_info = {
    'class'            : 'xml_base', \
    'tag'              : 'tape_info', \
    'name'             : 'test', \
    'start_time'       : 2454822.5698634, \
    'last_block_time'  : 2454822.5698634, \
    'last_block_done'  : 6280, \
    'missed'           : 0, \
    'tape_quality'     : 0,
    'beam'             : 8
 }

"""
coordinate template
"""
coordinate_t = {
    'class'         : 'xml_base', \
    'tag'           : 'coordinate_t', \
    'time'          : 2454822.5698622, \
    'ra'            : 3.2887318938763, \
    'dec'           : 23.410418247457
}

"""
data_description template
""" 
data_desc =  {
    'class'             : 'xml_base', \
    'tag'               : 'data_desc', \
    'start_ra'          : 3.2887318938763, \
    'start_dec'         : 23.410418247457, \
    'end_ra'            : 3.3185884614727, \
    'end_dec'           : 26.095076667942, \
    'true_angle_range'  : 2.7152905955851, \
    'time_recorded'     : 'Mon Dec 22 01:40:36 2008', \
    'time_recorded_jd'  : 2454822.5698622, \
    'nsamples'          : 1048576, \
    'coords'            : ''
}

"""
corr_coeff template
"""
az_corr_coeff = {
    'class'         : 'xml_coeff', \
    'tag'           : 'az_corr_coeff', \
    'length'        : 99, \
    'encoding'      : "\"x-csv\"",\
    'values'        : [-37,-6.05,92.35,-731.21]
}

zen_corr_coeff = {
    'class'         : 'xml_coeff', \
    'tag'           : 'zen_corr_coeff', \
    'length'        : 99, \
    'encoding'      : "\"x-csv\"",\
    'values'        : [-37,-6.05,92.35,-731.21]
}
"""
receiver template
"""
receiver_cfg = {
    'class'         : 'xml_base', \
    'tag'           : 'receiver_cfg', \
    's4_id'         : 30, \
    'name'          : 'FAST 1.05G-1.45G MultiBeam, Beam 0, Pol 0', \
    'beam_width'    : 0.0483, \
    'center_freq'   : 1400, \
    'latitude'      : 25.652944, \
    'longitude'     : 106.856667, \
    'elevation'     : 1110.0288, \
    'diameter'      : 500, \
    'az_orientation': 0, \
    'az_corr_coeff' : 0, \
    'zen_corr_coeff': 0, \
    'array_az_ellipse' : 0, \
    'array_za_ellipse' : 0, \
    'array_angle'   : 0
}

"""
recorder template
"""
recorder_cfg = {
    'class'         : 'xml_base', \
    'tag'           : 'recorder_cfg', \
    'name'          : 'serendip6_reobs_FAST', \
    'bits_per_sample': 16, \
    'sample_rate'   : 15258.7890625, \
    'beams'         : 38, \
    'version'       : 2.000001
}

"""
splitter template
"""
splitter_cfg = {
    'class'         : 'xml_base', \
    'tag'           : 'splitter_cfg', \
    'version'       : 0.2123456, \
    'data_type'     : 'sun_binary',\
    'fft_len'       : 256, \
    'ifft_len'      : 1, \
    'filter'        : 'pfb', \
    'window'        : 'hanning', \
    'samples_per_wu': 1048576, \
    'highpass'      : 0, \
    'blanker_filter': 'randomize', \
    'wu_bits_per_sample' : 16
}

"""
chirp template
"""
chirp_parameter = {
    'class'         : 'xml_base', \
    'tag'           : 'chirp_parameter_t', \
    'chirp_limit'   : 30, \
    'fft_len_flags' : 262136
}
chirp_parameter_1 = {
    'class'         : 'xml_base', \
    'tag'           : 'chirp_parameter_t', \
    'chirp_limit'   : 100, \
    'fft_len_flags' : 65528
}
"""
analysis template
"""
analysis_cfg = {
    'class'                         : 'xml_base', \
    'tag'                           : 'analysis_cfg', \
    'spike_thresh'                  : 24, \
    'spikes_per_spectrum'           : 1,\
    'gauss_null_chi_sq_thresh'      : 2.15593648,\
    'gauss_chi_sq_thresh'           : 1.41999996,\
    'gauss_power_thresh'            : 3,\
    'gauss_peak_power_thresh'       : 3.20000005,\
    'gauss_pot_length'              : 64,\
    'pulse_thresh'                  : 19.1000000,\
    'pulse_display_thresh'          : 0.5,\
    'pulse_max'                     : 40960,\
    'pulse_min'                     : 16,\
    'pulse_fft_max'                 : 8192,\
    'pulse_pot_length'              : 256,\
    'triplet_thresh'                : 9.0,\
    'triplet_max'                   : 131072,\
    'triplet_min'                   : 16,\
    'triplet_pot_length'            : 256,\
    'pot_overlap_factor'            : 0.5,\
    'pot_t_offset'                  : 1,\
    'pot_min_slew'                  : 0.00209999993,\
    'pot_max_slew'                  : 0.0104999999,\
    'chirp_resolution'              : 0.333,\
    'analysis_fft_lengths'          : 262136,\
    'bsmooth_boxcar_length'         : 8192,\
    'bsmooth_chunk_size'            : 32768,\
    'chirps'                        : np.array([chirp_parameter, \
                                                chirp_parameter_1]),
    'pulse_beams'                   : 1, \
    'max_signals'                   : 1048576, \
    'max_spikes'                    : 1048576, \
    'max_autocorr'                  : 1048576, \
    'max_gaussians'                 : 1048576, \
    'max_pulses'                    : 1048576, \
    'max_triplets'                  : 1048576, \
    'keyuniq'                       : 7344400, \
    'credit_rate'                   : 2.8499999, \
    'autocorr_thresh'               : 19.75, \
    'autocorr_per_spectrum'         : 1, \
    'autocorr_fftlen'               : 131072, \
    'autocorr_min_delay_bins'       : 20
}

"""
subband template
"""
subband_desc = {
    'class'         : 'xml_base', \
    'tag'           : 'subband_desc', \
    'number'        : '',
    'center'        : 1420482788.0859,
    'base'          : 1420478515.625,
    'sample_rate'   : 15258.7890625
}
"""
group_info template
"""
group_info = {
    'class'         : 'xml_base', \
    'tag'           : 'group_info', \
    'tape_info'     : tape_info, \
    'name'          : '', \
    'data_desc'     : data_desc, \
    'receiver_cfg'  : receiver_cfg, \
    'recorder_cfg'  : recorder_cfg, \
    'splitter_cfg'  : splitter_cfg, \
    'analysis_cfg'  : analysis_cfg, \
    'sb_id'         : 0
}
"""
workunit_header template
"""
workunit_header = {
    'class'         : 'xml_base', \
    'tag'           : 'workunit_header', \
    'name'          : '', \
    'group_info'    : group_info, \
    'subband_desc'  : subband_desc, \
    'sb_id'         : 0
}

"""
data template
"""
wu_data = {
    'class'         : 'xml_data', \
    'tag'           : 'data', \
    'length'        : 2097152, \
    'encoding'      : "\"sun_binary\"",\
    'values'        : [48,49,50,-122,64]
}

"""
workunit group template
"""
workunit_grp = {
    'class'           : 'xml_base', \
    'tag'             : 'workunit', \
    'workunit_header' : workunit_header, \
    'data'            : wu_data
}