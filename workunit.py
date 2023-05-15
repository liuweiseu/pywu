"""
class: xml
"""
class xml(object):
    nindent = 0
    def __init__(self,f,name):
        self.f = f
        self.name = name
        
        
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
                    i.print_xml()
                self.print_xml_end(k)
            elif(isinstance(v,xml)):
                self.print_xml_begin(k)
                v.print_xml()
                self.print_xml_end(k)
            else:
                self.print_xml_indent()
                print("<%s>%s</%s>"%(k, v, k), file=self.f)

    def print_xml_indent(self):
        print(' '*xml.nindent, file=self.f, end='')

    def print_xml(self):
        self.print_xml_begin(self.name)
        xml.nindent += 2
        self.print_xml_content(self.info)
        xml.nindent -= 2
        self.print_xml_end(self.name)


"""
class tape
"""
tape_info = {'name'             : '', \
             'start_time'       : '', \
             'last_block_time'  : '', \
             'last_block_done'  : '', \
             'missed'           : '', \
             'tape_quality'     : '', \
             'beam'             : ''}
class tape(xml):
    def __init__(self, f, name, tape_info):
        self.f = f
        self.name = name
        self.info = tape_info

"""
class data_description
""" 
data_desc = {'start_ra'         : '', \
             'start_dec'        : '', \
             'end_ra'           : '', \
             'end_dec'          : '', \
             'true_angle_range' : '', \
             'time_recorded'    : '', \
             'time_recorded_jd' : '', \
             'nsamples'         : '', \
             'coords'           : ''}
class data_description(xml):
    def __init__(self, f, name, data_desc):
        self.f =f
        self.name = name
        self.info = data_desc

"""
class coordinate
"""
coordinate_t = {'time'          : '', \
                'ra'            : '', \
                'dec'           : ''}
class coordinate(xml):
    def __init__(self, f, name, coordinate_t):
        self.f = f
        self.name = name
        self.info = coordinate_t

"""
class receiver_cfg
"""
class receiver(xml):
    def __init__(self, f, name, receiver_cfg):
        self.f = f
        self.name = name
        self.info = receiver_cfg