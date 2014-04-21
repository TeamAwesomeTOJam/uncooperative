import pygame

import game


class AttractMode(object):
    
    def handle_event(self, event):
        game.get_game().mode = PlayMode()
            
    def update(self, dt):
        game.get_game().entity_manager.get_by_name('splashscreen').handle('update', dt)
    
    def draw(self):
        game.get_game().screen.blit(game.get_game().resource_manager.get('sprite', game.get_game().entity_manager.get_by_name('splashscreen').image), (0,0))
    

class PlayMode(object):
    
    def handle_event(self, event):
        for entity in game.get_game().entity_manager.get_by_tag('input'):
            entity.handle('input', event)
            
    def update(self, dt):
        entities_to_update = set()
        for player in game.get_game().entity_manager.get_by_tag('player'):
            update_area = pygame.Rect(0, 0, 800, 800)
            update_area.center = (player.x, player.y)
            entities_to_update.update(game.get_game().entity_manager.get_in_area('update', update_area, precise=False))
            
        for entity in entities_to_update:
            entity.handle('update', dt)
                    
    def draw(self):
        game.get_game().renderer.render()