import game
import pygame
import math
import random
from math import *

from vec2d import Vec2d


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
        
        if entity.props.dx or entity.props.dy:
            entity.props.last_good_x = entity.props.x
            entity.props.last_good_y = entity.props.y
            game.get_game().collision_grid.remove_entity(entity)
            entity.props.x += entity.props.dx * dt
            entity.props.y += entity.props.dy * dt
            game.get_game().collision_grid.add_entity(entity)
            
        entity.handle('draw', game.get_game().renderer.draw_surface)
        collisions = game.get_game().collision_grid.get_collisions_for_entity(entity)
        for collided_entity in collisions:
            collided_entity.handle('collision', entity)
            entity.handle('collision', collided_entity)

class InputMovementComponent(object):
    
    def add(self, entity):
        entity.register_handler('move', self.handle_move)
        game.get_game().register_for_input(entity)
    
    def remove(self, entity):
        entity.unregister_handler('move', self.handle_move)
    
    def handle_move(self, entity, event):
        SPEED = 20 * 8
        DEADZONE = 0.15

        if entity.props.player == event.player:
            if event.axis == 0:
                entity.props.x_input = event.magnitude
            if event.axis == 1:
                entity.props.y_input = event.magnitude
                
            magnitude = ((entity.props.x_input * entity.props.x_input) + (entity.props.y_input * entity.props.y_input)) ** 0.5

            if magnitude < DEADZONE:
                entity.props.dx = 0
                entity.props.dy = 0
            else:
                x_norm = entity.props.x_input / magnitude
                y_norm = entity.props.y_input / magnitude
                entity.props.dx = x_norm * ((magnitude - DEADZONE) / (1 - DEADZONE)) * SPEED
                entity.props.dy = y_norm * ((magnitude - DEADZONE) / (1 - DEADZONE)) * SPEED


class DrawComponent(object):
    
    def add(self, entity):
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.props.image), (entity.props.x, entity.props.y))


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
        mypos = Vec2d(entity.props.x,entity.props.y)
        in_range_player = None
        in_range_player_attack = []
        for player in game.get_game().characters:
            theirpos = Vec2d(player.props.x,player.props.y)
            dist = mypos.dot(theirpos)**.5
            if dist <= ZOMBIE_DISTANCE:
                if in_range_player is None:
                    in_range_player = player

                if dist <= ZOMBIE_ATTACK_DISTANCE:
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
        else:
            dir = Vec2d(entity.props.dx,entity.props.dy)
            if dir.length < 1:
                ang = random.uniform(0,3.14159)

                dir = ZOMBIE_SPEED * Vec2d(cos(ang),sin(ang))
            else:
                ang = atan(dir.y/dir.x)
                ang += random.gauss(0,1)
                dir = dir.length * Vec2d(cos(ang),sin(ang))
            entity.props.dx = dir.x
            entity.props.dy = dir.y



        if len(in_range_player_attack) > 0:
            entity.props.dx = 0
            entity.props.dy = 0

            entity.props.attacking = True

            for player in in_range_player_attack:
                player.handle('attack', ZOMBIE_ATTACK_STRENGTH, entity)


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


class PlayerCollisionComponent(object):
    def add(self, entity):
        entity.register_handler('collision', self.handle_collision)

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)

    def handle_collision(self, entity, colliding_entity):
        try:
            good_x = entity.props.last_good_x
            good_y = entity.props.last_good_y
        except AttributeError:
            good_x = entity.props.x - 20
            good_y  = entity.props.y - 20
        
        game.get_game().collision_grid.remove_entity(entity)
        entity.props.x = good_x
        entity.props.y = good_y
        game.get_game().collision_grid.add_entity(entity)
        
class ItemComponent(object):
    def add(self, entity):
        entity.register_handler('pickup', self.handle_pickup)
        entity.register_handler('move', self.handle_move)
        entity.register_handler('drop', self.handle_drop)

    def remove(self, entity):
        entity.unregister_handler('pickup', self.handle_pickup)
        entity.unregister_handler('move', self.handle_move)
        entity.unregister_handler('drop', self.handle_drop)

    def handle_pickup(self, entity, player):
        PICKUP_DISTANCE = 10
        if abs(entity.props.x - player.props.x) <= PICKUP_DISTANCE and \
            abs(entity.props.y - player.props.y) <= PICKUP_DISTANCE:
            entity.props.pickup = True
            entity.props.carrying_player = player

    def handle_drop(self, entity, player):
        entity.props.pickup = False
        entity.props.carrying_player = None

    def handle_move(self, entity):
        if entity.props.pickup and entity.props.carrying_player is not None:
            entity.props.x, entity.props.y = entity.props.carrying_player.props.x, entity.props.carrying_player.props.y
