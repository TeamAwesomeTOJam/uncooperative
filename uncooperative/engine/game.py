'''
Created on May 2, 2013

@author: jonathan
'''

import os
import sys

import pygame

import componentmanager
from entitymanager import EntityManager
from resourcemanager import ResourceManager, LoadEntityDefinition, LoadImage

from input import InputEvent, InputManager

_game = None


class Game(object):
    
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500,500))
        
        self.component_manager = componentmanager.ComponentManager()
        self.entity_manager = EntityManager()
        
        self.resource_manager = ResourceManager(os.path.join(sys.path[0], 'res'))
        self.resource_manager.register_loader('definition', LoadEntityDefinition)
        self.resource_manager.register_loader('sprite', LoadImage)

        self.input_manager = InputManager()
        self.input_manager.init_joysticks()

        self.entities_to_update = []
        self.entities_to_input = []
        
    def register_for_updates(self, entity):
        self.entities_to_update.append(entity)
        
    def register_for_input(self, entity):
        self.entities_to_input.append(entity)
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                elif e.type == pygame.JOYAXISMOTION or \
                        e.type == pygame.JOYBALLMOTION or \
                        e.type == pygame.JOYBUTTONDOWN or \
                        e.type == pygame.JOYBUTTONUP or \
                        e.type == pygame.JOYHATMOTION or \
                        e.type == pygame.KEYDOWN or \
                        e.type == pygame.KEYUP:
                    event = InputEvent(e)
                    for entity in self.entities_to_input:
                        entity.handle('input', event)


            for entity in self.entities_to_update:
                entity.handle('update', dt)


def get_game():
    global _game
    if not _game:
        _game = Game()
    return _game
