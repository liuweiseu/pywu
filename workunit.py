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
                    #ins = xml(k,v)
                    i.print_xml(self.f)
                self.print_xml_end(k)
            elif(isinstance(v,dict)):
                ins = xml(k,v)
                self.print_xml_begin(k)
                ins.print_xml(self.f)
                self.print_xml_end(k)
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
    'az_corr_coeff' : -37, \
    'zen_corr_coeff': -57, \
    'array_az_ellipse' : 329.06, \
    'array_za_ellipse' : 384.005, \
    'array_angle'   : -60
}


"""
group_info example
"""
group_info = {
    'tape_info'     : tape_info, \
    'name'          : '', \
    'data_desc'     : data_desc
}
"""
workunit_header example
"""
workunit_header = {
    'name' : '', \
    'group_info' : group_info
}
