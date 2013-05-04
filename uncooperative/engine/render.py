#from OpenGL import *;

import pygame
from random import randint
from camera import Camera
from gridgen import GridGenerator
from entity import Entity


class Render:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.tile_size = game.tile_size
        self.map_size = game.map_size
        self.screen_size = game.screen_size
        self.world_size = game.world_size
        self.world_surface = pygame.Surface(self.world_size)
        self.grid = GridGenerator(self.map_size).genMap()
        
        self.tiles = []
        
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                if self.grid[x][y]:
                    #impassible
                    tile = Entity('impassabletile',{'x':x*self.tile_size[0],'y':y*self.tile_size[1]})
                else:
                    #passable
                    tile = Entity('passabletile',{'x':x*self.tile_size[0],'y':y*self.tile_size[1]})
                self.tiles.append(tile)
        
        for t in self.tiles:
            t.handle('draw-tiles',self.world_surface)

        pygame.image.save(self.world_surface,"file.png")

        self.cameras = [Camera(p) for p in self.game.characters]
#        self.cameras = [Camera(500,500) for m in xrange(4)]
        self.draw_surface = self.world_surface.copy()


    def render(self):
        offx = int(self.screen_size[0] / 2)
        offy = int(self.screen_size[1] / 2)
        rect = pygame.Rect(0,0,offx,offy)
        rect.center = self.cameras[0].pos()
        self.screen.blit(self.draw_surface,(0,0),rect)
        rect.center = self.cameras[1].pos()
        self.screen.blit(self.draw_surface,(offx,0),rect)
        rect.center = self.cameras[2].pos()
        self.screen.blit(self.draw_surface,(0,offy),rect)
        rect.center = self.cameras[3].pos()
        self.screen.blit(self.draw_surface,(offx,offy),rect)
        pygame.display.flip()
        self.draw_surface = self.world_surface.copy()


