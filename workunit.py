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
    
    def print_xml_content(self,name, content):
        self.print_xml_indent()
        print("<%s>%s</%s>"%(name, content, name), file=self.f)

    def print_xml_indent(self):
        print(' '*xml.nindent, file=self.f, end='')

class tape(xml):
    def __init__(self, f, name, start_time, \
                 last_block_time, last_block_done, \
                 missed, tape_quality, beam):
        self.f = f
        self.name = name
        self.start_time = start_time
        self.last_block_time = last_block_time
        self.last_block_done = last_block_done
        self.missed = missed
        self.tape_quality = tape_quality
        self.beam = beam
    
    def print_xml(self):
        self.print_xml_begin('tape_info')
        xml.nindent += 2
        self.print_xml_content('start_time',str(self.start_time))
        self.print_xml_content('last_block_time',str(self.last_block_time))
        self.print_xml_content('last_block_done',str(self.last_block_done))
        self.print_xml_content('missed', self.missed)
        self.print_xml_content('tape_quality', self.tape_quality)
        self.print_xml_content('beam', self.beam)
        xml.nindent -= 2
        self.print_xml_end('tape_info')

 
class data_description(xml):
    def __init__(self, f, start_ra, start_dec, \
                          end_ra, end_dec, \
                          true_angle_range, \
                          time_recorded, \
                          time_recorded_jd, \
                          nsamples, \
                          coords):
        self.start_ra = start_ra
        self.start_dec = start_dec
        self.true_angle_range = true_angle_range
        self.time_recorded = time_recorded
        self.time_recorded_jd = time_recorded_jd
        self.nsamples = nsamples
        self.coords = coords
    
    def print_xml(self):
        self.print_xml_begin('data_desc')
        xml.nindent += 2
        
