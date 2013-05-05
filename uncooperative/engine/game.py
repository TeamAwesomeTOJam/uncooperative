'''
Created on May 2, 2013

@author: jonathan
'''

import os
import sys

import pygame

import componentmanager
from entitymanager import EntityManager
from entity import Entity
from animation import AnimationComponent
from resourcemanager import ResourceManager, LoadEntityDefinition, LoadImage, LoadInputMapping
from component import (MovementComponent,
                       ExampleComponent, 
                       InputMovementComponent, 
                       DrawComponent, 
                       PlayerCollisionComponent,
                       ZombieAIComponent,)

from collision import CollisionGrid

from render import Render
from input import InputEvent, InputManager

from random import randint

_game = None
from gridgen import GridGenerator
from grid import Grid,Vec2


class Game(object):
    
    def __init__(self):
        self.screen_size = (500,500)
        self.map_size = (128,128)
        self.tile_size = (32,32)
        self.world_size = (self.tile_size[0] * self.map_size[0], self.tile_size[1] * self.map_size[1])
        
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500,500))
        
        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_component('MovementComponent', MovementComponent())
        self.component_manager.register_component('ExampleComponent', ExampleComponent())
        self.component_manager.register_component('AnimationComponent', AnimationComponent())
        self.component_manager.register_component('DrawComponent', DrawComponent())
        self.component_manager.register_component('InputMovementComponent', InputMovementComponent())
        self.component_manager.register_component('PlayerCollisionComponent', PlayerCollisionComponent())
        self.component_manager.register_component('ZombieAIComponent', ZombieAIComponent())

        self.entity_manager = EntityManager()
        
        self.resource_manager = ResourceManager(os.path.join(sys.path[0], 'res'))
        self.resource_manager.register_loader('definition', LoadEntityDefinition)
        self.resource_manager.register_loader('sprite', LoadImage)
        self.resource_manager.register_loader('inputmap', LoadInputMapping)

        self.input_manager = InputManager()
        self.input_manager.init_joysticks()

        self.collision_grid = CollisionGrid(64)

        self.entities_to_update = set()
        self.entities_to_input = set()
        
        
    def register_for_updates(self, entity):
        self.entities_to_update.add(entity)
        
    def register_for_input(self, entity):
        self.entities_to_input.add(entity)
        
    def run(self):
        #chars = Entity('character1'), Entity('character2'), Entity('character3'), Entity('character4')
        self.characters = [Entity('character1'), Entity('character2'), Entity('character3'), Entity('character4')]
        self.renderer = Render(self)
        zombies = [Entity("zombie",properties={"x":randint(0,self.world_size[0]),"y":randint(0,self.world_size[1])}) for m in range(20)]
        self.zombies = [Entity("zombie")]
        for z in self.zombies:
            self.collision_grid.add_entity(z)
        for c in self.characters:
            self.collision_grid.add_entity(c)

        for tile in self.renderer.tiles:
            if not tile.props.passable:
                self.collision_grid.add_entity(tile)

        self.current_camera = 0
        while True:
            dt = self.clock.tick() / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                
                if e.type == pygame.JOYAXISMOTION or \
                        e.type == pygame.JOYBALLMOTION or \
                        e.type == pygame.JOYBUTTONDOWN or \
                        e.type == pygame.JOYBUTTONUP or \
                        e.type == pygame.JOYHATMOTION or \
                        e.type == pygame.KEYDOWN or \
                        e.type == pygame.KEYUP:
                    event = InputEvent(e)

                    for entity in self.entities_to_input:
                        if event.action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                            entity.handle('move', event)
                        else:
                            entity.handle('input', event)

            
            for entity in self.entities_to_update:
                entity.handle('update', dt)
            self.renderer.render()

def get_game():
    global _game
    if not _game:
        _game = Game()
    return _game
