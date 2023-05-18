#! /usr/bin/env python
"""
This is used for testing wu_xml
"""
import sys, os
import numpy as np

sys.path.insert(0, '../pywu/')

from util    import add_to_list
from wu_xml  import xml_base, xml_coeff
from wu_xml  import tape_info
from wu_xml  import data_desc
from wu_xml  import coordinate_t
from wu_xml  import az_corr_coeff
from wu_xml  import zen_corr_coeff
from wu_xml  import receiver_cfg
from wu_xml  import recorder_cfg
from wu_xml  import splitter_cfg
from wu_xml  import chirp_parameter
from wu_xml  import analysis_cfg
from wu_xml  import subband_desc
from wu_xml  import group_info
from wu_xml  import workunit_header
from wu_xml  import data
from wu_xml  import workunit_grp

if __name__ == '__main__':
    # create a workunit file
    f = open('workunit_template.sah','w')
    # create coordinate_ins
    coordinate_arr = []
    coordinate_arr = add_to_list(coordinate_arr, coordinate_t)
    coordinate_arr = add_to_list(coordinate_arr, coordinate_t)
    coordinate_arr = add_to_list(coordinate_arr, [coordinate_t, coordinate_t])
    data_desc['coords'] = coordinate_arr
    # create corr coeff
    az_corr_coeff_arr = []
    az_corr_coeff_arr = add_to_list(az_corr_coeff_arr, az_corr_coeff)
    zen_corr_coeff_arr = []
    zen_corr_coeff_arr = add_to_list(zen_corr_coeff_arr, zen_corr_coeff)
    receiver_cfg['az_corr_coeff'] = az_corr_coeff_arr
    receiver_cfg['zen_corr_coeff'] = zen_corr_coeff_arr
    # create chirp_parameter
    chirp_parameter_arr = []
    chirp_parameter_arr = add_to_list(chirp_parameter_arr, [chirp_parameter, chirp_parameter])
    analysis_cfg['chirps'] = chirp_parameter_arr
    # create workunit group
    workunit_grp_ins = xml_base('workunit_grp', workunit_grp)
    workunit_grp_ins.print_xml(f)
    f.close()