'''
Created on May 2, 2013

@author: jonathan
'''

import os
import sys

from componentmanager import ComponentManager
from entitymanager import EntityManager
from resourcemanager import ResourceManager

_game = None


class Game(object):
    
    def __init__(self):
        global _game 
        _game = self

        self.component_manager = ComponentManager()
        self.entity_manager = EntityManager()
        self.resource_manager = ResourceManager(os.path.join(sys.path[0], 'res'))
        
        self.entities_to_update = []
        
    def register_for_updates(self, entity):
        self.entities_to_update.append(entity)
        
    def run(self):
        while True:
            for entity in self.entities_to_update:
                entity.handle('update', 1)


def get_game():
    return _game