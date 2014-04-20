import sys

import pygame
from gridgen import GridGenerator
from entity import Entity
from vec2d import Vec2d
import game


class Render:
    
    def __init__(self, game):
        self.game = game
        self.tile_size = game.tile_size
        self.map_size = game.map_size
        self.screen_size = game.screen_size
        self.world_size = game.world_size
        self.grid = GridGenerator(self.map_size).genMap()
        
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                if self.grid[x][y]:
                    up = self.grid[x][(y-1) % self.map_size[1]]
                    down = self.grid[x][(y+1) % self.map_size[1]]
                    left = self.grid[(x-1)% self.map_size[0]][y]
                    right = self.grid[(x+1)% self.map_size[0]][y]
                    tile_type = 'impassabletileA'
                    if up and down and left and right:
                        upleft = self.grid[(x-1)% self.map_size[0]][(y-1)% self.map_size[1]]
                        upright = self.grid[(x+1)% self.map_size[0]][(y-1)% self.map_size[1]]
                        downleft = self.grid[(x-1)% self.map_size[0]][(y+1)% self.map_size[1]]
                        downright = self.grid[(x+1)% self.map_size[0]][(y+1)% self.map_size[1]]
                        if not upleft:
                            tile_type = 'impassabletileBR'
                        elif not upright:
                            tile_type = 'impassabletileBL'
                        elif not downleft:
                            tile_type = 'impassabletileTR'
                        elif not downright:
                            tile_type = 'impassabletileTL'
                        else:
                            tile_type = 'impassabletileA'
                    elif up and down and left and not right:
                        tile_type = 'impassabletileL'
                    elif up and down and not left and right:
                        tile_type = 'impassabletileR'
                    elif up and down and not left and not right:
                        tile_type = 'impassabletileCV'
                    elif up and not down and left and right:
                        tile_type = 'impassabletileT'
                    elif up and not down and left and not right:
                        tile_type = 'impassabletileCBR'
                    elif up and not down and not left and right:
                        tile_type = 'impassabletileCBL'
                    elif up and not down and not left and not right:
                        tile_type = 'impassabletileCT'
                    elif not up and down and left and right:
                        tile_type = 'impassabletileB'
                    elif not up and down and left and not right:
                        tile_type = 'impassabletileCTR'
                    elif not up and down and not left and right:
                        tile_type = 'impassabletileCTL'
                    elif not up and down and not left and not right:
                        tile_type = 'impassabletileCB'
                    elif not up and not down and left and right:
                        tile_type = 'impassabletileCH'
                    elif not up and not down and left and not right:
                        tile_type = 'impassabletileCR'
                    elif not up and not down and not left and right:
                        tile_type = 'impassabletileCL'
                    elif not up and not down and not left and not right:
                        tile_type = 'impassabletileC'
                    tile = Entity(tile_type, x=x*self.tile_size[0], y=y*self.tile_size[1])
                else:
                    #passable
                    tile = Entity('passabletile', x=x*self.tile_size[0], y=y*self.tile_size[1])
                self.game.entity_manager.add_entity(tile)

        self.minimap_scale = 0.025
        self.minimap_size = Vec2d(int(self.minimap_scale*self.world_size[0]),int(self.minimap_scale*self.world_size[1]))
        
        layers = [StaticLayer(game.world_size, 'tile'), DepthSortedLayer('draw'), UILayer()]
        
        try:
            self.minimap = pygame.transform.smoothscale(layers[0].surface, self.minimap_size)
        except:
            self.minimap = pygame.transform.scale(layers[0].surface, self.minimap_size)

        self.views = []
        self.views.append(View(game.screen, pygame.Rect(0, 0, game.screen_size[0]/2, game.screen_size[1]/2), layers, 'player1'))
        self.views.append(View(game.screen, pygame.Rect(game.screen_size[0]/2, 0, game.screen_size[0]/2, game.screen_size[1]/2), layers, 'player2'))
        self.views.append(View(game.screen, pygame.Rect(0, game.screen_size[1]/2, game.screen_size[0]/2, game.screen_size[1]/2), layers, 'player3'))
        self.views.append(View(game.screen, pygame.Rect(game.screen_size[0]/2, game.screen_size[1]/2, game.screen_size[0]/2, game.screen_size[1]/2), layers, 'player4'))

    def render(self):
        for view in self.views:
            view.draw()
            
        pygame.display.flip()


class View(object):
    
    def __init__(self, surface, area, layers, entity_name):
        self.surface = surface
        self.area = area
        self.layers = layers
        self.entity_name = entity_name
    
    @property
    def entity(self):
        return game.get_game().entity_manager.get_by_name(self.entity_name)
    
    def add_layer(self, layer):
        self.layers.append(layer)
        
    def draw(self):
        self.surface.set_clip(self.area)
        
        for layer in self.layers:
            layer.draw(self)
            
        self.surface.set_clip(None)


class StaticLayer(object):
    
    def __init__(self, size, tag):
        self.size = size
        self.tag = tag
        self.surface = pygame.Surface(self.size)
        self.surface.convert()
        
        transform = lambda x, y : (x, y)
        
        for entity in game.get_game().entity_manager.get_by_tag(tag):
            entity.handle('draw', self.surface, transform)
        
    def draw(self, view):
        area_to_blit = pygame.Rect(view.area)
        area_to_blit.center = (view.entity.x, view.entity.y)
        view.surface.blit(self.surface, view.area, area_to_blit)
    

class DepthSortedLayer(object):
    
    def __init__(self, tag):
        self.tag = tag
        
    def draw(self, view):
        area_to_blit = pygame.Rect(view.area)
        area_to_blit.center = (view.entity.x, view.entity.y)   

        entities_to_draw = sorted(game.get_game().entity_manager.get_in_area(self.tag, area_to_blit, precise=False), key=lambda entity: entity.y)

        transform = lambda x, y : (x - area_to_blit.x + view.area.x, y - area_to_blit.y + view.area.y)
        
        for entity in entities_to_draw:
            entity.handle('draw', view.surface, transform)
        

class UILayer(object):

    def draw(self, view):
        player = view.entity
        offset = Vec2d(view.area.left, view.area.top)
        width = view.area.width
        height = view.area.height
        
        rect = view.area
        pygame.draw.rect(view.surface, (255,255,255), rect, 3)
    
        player_pos = Vec2d(player.x, player.y)
        
        if player.carrying_item or not game.get_game().entity_manager.get_by_tag('item'):
            car = game.get_game().entity_manager.get_by_name('car')
            dest_pos = Vec2d(car.x, car.y)
        else:
            min_distance = sys.maxint
            for item in game.get_game().entity_manager.get_by_tag('item'):
                position = Vec2d(item.x,item.y)
                distance = player_pos - position
                if distance.length < min_distance:
                    min_distance = distance.length
                    min_pos = position
            dest_pos = min_pos
        direction = dest_pos - player_pos
        
        compass_surface = pygame.transform.rotate(game.get_game().resource_manager.get('sprite','compass.png'),-1*direction.angle - 90)
        compass_rect = compass_surface.get_rect()
        
        
        radar_offset = offset + Vec2d(width - 30,30)
        compass_rect.center = radar_offset
        
        pygame.draw.circle(view.surface,(0,0,0),radar_offset,20)
        view.surface.blit(compass_surface,compass_rect)
        
        minimap_offset = offset + Vec2d(10,height - game.get_game().renderer.minimap_size[1] - 10)
        
        view.surface.blit(game.get_game().renderer.minimap, minimap_offset)
        
        player_minimap_pos = game.get_game().renderer.minimap_scale*player_pos
        player_minimap_pos = Vec2d(int(player_minimap_pos[0]),int(player_minimap_pos[1]))
        
        pygame.draw.circle(view.surface,(255,0,0),minimap_offset+player_minimap_pos,1)
        
        health_pos = Vec2d(15,15)
        
        health_bar_rect = pygame.Rect(offset+health_pos,(100,10))
        health_rect = pygame.Rect((0,0),(player.health,10))
        health_rect.inflate_ip(-2,-2)
        health_rect.midleft = health_bar_rect.midleft + Vec2d(2,0)
        
        pygame.draw.rect(view.surface,(0,0,0),health_bar_rect)
        if player.health > 0:
            pygame.draw.rect(view.surface,(255,0,0),health_rect)
            
        # you lose
        if player.dead:
            text_surface = game.get_game().resource_manager.get('sprite','Text/YouLose.png')
            text_rect = text_surface.get_rect()
            text_rect.center = offset + Vec2d(width/2,height/2)
            
            view.surface.blit(text_surface,text_rect)
        elif player.win:
            text_surface = game.get_game().resource_manager.get('sprite','Text/YouWin.png')
            text_rect = text_surface.get_rect()
            text_rect.center = offset + Vec2d(width/2,height/2)
    
            view.surface.blit(text_surface,text_rect)
