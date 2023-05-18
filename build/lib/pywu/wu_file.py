from .wu_xml import xml_base
from .wu_dict import *

header={
'tape_info'         : dict(), \
'data_desc'         : dict(), \
'receiver_cfg'      : dict(), \
'subband_desc'      : dict()
}

class wu_file(object):
    def __init__(self, filename, info=workunit_grp, name='workunit_group'):
        self.filename = filename
        self.wu_xml = xml_base(info=info, name=name)
    
    def gen(self):
        f = open(self.filename, 'w')
        self.wu_xml.print_xml(f)
        f.close()
    
    def init_header(self, info, coord, ch):
        # tape_info
        header['tape_info']['beam']               = info['beam'] * 2 + info['pol']
        # data_desc
        header['data_desc']['start_ra']           = coord[0]['ra']
        header['data_desc']['start_dec']          = coord[0]['dec']
        header['data_desc']['end_ra']             = coord[-1]['ra']
        header['data_desc']['end_dec']            = coord[-1]['dec']
        header['data_desc']['coord']              = coord
        # TODO: calculate true_angle_range
        header['data_desc']['true_angle_range']   = 0 
        header['data_desc']['time_recorded']      = info['time_recorded']
        header['data_desc']['time_recorded_jd']   = info['time_recorded_jd']
        # receiver_cfg
        # TODO: check the s4_id with Eric
        header['receiver_cfg']['s4_id']           = info['beam']
        header['receiver_cfg']['name']            = "FAST %s MultiBeam, Beam %s, Pol %s"%( \
                                                    info['band'], \
                                                    info['beam'], \
                                                    info['pol'])
        # TODO: ask zhenzhao for the FAST info
        header['receiver_cfg']['beam_width']      = 0
        header['receiver_cfg']['center_freq']     = 1250
        header['receiver_cfg']['latitude']        = 0
        header['receiver_cfg']['longitude']       = 0
        header['receiver_cfg']['elevation']       = 0
        header['receiver_cfg']['diameter']        = 0
        header['receiver_cfg']['az_orientation']  = 0
        # subband_desc
        #TODO: double check the following info
        header['subband_desc']['number']          = ch
        header['subband_desc']['center']          = 0
        header['subband_desc']['base']            = 0
        ### create wu_header
        for key in header:
            for subkey in header[key]:
                eval(key)[subkey] = header[key][subkey] 

    def set_data(self, d):
        data['values'] = d