import numpy as np

# add dict item to the np.ndarray
#
def add_to_list(l,item):
    if(not isinstance(l,np.ndarray)):
        l = np.array(l)
    if(isinstance(item, dict)):
        return np.append(l, item)
    elif(isinstance(item, list) or isinstance(item, np.ndarray)):
        for i in item:
            l = np.append(l,i)
        return l