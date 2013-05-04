import game
import pygame
import math



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
        pygame.draw.rect(game.get_game().world_surface, (255,255,255), (entity.props.x,entity.props.y,20,20))

        
class InputMovementComponent(object):
    
    def add(self, entity):
        entity.register_handler('move', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('move', self.handle_update)
    
    def handle_update(self, entity, event):
        speed = 10
        deadzone = 0.25
        if entity.props.controller == event.joy:

            if event.axis == 0:
                entity.props.x_input = event.value
            if event.axis == 1:
                entity.props.y_input = event.value
                
            magnitude = ((entity.props.x_input * entity.props.x_input) + (entity.props.y_input * entity.props.y_input)) ** 0.5

            if magnitude < deadzone:
                entity.props.dx = 0
                entity.props.dy = 0
            else:
                entity.props.dx = event.value * speed
                x_norm = entity.props.x_input / magnitude
                y_norm = entity.props.y_input / magnitude
                entity.props.dx = x_norm * ((magnitude - deadzone) / (1 - deadzone)) * speed
                entity.props.dy = y_norm * ((magnitude - deadzone) / (1 - deadzone)) * speed

class TileDraw(object):
    
    def add(self, entity):
        entity.register_handler('draw-tiles', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('draw-tiles', self.handle_update)
        
    def handle_update(self, entity, surface):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.props.image),(entity.props.x,entity.props.y))

class ZombieAIComponent(object):

    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        ZOMBIE_DISTANCE = 200
        ZOMBIE_SPEED = 50
        ZOMBIE_ATTACK_DISTANCE = 10
        ZOMBIE_ATTACK_STRENGTH = 1
        in_range_player = None
        in_range_player_attack = []
        for player in game.get_game().player_list:
            if abs(entity.props.x - player.props.x) <= ZOMBIE_DISTANCE or \
                    abs(entity.props.y - player.props.y) <= ZOMBIE_DISTANCE:
                if in_range_player is None:
                    in_range_player = player

                if abs(entity.props.x - player.props.x) <= ZOMBIE_ATTACK_DISTANCE or \
                    abs(entity.props.y - player.props.y) <= ZOMBIE_ATTACK_DISTANCE:
                    in_range_player_attack.append(player)

        if in_range_player is not None:
            if in_range_player.props.x >= entity.props.x:
                entity.props.dx = ZOMBIE_SPEED
            else:
                entity.props.dx = -ZOMBIE_SPEED

            if in_range_player.props.dy >= entity.props.y:
                entity.props.dy = ZOMBIE_SPEED
            else:
                in_range_player.props.dy = -ZOMBIE_SPEED

        if len(in_range_player_attack) > 0:
            entity.props.dx = 0
            entity.props.dy = 0

            entity.props.attacking = True

            for player in in_range_player_attack:
                player.handle('attack', attack_strength=ZOMBIE_ATTACK_STRENGTH, zombie=entity)


class AttackComponent(object):
    def add(self, entity):
        entity.register_handler('attack', self.handle_attack)
        game.get_game().register_for_updates(entity)

    def remove(self, entity):
        entity.unregister_handler('attack', self.handle_attack)

    def handle_attack(self, entity, attack_strength, zombie):
        PLAYER_PUSHBACK_VELOCITY = 20

        if (entity.props.health - attack_strength <= 0):
            entity.props.health = 0
            entity.handle('dead')
        else:
            entity.props.health -= attack_strength

            x = entity.props.x - zombie.props.x
            y = entity.props.y - zombie.props.y

            entity.props.dx = -math.sqrt(math.pow(y, 2) - math.pow(PLAYER_PUSHBACK_VELOCITY, 2))
            entity.props.dy = -math.sqrt(math.pow(x, 2) - math.pow(PLAYER_PUSHBACK_VELOCITY, 2))
