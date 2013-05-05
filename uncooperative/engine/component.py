import game
import pygame
import math
import random
from math import *

from vec2d import Vec2d


FACING = ['right', 'down', 'left', 'up']


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
        if entity.props.last_good_x is None:
            entity.props.last_good_x = entity.props.x
        if entity.props.last_good_y is None:
            entity.props.last_good_y = entity.props.y
    
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
        entity.props.facing = 1
    
    def remove(self, entity):
        entity.unregister_handler('move', self.handle_move)
    
    def handle_move(self, entity, event):
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
                entity.handle('play-animation', 'idle-%s' % (FACING[entity.props.facing],), True)
            else:
                x_norm = entity.props.x_input / magnitude
                y_norm = entity.props.y_input / magnitude

                entity.props.dx = x_norm * ((magnitude - DEADZONE) / (1 - DEADZONE)) * entity.props.speed
                entity.props.dy = y_norm * ((magnitude - DEADZONE) / (1 - DEADZONE)) * entity.props.speed
                
                dir = Vec2d(entity.props.dx, entity.props.dy)
                entity.props.facing = int(((dir.get_angle() + 45) % 360) / 90)
                entity.handle('play-animation', 'walk-%s' % (FACING[entity.props.facing],), True)


class DrawComponent(object):
    
    def add(self, entity):
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        if entity.props.image_x is None:
            image_x = 0
        else:
            image_x = entity.props.image_x
            
        if entity.props.image_y is None:
            image_y = 0
        else:
            image_y = entity.props.image_y
        surface.blit(game.get_game().resource_manager.get('sprite', entity.props.image), 
                     (entity.props.x + image_x, entity.props.y + image_y))


class DrawHitBoxComponent(object):
    
    def add(self, entity):
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        pygame.draw.rect(surface, (255, 0, 255), (entity.props.x, entity.props.y, entity.props.width, entity.props.height))
        

class RegisterForDrawComponent(object):
    
    def add(self, entity):
        game.get_game().register_for_drawing(entity)
        
    def remove(self, entity):
        pass
    

class ZombieAIComponent(object):

    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)
        entity.props.facing = 1

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        ZOMBIE_DISTANCE = entity.props.sight_distance
        ZOMBIE_SPEED = entity.props.speed
        ZOMBIE_ATTACK_DISTANCE = entity.props.attack_distance
        ZOMBIE_ATTACK_TIME = entity.props.total_attack_time

        if entity.props.attacking:
            entity.props.attack_time += dt
            if entity.props.attack_time >= ZOMBIE_ATTACK_TIME:
                entity.props.attacking = False
                entity.props.attack_time = 0
            else:
                return

        mypos = entity.props.get_midpoint()
        in_range_player = None
        in_range_player_attack = []
        mindist = ZOMBIE_DISTANCE
        for player in game.get_game().characters:
            if player.props.health > 0:
                theirpos = player.props.get_midpoint()
                dist = (mypos-theirpos).length
                if dist <= ZOMBIE_DISTANCE :
                    if mindist > dist:
                        in_range_player = player

                    if dist <= ZOMBIE_ATTACK_DISTANCE:
                        in_range_player_attack.append(player)

        if in_range_player is not None:
            theirpos = in_range_player.props.get_midpoint()
            dir = ZOMBIE_SPEED * (theirpos-mypos).normalized()
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
            #entity.props.attack_time = 0

            for player in in_range_player_attack:
                player.handle('attack', entity, dt)
        
        entity.props.facing = int(((dir.get_angle() + 45) % 360) / 90)
        entity.handle('play-animation', 'walk-%s' % (FACING[entity.props.facing],), True)


class AttackComponent(object):
    def add(self, entity):
        entity.register_handler('attack', self.handle_attack)
        game.get_game().register_for_updates(entity)

    def remove(self, entity):
        entity.unregister_handler('attack', self.handle_attack)

    def handle_attack(self, entity, attacker, dt):
        if entity.props.health - (attacker.props.attack_strength * dt) <= 0:
            entity.props.health = 0
            entity.handle('dead')
        else:
            entity.props.health -= (attacker.props.attack_strength * dt)

            #entity_vec = entity.props.get_midpoint() - attacker.props.get_midpoint()
            #point_vec = entity_vec.normalized() * attacker.props.pushback_velocity
            #print entity_vec, point_vec

            #entity.props.dx += point_vec.x
            #entity.props.dy += point_vec.y


class PlayerCollisionComponent(object):
    def add(self, entity):
        entity.register_handler('collision', self.handle_collision)
        game.get_game().collision_grid.add_entity(entity)
        if entity.props.last_good_x is None:
            entity.props.last_good_x = entity.props.x
        if entity.props.last_good_y is None:
            entity.props.last_good_y = entity.props.y

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)
        game.get_game().collision_grid.remove_entity(entity)

    def handle_collision(self, entity, colliding_entity):
        if colliding_entity.props.car and entity.props.carrying_item:
            colliding_entity.handle('use', entity.props.carring_item, entity)
            return

        try:
            dx = entity.props.dx
            dy = entity.props.dy
        except AttributeError:
            dx = None
            dy = None

        if dx or dy:
            game.get_game().collision_grid.remove_entity(entity)
            
            keep_y = game.get_game().collision_grid.get_collisions((entity.props.last_good_x, entity.props.y, entity.props.width, entity.props.height))
            keep_x = game.get_game().collision_grid.get_collisions((entity.props.x, entity.props.last_good_y, entity.props.width, entity.props.height))
            
            if len(keep_x) > 0 or len(keep_y) > 0:
                if len(keep_x) == 0:
                    entity.props.y = entity.props.last_good_y
                elif len(keep_y) == 0 :
                    entity.props.x = entity.props.last_good_x
                else:
                    entity.props.x = entity.props.last_good_x
                    entity.props.y = entity.props.last_good_y
            
            game.get_game().collision_grid.add_entity(entity)
            
        
class StaticCollisionComponent(object):
    
    def add(self, entity):
        game.get_game().collision_grid.add_entity(entity)
        
    def remove(self, entity):
        game.get_game().collision_grid.remove_entity(entity)
        
        
class ZombieCollisionComponent(object):
    def add(self, entity):
        entity.register_handler('collision', self.handle_collision)
        game.get_game().collision_grid.add_entity(entity)
        if entity.props.last_good_x is None:
            entity.props.last_good_x = entity.props.x
        if entity.props.last_good_y is None:
            entity.props.last_good_y = entity.props.y

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)
        game.get_game().collision_grid.remove_entity(entity)

    def handle_collision(self, entity, colliding_entity):
        try:
            dx = entity.props.dx
            dy = entity.props.dy
        except AttributeError:
            dx = None
            dy = None

        if dx or dy:
            game.get_game().collision_grid.remove_entity(entity)
            
            entity.props.x = entity.props.last_good_x
            entity.props.y = entity.props.last_good_y
            
            game.get_game().collision_grid.add_entity(entity)
            
            
class ItemComponent(object):
    def add(self, entity):
        entity.register_handler('pickup', self.handle_pickup)
        entity.register_handler('update', self.handle_update)
        entity.register_handler('drop', self.handle_drop)
        game.get_game().register_for_updates(entity)

    def remove(self, entity):
        entity.unregister_handler('pickup', self.handle_pickup)
        entity.unregister_handler('update', self.handle_update)
        entity.unregister_handler('drop', self.handle_drop)

    def handle_pickup(self, entity, player):
        print "Pickup", entity
        entity.props.pickup = True
        entity.props.carrying_player = player
        player.props.carrying_item = entity
        game.get_game().component_manager.remove("StaticCollisionComponent", entity)

    def handle_drop(self, entity, player):
        entity.props.pickup = False
        entity.props.carrying_player = None
        player.props.carrying_item = None
        game.get_game().component_manager.add("StaticCollisionComponent", entity)


    def handle_update(self, entity, dt):
        if entity.props.pickup and entity.props.carrying_player is not None:
            box_in_front = entity.props.carrying_player.get_box_in_front(entity.props.width, entity.props.height)

            entity.props.x, entity.props.y = box_in_front[0], box_in_front[1]


class CarComponent(object):
    def add(self, entity):
        entity.register_handler('use', self.handle_use)

    def remove(self, entity):
        entity.unregister_handler('use', self.handle_use)

    def handle_use(self, entity, item, player):
        if item:
            if item.type not in entity.item_types:
                item.handle('drop', player)

                entity.items.append(item)
                entity.item_types.append(item.type)
        elif player and all(x in entity.props.needed_item_types for x in entity.props.item_types):
            if entity.props.driver is None:
                entity.props.driver = player
                player.props.draw = False
                player.props.x, player.props.y = entity.props.x, entity.props.y


class InputActionComponent(object):
    def add(self, entity):
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, event):
        if hasattr(event, "player") and entity.props.player and entity.props.player == event.player and \
                (event.button_down or event.key_down) and event.action == "PICKUP":
            if not entity.props.carrying_item:
                entities_in_front = entity.get_entities_in_front()

                print entities_in_front
                for i in entities_in_front:
                    if i.props.item:
                        i.handle('pickup', entity)
                        return
            else:
                entity.props.carrying_item.handle('drop', entity)


class DeadComponent(object):
    def add(self, entity):
        entity.register_handler('dead', self.handle_dead)

    def remove(self, entity):
        entity.unregister_handler('dead', self.handle_dead)

    def handle_dead(self, entity):
        entity.props.dead = True
        game.get_game().component_manager.remove('MovementComponent', entity)
        game.get_game().component_manager.remove('InputMovementComponent', entity)
        game.get_game().component_manager.remove('PlayerCollisionComponent', entity)
        game.get_game().component_manager.remove('AnimationComponent', entity)
        game.get_game().component_manager.remove('DrawComponent', entity)
        game.get_game().component_manager.remove('RegisterForDrawComponent', entity)
        game.get_game().component_manager.remove('AttackComponent', entity)
        game.get_game().component_manager.remove('InputActionComponent', entity)