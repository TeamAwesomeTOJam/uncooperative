import game
import pygame

class ExampleComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        print '%f seconds have elapsed!' % (dt,)

class MovementComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        entity.props.x += entity.props.dx * dt
        entity.props.y += entity.props.dy * dt
        
        
class InputMovementComponent(object):
    
    def add(self, entity):
        entity.register_handler('move', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('move', self.handle_update)
    
    def handle_update(self, entity, event):
        if entity.props.controller == event.joy:
            if event.axis == 0:
                self.dx = event.value
            if event.axis == 1:
                self.dy = event.value

class TileDraw(object):
    
    def add(self, entity):
        entity.register_handler('draw-tiles', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('draw-tiles', self.handle_update)
        
    def handle_update(self, entity, surface):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.props.image),(entity.props.x,entity.props.y))

class ZombieAI(object):

    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        ZOMBIE_DISTANCE = 200
        ZOMBIE_SPEED = 50
        in_range_player = None
        for player in game.get_game().player_list:
            if abs(entity.props.x - player.props.x) <= ZOMBIE_DISTANCE or \
                    abs(entity.props.y - player.props.y) <= ZOMBIE_DISTANCE:
                in_range_player = player
                break

        if in_range_player is not None:
            if in_range_player.props.x >= entity.props.x:
                entity.props.dx = ZOMBIE_SPEED * dt
            else:
                entity.props.dx = -ZOMBIE_SPEED * dt

            if in_range_player.props.dy >= entity.props.y:
                entity.props.dy = ZOMBIE_SPEED * dt
            else:
                in_range_player.props.dy = -ZOMBIE_SPEED * dt
