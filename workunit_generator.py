#! /usr/bin/env python

import sys, os
from datetime import datetime
sys.path.insert(0, './pywu')

from util import add_to_list
from wu_io import dfile,redis_info
from wu_xml import xml_base, xml_coeff
from wu_xml import tape_info
from wu_xml import data_desc
from wu_xml import coordinate_t
from wu_xml import az_corr_coeff
from wu_xml import zen_corr_coeff
from wu_xml import receiver_cfg
from wu_xml import recorder_cfg
from wu_xml import splitter_cfg
from wu_xml import chirp_parameter
from wu_xml import analysis_cfg
from wu_xml import subband_desc
from wu_xml import group_info
from wu_xml import workunit_header
from wu_xml import data
from wu_xml import workunit_grp

def create_header(info, coord):
    header={}
    # tape_info
    header['tape_info']['beam']               = int(info['beam']) * 2 + int(info['pol'])
    # data_desc
    header['data_desc']['start_ra']           = coord[0]['ra']
    header['data_desc']['start_dec']          = coord[0]['dec']
    header['data_desc']['end_ra']             = coord[-1]['ra']
    header['data_desc']['end_dec']            = coord[-1]['dec']
    # TODO: calculate true_angle_range
    header['data_desc']['true_angle_range']   = 0 
    header['data_desc']['time_recorded']      = info['time_recorded']
    header['data_desc']['time_recorded_jd']   = info['time_recorded_jd']
    # receiver_cfg
    # TODO: check the s4_id with Eric
    header['receiver_cfg']['s4_id']           = info['beam']
    header['receiver_cfg']['name']            = "Arecibo %s MultiBeam, Beam %s, Pol %s"%( \
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

def init_wu_header(metadata):
    pass

def main():
    # open data file
    f = dfile('data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat')
    # get metadata from redis_info.json
    r = redis_info('data_example/redis_info_20230511.json')
    coord = r.seekcood(0,f.info['timestamp'], 6)
    # create a wu_xml file
    f = open('workunit.sah','w')
    # create coordinate_ins
    data_desc['coords'] = coord
    # create workunit
    workunit_grp_ins = xml_base('workunit_group', workunit_grp)
    workunit_grp_ins.print_xml(f)
    f.close()

if __name__ == '__main__':
    main()