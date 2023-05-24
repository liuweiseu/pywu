"""
High-level module for users.
Most of the user should be able to get a workunit file by only using this module.
"""
from .wu_xml import xml_base
from .wu_dict import *
from .obs_config import *
import math

wu_header={
'workunit_header'   : dict(), \
'group_info'        : dict(), \
'tape_info'         : dict(), \
'data_desc'         : dict(), \
'receiver_cfg'      : dict(), \
'subband_desc'      : dict()
}

class wu_file(object):
    """
    Description:
        This is a high-level class for generating a workunit file.
        User should be able to get a workunit by using this class only.
    """
    def __init__(self, filename, info=workunit_grp):
        """
        Description:
            Create a wu_file object based on the name and info.
        Inputs:
            - tag(str): It's the tag name at the begining of the workunit.
                Default='workunit_group'
            - info(dict): It's a big dict contains all the info required by a workunit.
                By default, it uses the dict template in wu_dict.py.
                Default=workunit_grp
        """
        self.filename = filename
        self.wu_xml = xml_base(info=info)
       
    def init_header(self, info, coord, ch):
        """
        Description:
            Change workunit_header based on info, coord and ch.
        Inputs:
            - info(dict): information from raw data file name
                Default=None
            - coord(list or np.ndarray): coord info from redis_info.json
                Default=None
            - ch(int): channel number [0-255]
                Default=None
        """
        # the workunit name is: <source_filename>.<splitter_pid>.<data_start_block>.<receiver_s4_id>.<band_number>
        # TODO: splitter_pid and data_start_block may need to be chagned.
        fn                                           = info['fn']
        splitter_pid                                 = 0
        data_start_block                             = 0
        receiver_s4_id                               = 30 + info['beam']*2 + info['pol']
        band_number                                  = 0
        # workunit_header
        wu_header['workunit_header']['name']         = '%s.%d.%d.%d.%d'%(fn,                \
                                                                        splitter_pid,       \
                                                                        data_start_block,   \
                                                                        receiver_s4_id,     \
                                                                        band_number)
        # group_info
        wu_header['group_info']['name']              = '%s.%d.%d.%d'%(fn,                   \
                                                                        splitter_pid,       \
                                                                        data_start_block,   \
                                                                        receiver_s4_id,     )
        # tape_info
        wu_header['tape_info']['name']               = fn
        wu_header['tape_info']['beam']               = info['beam'] * 2 + info['pol']
        wu_header['tape_info']['start_time']         = coord[0]['time']
        wu_header['tape_info']['last_block_time']    = coord[0]['time']
        # data_desc
        wu_header['data_desc']['start_ra']           = coord[0]['ra']
        wu_header['data_desc']['start_dec']          = coord[0]['dec']
        wu_header['data_desc']['end_ra']             = coord[-1]['ra']
        wu_header['data_desc']['end_dec']            = coord[-1]['dec']
        wu_header['data_desc']['coords']              = coord

        wu_header['data_desc']['true_angle_range']   = math.sqrt((float(coord[0]['ra']) - float(coord[-1]['ra']))**2 + \
                                                       (float(coord[0]['dec']) - float(coord[-1]['dec']))**2)
        wu_header['data_desc']['time_recorded']      = info['time_recorded']
        wu_header['data_desc']['time_recorded_jd']   = info['time_recorded_jd']
        # receiver_cfg
        wu_header['receiver_cfg']['s4_id']           = receiver_s4_id
        wu_header['receiver_cfg']['name']            = "FAST %s MultiBeam, Beam %s, Pol %s"%( \
                                                        info['band'], info['beam'], info['pol'])
        # subband_desc
        ch_center_freq = LO + FS/FFT_POINT*ch
        wu_header['subband_desc']['number']          = ch
        wu_header['subband_desc']['center']          = ch_center_freq * 10**6
        wu_header['subband_desc']['base']            = ch_center_freq * 10**6
        ### create wu_header
        for key in wu_header:
            for subkey in wu_header[key]:
                eval(key)[subkey] = wu_header[key][subkey] 

    def set_data(self, d):
        """
        Description:
            Write data into the workunit_group.
        Inputs:
            - d(np.ndarray):
        """
        wu_data['values'] = d
        wu_data['length'] = len(d) * BYTES_PER_SAMPLE + 2
        data_desc['nsamples'] = len(d)


    def gen(self):
        f = open(self.filename, 'w')
        self.wu_xml.print_xml(f)
        f.close()