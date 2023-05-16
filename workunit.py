"""
class: xml
"""
class xml(object):
    nindent = 0
    def __init__(self,name, info):
        self.f = 0
        self.name = name
        self.info = info
        
    def print_xml_begin(self,name):
        self.print_xml_indent()
        print("<%s>"%(name),file=self.f)

    def print_xml_end(self,name):
        self.print_xml_indent()
        print("</%s>"%(name), file=self.f)
    
    def print_xml_content(self, c):
        for k in c:
            v = c[k]
            if(isinstance(v,list)):
                self.print_xml_begin(k)
                for i in v:
                    i.print_xml(self.f)
                self.print_xml_end(k)
            elif(isinstance(v,dict)):
                ins = xml(k,v)
                ins.print_xml(self.f)
            elif(isinstance(v,xml)):
                v.print_xml(self.f)
            else:
                self.print_xml_indent()
                print("<%s>%s</%s>"%(k, v, k), file=self.f)

    def print_xml_indent(self):
        print(' '*xml.nindent, file=self.f, end='')

    def print_xml(self,f):
        self.f = f
        self.print_xml_begin(self.name)
        xml.nindent += 2
        self.print_xml_content(self.info)
        xml.nindent -= 2
        self.print_xml_end(self.name)


class xml_coeff(xml):
    def __init__(self, name, info):
        super(xml_coeff, self).__init__(name, info)

    def print_xml_begin(self, name):
        self.print_xml_indent()
        print("<%s "%(name),file=self.f, end='')
        for k in self.info:
            if k == 'values':
                break
            v = self.info[k]
            print("%s=%s "%(k,v),file=self.f, end='')
        print(">", file=self.f)
    def print_xml_content(self, c):
        self.print_xml_indent()
        for v in c['values'][:-1]:
            print("%s,"%(v), file=self.f, end='')
        print(c['values'][-1], file=self.f)
        
"""
tape example
"""
tape_info = {
    'name'             : 'test', \
    'start_time'       : 2454822.5698634, \
    'last_block_time'  : 2454822.5698634, \
    'last_block_done'  : 6280, \
    'missed'           : 0, \
    'tape_quality'     : 0,
    'beam'             : 8
 }


"""
coordinate example
"""
coordinate_t = {
    'time'          : 2454822.5698622, \
    'ra'            : 3.2887318938763, \
    'dec'           : 23.410418247457
}

"""
data_description example
""" 
coordinate_ins = xml('coordinate_t', coordinate_t)
data_desc =  {
    'start_ra'        : 3.2887318938763, \
    'start_dec'         : 23.410418247457, \
    'end_ra'            : 3.3185884614727, \
    'end_dec'           : 26.095076667942, \
    'true_angle_range'  : 2.7152905955851, \
    'time_recorded'     : 'Mon Dec 22 01:40:36 2008', \
    'time_recorded_jd'  : 2454822.5698622, \
    'nsamples'          : 1048576, \
    'coords'            : [coordinate_ins, coordinate_ins]
}

"""
corr_coeff example
"""
az_corr_coeff = {
    'length'        : 99, \
    'encoding'      : "\"x-csv\"",\
    'values'        : [-37,-6.05,92.35,-731.21]
}
az_corr_coeff_ins = xml_coeff('az_corr_coeff', az_corr_coeff)

zen_corr_coeff = {
    'length'        : 99, \
    'encoding'      : "\"x-csv\"",\
    'values'        : [-37,-6.05,92.35,-731.21]
}
zen_corr_coeff_ins = xml_coeff('zen_corr_coeff', zen_corr_coeff)
"""
receiver example
"""
receiver_cfg = {
    's4_id'         : 11, \
    'name'          : 'Arecibo 1.4GHz Array, Beam 4, Pol 0', \
    'beam_width'    : 0.0500000007, \
    'center_freq'   : 1420, \
    'latitude'      : 18.3538056, \
    'longitude'     : -66.7552222, \
    'elevation'     : 497, \
    'diameter'      : 168, \
    'az_orientation': 180, \
    'az_corr_coeff' : az_corr_coeff_ins, \
    'zen_corr_coeff': zen_corr_coeff_ins, \
    'array_az_ellipse' : 329.06, \
    'array_za_ellipse' : 384.005, \
    'array_angle'   : -60
}

"""
recorder example
"""
recorder_cfg = {
    'name'          : '', \
    'bits_per_sample': 2, \
    'sample_rate'   : 2500000, \
    'beams'         : 14, \
    'version'       : 1.99000001
}

"""
splitter example
"""
splitter_cfg = {
    'version'       : 0.200003, \
    'data_type'     : 'encoded',\
    'fft_len'       : 2048, \
    'ifft_len'      : 8, \
    'filter'        : 'fft', \
    'window'        : 'welsh', \
    'sammples_per_wu': 1048576, \
    'highpass'      : 0, \
    'blanker_filter': 'randomize'
}

"""
chirp example
"""
chirp_parameter = {
    'chirp_limit'   : 30, \
    'fft_len_flags' : 262136
}
chirp_parameter_t = xml('chirp_parameter_t', chirp_parameter)
"""
analysis example
"""
analysis_cfg = {
    'spike_thresh'                  : 24, \
    'spikes_per_spectrum'           : 1,\
    'gauss_null_chi_sq_thresh'      : 2.15593648,\
    'gauss_chi_sq_thresh'           : 1.41999996,\
    'gauss_power_thresh'            : 3,\
    'gauss_peak_power_thresh'       : 3.20000005,\
    'gauss_pot_length'              : 64,\
    'pulse_thresh'                  : 18.2443752,\
    'pulse_display_thresh'          : 0.5,\
    'pulse_max'                     : 40960,\
    'pulse_min'                     : 16,\
    'pulse_fft_max'                 : 8192,\
    'pulse_pot_length'              : 256,\
    'triplet_thresh'                : 7.2444005,\
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
    'chirps'                        : [chirp_parameter_t, chirp_parameter_t],
    'pulse_beams'                   : 1, \
    'max_signals'                   : 30, \
    'max_spikes'                    : 8, \
    'max_gaussians'                 : 0, \
    'max_pulses'                    : 0, \
    'max_triplets'                  : 0, \
    'keyuniq'                       : 7344400, \
    'credit_rate'                   : 2.8499999
}

"""
subband example
"""
subband_desc = {
    'number'        : 49,
    'center'        : 1420482788.0859,
    'base'          : 1420478515.625,
    'sample_rate'   : 9765.625
}
"""
group_info example
"""
group_info = {
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
workunit_header example
"""
workunit_header = {
    'name'          : '', \
    'group_info'    : group_info, \
    'subband_desc'  : subband_desc, \
    'sd_id'         : 0
}
