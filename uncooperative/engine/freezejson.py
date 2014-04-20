'''
Created on Dec 1, 2013

@author: jonathan
'''

import collections


def freeze_value(value):
    if isinstance(value, dict):
        return _freeze_object(value)
    elif isinstance(value, list):
        return _freeze_array(value)
    elif isinstance(value, unicode):
        return value.encode('ascii', 'ignore')
    else:
        return value
    
def _freeze_object(obj):
    for key, value in obj.items():
        obj[key] = freeze_value(value)

    named_tuple = collections.namedtuple('object', obj.keys())
    return named_tuple(**obj)

def _freeze_array(array):
    for index, value in enumerate(array):
        array[index] = freeze_value(value)
        
    return tuple(array)