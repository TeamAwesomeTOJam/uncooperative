'''
Created on May 3, 2013

@author: jonathan
'''

import json
import os

import pygame


class ResourceManager(object):
    
    def __init__(self, prefix):
        self.prefix = prefix
        self.loaders = {}
        self.cache = {}
    
    def register_loader(self, res_type, loader):
        self.loaders[res_type] = loader
    
    def get(self, res_type, key):
        try:
            return self.cache[(res_type, key)]
        except KeyError:
            value = self.loaders[res_type](self.prefix, key)
            self.cache[(res_type, key)] = value
            return value
    
    def clear(self):
        self.cache = {}
        
        
def LoadEntityDefinition(prefix, key):
    with open(os.path.join(prefix, 'definitions', key + '.json')) as in_file:
        definition = json.load(in_file)
    for required_key in ['properties', 'components']:
        if required_key not in definition:
            raise KeyError("Definitions must have a '%s' property, but this one doesn't" % (required_key,))
    return definition
    
def LoadImage(prefix, key):
    image_surface = pygame.image.load(os.path.join(prefix, 'sprites', key))
    image_surface.convert()
    #image_surface.set_colorkey((255, 0, 255))
    return image_surface

def LoadInputMapping(prefix, key):
    with open(os.path.join(prefix, 'definitions', 'keymapping.json')) as in_file:
        definition = json.load(in_file)
        
    return definition['input']