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
        SPEED = 100
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
                entity.handle('play-animation', 'default', True)
            else:
                x_norm = entity.props.x_input / magnitude
                y_norm = entity.props.y_input / magnitude
                entity.props.dx = x_norm * ((magnitude - DEADZONE) / (1 - DEADZONE)) * SPEED
                entity.props.dy = y_norm * ((magnitude - DEADZONE) / (1 - DEADZONE)) * SPEED
                entity.handle('play-animation', 'walk', True)


class DrawComponent(object):
    
    def add(self, entity):
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.props.image), (entity.props.x, entity.props.y))


class RegisterForDrawComponent(object):
    
    def add(self, entity):
        game.get_game().register_for_drawing(entity)
        
    def remove(self, entity):
        pass
    

class ZombieAIComponent(object):

    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        ZOMBIE_DISTANCE = 200
        ZOMBIE_SPEED = 40
        ZOMBIE_ATTACK_DISTANCE = 10
        ZOMBIE_ATTACK_STRENGTH = 1
        ZOMBIE_ATTACK_TIME = 200

        if entity.props.attacking:
            entity.props.attack_time += dt
            if entity.props.attack_time >= ZOMBIE_ATTACK_TIME:
                entity.props.attacking = False
                entity.props.attack_time = 0
            else:
                return

        mypos = Vec2d(entity.props.x,entity.props.y)
        in_range_player = None
        in_range_player_attack = []
        for player in game.get_game().characters:
            theirpos = Vec2d(player.props.x,player.props.y)
            dist = (mypos-theirpos).length
            if dist <= ZOMBIE_DISTANCE:
                if in_range_player is None:
                    in_range_player = player

                if dist <= ZOMBIE_ATTACK_DISTANCE:
                    in_range_player_attack.append(player)

        if in_range_player is not None:
            theirpos = Vec2d(in_range_player.props.x,in_range_player.props.y)
            dir = ZOMBIE_SPEED * (theirpos-mypos).normalized()
            print "Following: ", dir.x,dir.y,in_range_player.props.player
            entity.props.dx = dir.x
            entity.props.dy = dir.y

        else:
            dir = Vec2d(entity.props.dx,entity.props.dy)
            if dir.length < 1:
                ang = random.uniform(0,3.14159)

                dir = ZOMBIE_SPEED * Vec2d(cos(ang),sin(ang))
            else:
                ang = atan(dir.y/dir.x)
                ang += random.gauss(0,0.1)
                dir = dir.length * Vec2d(cos(ang),sin(ang))
            entity.props.dx = dir.x
            entity.props.dy = dir.y


        if len(in_range_player_attack) > 0:
            entity.props.dx = 0
            entity.props.dy = 0

            entity.props.attacking = True
            entity.props.attack_time = 0

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

        if entity.props.health - attack_strength <= 0:
            entity.props.health = 0
            entity.handle('dead')
        else:
            #print entity.props.x, entity.props.y, zombie.props.x, zombie.props.y

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
            player = entity.props.player
            #if player != "4":
                #print entity.props.__dict__
                #print colliding_entity.props.__dict__
        except:
            pass
        
        try:
            good_x = entity.props.last_good_x
            good_y = entity.props.last_good_y
        except AttributeError:
            good_x = entity.props.x 
            good_y = entity.props.y
        
        try:
            dx = entity.props.dx
            dy = entity.props.dy
        except:
            dx = None
            dy = None

        if dx or dy:
            #print entity.props.x, entity.props.y, colliding_entity.props.x, colliding_entity.props.y
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


class CarComponent(object):
    def add(self, entity):
        entity.register_handler('use', self.handle_use)

    def remove(self, entity):
        entity.unregister_handler('use', self.handle_use)

    def handle_use(self, entity, item, player):
        CAR_USE_DISTANCE = 10

        if abs(entity.props.x - player.props.x) <= CAR_USE_DISTANCE and \
            abs(entity.props.y - player.props.y) <= CAR_USE_DISTANCE:
            if item:
                if item.type not in entity.item_types:
                    item.props.pickup = False
                    item.props.carrying_player = None
                    item.props.display = False
                    entity.items.append(item)
                else:
                    item.props.pickup = False
                    item.props.carrying_player = None
            elif player and all(x in entity.props.needed_item_types for x in entity.props.item_types):
                if entity.props.driver is None:
                    entity.props.driver = player
                    player.props.draw = False
                    player.props.x, player.props.y = entity.props.x, entity.props.y
