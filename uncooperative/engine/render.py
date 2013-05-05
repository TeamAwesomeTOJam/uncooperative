#from OpenGL import *;

import pygame
from random import randint
from camera import Camera
from gridgen import GridGenerator
from entity import Entity
from vec2d import Vec2d

class Render:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.tile_size = game.tile_size
        self.map_size = game.map_size
        self.screen_size = game.screen_size
        self.world_size = game.world_size
        self.world_surface = pygame.Surface(self.world_size)
        self.world_surface.convert()
        self.grid = GridGenerator(self.map_size).genMap()
        
        self.tiles = []
        
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                if self.grid[x][y]:
                    up = self.grid[x][(y-1) % self.map_size[1]]
                    down = self.grid[x][(y+1) % self.map_size[1]]
                    left = self.grid[(x-1)% self.map_size[0]][y]
                    right = self.grid[(x+1)% self.map_size[0]][y]
                    type = 'impassabletileA'
                    if up and down and left and right:
                        upleft = self.grid[(x-1)% self.map_size[0]][(y-1)% self.map_size[1]]
                        upright = self.grid[(x+1)% self.map_size[0]][(y-1)% self.map_size[1]]
                        downleft = self.grid[(x-1)% self.map_size[0]][(y+1)% self.map_size[1]]
                        downright = self.grid[(x+1)% self.map_size[0]][(y+1)% self.map_size[1]]
                        if not upleft:
                            type = 'impassabletileBR'
                        elif not upright:
                            type = 'impassabletileBL'
                        elif not downleft:
                            type = 'impassabletileTR'
                        elif not downright:
                            type = 'impassabletileTL'
                        else:
                            type = 'impassabletileA'
                    elif up and down and left and not right:
                        type = 'impassabletileL'
                    elif up and down and not left and right:
                        type = 'impassabletileR'
                    elif up and down and not left and not right:
                        type = 'impassabletileCV'
                    elif up and not down and left and right:
                        type = 'impassabletileT'
                    elif up and not down and left and not right:
                        type = 'impassabletileCBR'
                    elif up and not down and not left and right:
                        type = 'impassabletileCBL'
                    elif up and not down and not left and not right:
                        type = 'impassabletileCT'
                    elif not up and down and left and right:
                        type = 'impassabletileB'
                    elif not up and down and left and not right:
                        type = 'impassabletileCTR'
                    elif not up and down and not left and right:
                        type = 'impassabletileCTL'
                    elif not up and down and not left and not right:
                        type = 'impassabletileCB'
                    elif not up and not down and left and right:
                        type = 'impassabletileCH'
                    elif not up and not down and left and not right:
                        type = 'impassabletileCR'
                    elif not up and not down and not left and right:
                        type = 'impassabletileCL'
                    elif not up and not down and not left and not right:
                        type = 'impassabletileC'
                    tile = Entity(type,{'x':x*self.tile_size[0],'y':y*self.tile_size[1]})
                else:
                    #passable
                    tile = Entity('passabletile',{'x':x*self.tile_size[0],'y':y*self.tile_size[1]})
                self.tiles.append(tile)
        
        for t in self.tiles:
            t.handle('draw', self.world_surface)

        pygame.image.save(self.world_surface,"file.png")
        self.minimap_scale = 0.025
        self.minimap_size = Vec2d(int(self.minimap_scale*self.world_size[0]),int(self.minimap_scale*self.world_size[1]))
        self.minimap = pygame.transform.scale(self.world_surface,self.minimap_size)

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
        
        
        #draw the HUD
        
        for player in range(4):
            offset = Vec2d(0,0)
            if player == 0:
                offset = Vec2d(0,0)
            elif player == 1:
                offset = Vec2d(self.screen_size[0]/2,0)
            elif player == 2:
                offset = Vec2d(0,self.screen_size[1]/2)
            elif player == 3:
                offset = Vec2d(self.screen_size[0]/2,self.screen_size[1]/2)
            width = self.screen_size[0]/2
            height = self.screen_size[1]/2
            
            rect = pygame.Rect(offset,(width,height))
            pygame.draw.rect(self.screen,(255,255,255),rect,3)
            
            player_pos = Vec2d(self.game.characters[player].props.x,self.game.characters[player].props.y)
            car_pos = Vec2d(self.world_size[0]/2,self.world_size[1]/2)
            dir = car_pos - player_pos
            
            compass_surface = pygame.transform.rotate(self.game.resource_manager.get('sprite','compass.png'),-1*dir.angle - 90)
            compass_rect = compass_surface.get_rect()
            
            
            radar_offset = offset + Vec2d(width - 30,30)
            compass_rect.center = radar_offset
            
            pygame.draw.circle(self.screen,(0,0,0),radar_offset,20)
            self.screen.blit(compass_surface,compass_rect)
            
            minimap_offset = offset + Vec2d(10,190)
            
            self.screen.blit(self.minimap,minimap_offset)
            
            player_minimap_pos = self.minimap_scale*player_pos
            player_minimap_pos = Vec2d(int(player_minimap_pos[0]),int(player_minimap_pos[1]))
            
            pygame.draw.circle(self.screen,(255,0,0),minimap_offset+player_minimap_pos,1)
            
            
            
        
        
        pygame.display.flip()
        self.draw_surface = self.world_surface.copy()
            
            



