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
from camera import Camera
from entity import Entity

from input import InputEvent, InputManager

_game = None


class Game(object):
    
    def __init__(self):
        self.screen_size = (500,500)
        self.world_size = (5000,5000)
        
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500,500))
        
        self.component_manager = componentmanager.ComponentManager()
        self.entity_manager = EntityManager()
        self.resource_manager = ResourceManager(os.path.join(sys.path[0], 'res'))
        self.input_manager = InputManager()
        self.input_manager.init_joysticks()
        
        self.entities_to_update = []
        self.entities_to_input = []
        
        self.camera_entity = Entity('camera')
        
        self.camera1 = Entity('camera')
        self.camera2 = Entity('camera')
        self.camera3 = Entity('camera')
        self.camera4 = Entity('camera')
        
        self.cameras = [self.camera1,self.camera2,self.camera3, self.camera4]
        self.current_camera = 0
        
        self.world_surface = pygame.Surface(self.world_size)
        for x in range(0,self.world_size[0],10):
            for y in range(0,self.world_size[1],10):
                pygame.draw.rect(self.world_surface,(255,0,0),(x,y,5,5))
        
    def register_for_updates(self, entity):
        self.entities_to_update.append(entity)
        
    def register_for_input(self, entity):
        self.entities_to_input.append(entities)
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_TAB:
                        self.current_camera = (self.current_camera +1)%4
                    if e.key == pygame.K_a:
                        self.cameras[self.current_camera].props.dx = 1
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_a:
                        self.cameras[self.current_camera].props.dx = 1
                if e.type == pygame.JOYAXISMOTION or \
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
            
            for i in range(4):
                if self.camera_dirs[i]:
                    self.cameras[i].x += 1
            rect = pygame.Rect(0,0,250,250)
            rect.center = (self.camera1.props.x,self.camera1.props.y)
            self.screen.blit(self.world_surface,(0,0),rect)
            rect.center = (self.camera2.props.x,self.camera2.props.y)
            self.screen.blit(self.world_surface,(250,0),rect)
            rect.center = (self.camera3.props.x,self.camera3.props.y)
            self.screen.blit(self.world_surface,(0,250),rect)
            rect.center = (self.camera4.props.x,self.camera4.props.y)
            self.screen.blit(self.world_surface,(250,250),rect)
            pygame.display.flip()


def get_game():
    global _game
    if not _game:
        _game = Game()
    return _game
