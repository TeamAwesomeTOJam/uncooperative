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
    with open(os.path.join(prefix, 'defintions', key + '.json')) as in_file:
        return json.load(in_file)
    
def LoadImage(prefix, key):
    image_surface = pygame.image.load(os.path.join('data', 'bla.png'))
    image_surface.convert()
    return image_surface
