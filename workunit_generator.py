import sys, os

sys.path.insert(0, './')

from workunit import tape, tape_info
from workunit import data_description, data_desc
from workunit import coordinate, coordinate_t

if __name__ == '__main__':
    f = open('test.sah','w')
    tape_info = {'name'             : 'test', \
             'start_time'       : 2454822.5698634, \
             'last_block_time'  : 2454822.5698634, \
             'last_block_done'  : 6280, \
             'missed'           : 0, \
             'tape_quality'     : 0,
             'beam'             : 8}
    coordinate_t = {'time'      : 2454822.5698622, \
                'ra'            : 3.2887318938763, \
                'dec'           : 23.410418247457}
    coordinate_ins = coordinate(f, 'coordinate_t', coordinate_t)
    data_desc =  {'start_ra'         : 3.2887318938763, \
             'start_dec'        : 23.410418247457, \
             'end_ra'           : 3.3185884614727, \
             'end_dec'          : 26.095076667942, \
             'true_angle_range' : 2.7152905955851, \
             'time_recorded'    : 'Mon Dec 22 01:40:36 2008', \
             'time_recorded_jd' : 2454822.5698622, \
             'nsamples'         : 1048576, \
             'coords'           : [coordinate_ins,coordinate_ins]}

    tape_info_ins = tape(f, 'tape_info',tape_info)
    tape_info_ins.print_xml()
    data_desc_ins = data_description(f, 'data_desc', data_desc)
    data_desc_ins.print_xml()

    f.close()