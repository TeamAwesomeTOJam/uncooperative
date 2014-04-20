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
from resourcemanager import ResourceManager, LoadEntityData, LoadImage, LoadInputMapping, LoadSound
from component import (MovementComponent,
                       ExampleComponent, 
                       InputMovementComponent, 
                       DrawComponent, 
                       PlayerCollisionComponent,
                       ZombieAIComponent,
                       CarComponent,
                       DrawHitBoxComponent,
                       AttackComponent,
                       ItemComponent,
                       InputActionComponent,
                       DeadComponent,
                       ZombieCollisionComponent)

from render import Render
from input import InputManager
from random import randint


_game = None


class Game(object):
    
    def __init__(self):
        self.screen_size = (1280,720)
        self.map_size = (128,128)
        self.tile_size = (32,32)
        self.world_size = (self.tile_size[0] * self.map_size[0], self.tile_size[1] * self.map_size[1])
        self.world_rooms = (8,8)

        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        
        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_component('MovementComponent', MovementComponent())
        self.component_manager.register_component('ExampleComponent', ExampleComponent())
        self.component_manager.register_component('AnimationComponent', AnimationComponent())
        self.component_manager.register_component('DrawComponent', DrawComponent())
        self.component_manager.register_component('InputMovementComponent', InputMovementComponent())
        self.component_manager.register_component('PlayerCollisionComponent', PlayerCollisionComponent())
        self.component_manager.register_component('ZombieAIComponent', ZombieAIComponent())
        self.component_manager.register_component('ZombieAIComponent', ZombieAIComponent())
        self.component_manager.register_component('CarComponent', CarComponent())
        self.component_manager.register_component('DrawHitBoxComponent', DrawHitBoxComponent()) 
        self.component_manager.register_component('AttackComponent', AttackComponent())
        self.component_manager.register_component('ItemComponent', ItemComponent())
        self.component_manager.register_component('InputActionComponent', InputActionComponent())
        self.component_manager.register_component('DeadComponent', DeadComponent())
        self.component_manager.register_component('ZombieCollisionComponent', ZombieCollisionComponent())
        
        self.entity_manager = EntityManager()
        
        if getattr(sys, 'frozen', None):
            basedir = sys._MEIPASS
        else:
            basedir = sys.path[0]
            
        self.resource_manager = ResourceManager(os.path.join(basedir, 'res'))
        self.resource_manager.register_loader('definition', LoadEntityData)
        self.resource_manager.register_loader('sprite', LoadImage)
        self.resource_manager.register_loader('inputmap', LoadInputMapping)
        self.resource_manager.register_loader('sound', LoadSound)

        self.input_manager = InputManager()
        self.input_manager.init_joysticks()
        
        self.mode = 'splash'
        
    def run(self):
        #pygame.display.toggle_fullscreen()
        self.music = self.resource_manager.get('sound', 'Teamawesome_zombies_LOOP.wav')
        self.music.play(loops=-1)
        self.entity_manager.add_entity(Entity('car'))
        for e in [Entity('character1'), Entity('character2'), Entity('character3'), Entity('character4')]:
            self.entity_manager.add_entity(e)
        self.item_names = ["engine", "gas-can", "radiator", "steering-wheel-2", "tire", "steering-wheel", "toolbox", "tire", "tire", "tire"]

        for i in self.item_names:
            x_pos = (self.world_size[0]/self.world_rooms[0] * randint(0, self.world_rooms[0]-1)) + self.world_size[0]/self.world_rooms[0]/2
            y_pos = (self.world_size[1]/self.world_rooms[1] * randint(0, self.world_rooms[1]-1)) + self.world_size[1]/self.world_rooms[1]/2
            self.entity_manager.add_entity(Entity(i, x=x_pos, y=y_pos))
        
        self.entity_manager.add_entity(Entity('splashscreen'))
        self.screen.blit(self.resource_manager.get('sprite', self.entity_manager.get_by_name('splashscreen').image),(0,0))
        pygame.display.flip()
        self.renderer = Render(self)

        self.zombies = []
        for _ in range(50):
            x_pos = (self.world_size[0]/self.world_rooms[0] * randint(0, self.world_rooms[0]-1)) + self.world_size[0]/self.world_rooms[0]/2
            y_pos = (self.world_size[1]/self.world_rooms[1] * randint(0, self.world_rooms[1]-1)) + self.world_size[1]/self.world_rooms[1]/2
            self.entity_manager.add_entity(Entity("zombie", x=x_pos, y=y_pos))

        while True:
            dt = self.clock.tick(60) / 1000.0

            if self.mode=='game':
                events = self.input_manager.process_events()
                for event in events:
                    if event.target == 'GAME':
                        if event.action == 'QUIT' and event.value > 0:
                            sys.exit()
                        elif event.action == 'FULLSCREEN' and event.value > 0:
                            pygame.display.toggle_fullscreen()
                        elif event.action == 'RELOAD' and event.value > 0:
                            self.resource_manager.clear()
                    else:
                        for entity in self.entity_manager.get_by_tag('input'):
                            entity.handle('input', event)  

                entities_in_view = set()
                for view in self.renderer.views:
                    entities_in_view.update(view.entities_in_view())
                    
                for entity in (entities_in_view & self.entity_manager.get_by_tag('update')) | self.entity_manager.get_by_tag('item') | {self.entity_manager.get_by_name('car')}:
                    entity.handle('update', dt)

                self.renderer.render()
                
            elif self.mode == 'splash':
                for e in pygame.event.get():
                    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): sys.exit()
                    if e.type == pygame.KEYDOWN:
                        self.mode = 'game'
                self.entity_manager.get_by_name('splashscreen').handle('update', dt)
                self.screen.blit(self.resource_manager.get('sprite', self.entity_manager.get_by_name('splashscreen').image), (0,0))
                pygame.display.flip()
                
            pygame.display.set_caption('fps: ' + str(self.clock.get_fps()))


def get_game():
    global _game
    if not _game:
        _game = Game()
    return _game
