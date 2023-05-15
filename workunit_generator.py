import sys, os

sys.path.insert(0, './')

from workunit import tape


if __name__ == '__main__':
    with open('test.sah','w') as f:
        tape_info = tape(f, 'test', 2454822.5698634, \
                                2454822.5698634, \
                                6208, \
                                0, \
                                0, \
                                8)
        tape_info.print_xml()
    