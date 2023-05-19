# Software for FAST reobs project
This python package is used for converting raw PFB data to workunit, which can be processed by setiathome client.  
## Getting start
1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)(optional)  
Miniconda is recommended to create a vritual python environment, so that it won't mess up the python environment on your system.  
If miniconda is installed, please create and activate the python environment.
    ```
    conda create -n wu_env python=3.9
    conda activate wu_env
    ``` 
2. clone the repository
    ```
    git clone https://github.com/liuweiseu/pywu.git
    ```
3. install numpy
    ```
    pip install numpy
    ```
   **Note**: This is because numpy can't be installed automatically, even though it's in the install_requires list.
4. install the package
    ```
    cd pywu
    pip install .
    ```
    **Note:** The packeage is tested under python3.9.16. It should work under python3.x. 
# Introduction
There are four modules in the package:  
* wu_file : This is a high-level module for generating workunit files, which should be used by most of the users. It calls the following modules to generate workunit files.
* wu_io : three are two classes in this module  
    * dfile() : parse the raw data file, read PFB data from the file.
    * redis_info() : load json file, which contains coord information by time, and get coord from the json file.
* wu_xml : It contains several classes to print out data in xml-like format.  
    * xml_base() : generate output in the standard xml format.
    * xml_coeff() : genetate coeff in a workunit.
    * xml_data() : generate data in a workunit.
* wu_dict : It contains a template dict of a workunit file. What we need to do is fill the content into this dict.  
**Note:** Before loading `redis_info.json`, you need to add '[' and ']' at the beginning and end of the file, you also need to replace '}{' with '},{' in the .json file.
# Examples 
* Here is an example about how to use this package:
    ```python
    import pywu

    # open data file
    f = pywu.io.dfile('../data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat')
    info = f.dparse()
    t = info['timestamp']
    beam = info['beam']
    start_t = info['timestamp']
    beam = info['beam']
    # get metadata from redis_info.json
    r = pywu.io.redis_info('../data_example/redis_info.json')
    # seek coord from redis, and read data from the data file
    # we only get 2 seconds of data for test
    nsec = 2
    coord = r.seekcoord(beam, start_t, nsec)
    d = f.dread(nsec)
    # generate workunit for channel 0
    ch = 0
    wu = pywu.wu_file('workunit_example.sah')
    wu.init_header(info, coord, ch)
    wu.set_data(d[ch])
    wu.gen()
    ```
    You can get more detail about the example [here](https://github.com/liuweiseu/pywu/blob/master/examples). Please use `./workunit_generator.py -h` to get more information about it.  
* Modify workunit header   
The workunit header is generated from a template [here](https://github.com/liuweiseu/pywu/blob/master/pywu/wu_dict.py).  
Sometimes, you may want to change metadata in workunit header, you can refer the following code to change any metadata you want:
    ```python
    wu.init_header(info, coord, ch)
    wu.set_data(d[ch])
    # change the tape_info name to 'tape_info_test'.
    pywu.tape_info['name'] = 'tape_info_test'
    wu.gen()
    ```
    After you generate the workunit file, you should be able to see the name in tape_info changed:
    ```xml
    <tape_info>
        <name>tape_info_test</name>
        ...
    ```