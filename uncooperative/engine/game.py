'''
Created on May 2, 2013

@author: jonathan
'''

import os
import sys

import pygame

import componentmanager
from entitymanager import EntityManager
from resourcemanager import ResourceManager

_game = None


class Game(object):
    
    def __init__(self):
        global _game 
        _game = self

        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500,500))
        
        self.component_manager = componentmanager.ComponentManager()
        self.entity_manager = EntityManager()
        self.resource_manager = ResourceManager(os.path.join(sys.path[0], 'res'))
        
        self.entities_to_update = []
        
    def register_for_updates(self, entity):
        self.entities_to_update.append(entity)
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000.0
            for e in pygame.event.get():
                 if e.type == pygame.QUIT: sys.exit()
            for entity in self.entities_to_update:
                entity.handle('update', dt)


def get_game():
    global _game
    if not _game:
        _game = Game()
    return _game