import game
import pygame
import random
from math import *

from vec2d import Vec2d


FACING = ['right', 'down', 'left', 'up']


class ExampleComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        print '%f seconds have elapsed!' % (dt,)


class MovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('last_good_x', entity.x), ('last_good_y', entity.y)])
        
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.dx or entity.dy:
            entity.last_good_x = entity.x
            entity.last_good_y = entity.y
            game.get_game().collision_grid.remove_entity(entity)
            entity.x += entity.dx * dt
            entity.y += entity.dy * dt
            game.get_game().collision_grid.add_entity(entity)
            
            collisions = game.get_game().collision_grid.get_collisions_for_entity(entity)
            for collided_entity in collisions:
                collided_entity.handle('collision', entity)
                entity.handle('collision', collided_entity)


class InputMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 0), ('dy', 0), 'player'])
        entity.facing = 1
              
        entity.register_handler('input', self.handle_input)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
    
    def handle_input(self, entity, event):
        if event.player != entity.player or event.control not in ['RIGHT', 'UP', 'LEFT', 'DOWN']:
            return
        
        if event.control == 'RIGHT':
            entity.dx = event.value * entity.speed
        elif event.control == 'UP':
            entity.dy = -1 * event.value * entity.speed
        elif event.control == 'LEFT':
            entity.dx = -1 * event.value * entity.speed
        elif event.control == 'DOWN':
            entity.dy = event.value * entity.speed 
        
        if entity.dx != 0 or entity.dy != 0:
            direction = Vec2d(entity.dx, entity.dy)
            entity.facing = int(((direction.get_angle() + 45) % 360) / 90)
            entity.handle('play-animation', 'walk_%s' % (FACING[entity.facing],), True)
        else:
            entity.handle('play-animation', 'idle_%s' % (FACING[entity.facing],), True)           


class DrawComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('image_x', 0), ('image_y', 0), 'x', 'y'])
        
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.image), 
                     (entity.x + entity.image_x, entity.y + entity.image_y))


class DrawHitBoxComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height'])
        
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface):
        pygame.draw.rect(surface, (255, 0, 255), (entity.x, entity.y, entity.width, entity.height))
   

class ZombieAIComponent(object):

    def add(self, entity):
        verify_attrs(entity, ['sight_distance', 'speed', 'attack_distance', 'total_attack_time', ('dx', 0), ('dy', 0)])
        entity.attacking = False
        entity.facing = 1
                
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        if entity.attacking:
            entity.attack_time += dt
            if entity.attack_time >= entity.total_attack_time:
                entity.attacking = False
                entity.attack_time = 0
            else:
                return

        mypos = get_midpoint(entity)
        in_range_player = None
        in_range_player_attack = []
        mindist = entity.sight_distance
        for player in game.get_game().entity_manager.get_by_tag("player"):
            if player.health > 0:
                theirpos = get_midpoint(player)
                dist = (mypos-theirpos).length
                if dist <= entity.sight_distance :
                    if mindist > dist:
                        in_range_player = player

                    if dist <= entity.attack_distance:
                        in_range_player_attack.append(player)

        if in_range_player is not None:
            theirpos = get_midpoint(in_range_player)
            direction = entity.speed * (theirpos-mypos).normalized()
            entity.dx = direction.x
            entity.dy = direction.y

        else:
            direction = Vec2d(entity.dx,entity.dy)
            if direction.length < 1:
                ang = random.uniform(0,3.14159)

                direction = entity.speed * Vec2d(cos(ang),sin(ang))
            else:
                ang = atan(direction.y/direction.x)
                ang += random.gauss(0,0.1)
                direction = direction.length * Vec2d(cos(ang),sin(ang))
            entity.dx = direction.x
            entity.dy = direction.y


        if len(in_range_player_attack) > 0:
            entity.dx = 0
            entity.dy = 0

            entity.attacking = True
            #entity.attack_time = 0

            for player in in_range_player_attack:
                player.handle('attack', entity, dt)
        
        entity.facing = int(((direction.get_angle() + 45) % 360) / 90)
        entity.handle('play-animation', 'walk_%s' % (FACING[entity.facing],), True)


class AttackComponent(object):
    def add(self, entity):
        verify_attrs(entity, ['health'])
        
        entity.register_handler('attack', self.handle_attack)

    def remove(self, entity):
        entity.unregister_handler('attack', self.handle_attack)

    def handle_attack(self, entity, attacker, dt):
        if entity.health - (attacker.attack_strength * dt) <= 0:
            entity.health = 0
            entity.handle('dead', False)
        else:
            entity.health -= (attacker.attack_strength * dt)

            #entity_vec = entity.get_midpoint() - attacker.get_midpoint()
            #point_vec = entity_vec.normalized() * attacker.pushback_velocity
            #print entity_vec, point_vec

            #entity.dx += point_vec.x
            #entity.dy += point_vec.y


class PlayerCollisionComponent(object):
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('dx', 0), ('dy', 0), ('last_good_x', entity.x), ('last_good_y', entity.y)])
        
        entity.register_handler('collision', self.handle_collision)
        game.get_game().collision_grid.add_entity(entity)

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)
        game.get_game().collision_grid.remove_entity(entity)

    def handle_collision(self, entity, colliding_entity):
        if 'car' in colliding_entity.tags:
            colliding_entity.handle('use', entity.carrying_item, entity)

        game.get_game().collision_grid.remove_entity(entity)
        
        keep_y = game.get_game().collision_grid.get_collisions((entity.last_good_x, entity.y, entity.width, entity.height))
        keep_x = game.get_game().collision_grid.get_collisions((entity.x, entity.last_good_y, entity.width, entity.height))
        
        if len(keep_x) > 0 or len(keep_y) > 0:
            if len(keep_x) == 0:
                entity.y = entity.last_good_y
            elif len(keep_y) == 0 :
                entity.x = entity.last_good_x
            else:
                entity.x = entity.last_good_x
                entity.y = entity.last_good_y
        
        game.get_game().collision_grid.add_entity(entity)
            
        
class StaticCollisionComponent(object):
    
    def add(self, entity):
        game.get_game().collision_grid.add_entity(entity)
        
    def remove(self, entity):
        game.get_game().collision_grid.remove_entity(entity)
        
        
class ZombieCollisionComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('dx', 0), ('dy', 0), ('last_good_x', entity.x), ('last_good_y', entity.y)])

        entity.register_handler('collision', self.handle_collision)
        game.get_game().collision_grid.add_entity(entity)

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)
        game.get_game().collision_grid.remove_entity(entity)

    def handle_collision(self, entity, colliding_entity):
        # zombies can't collide with other zombies
        if not 'zombie' in colliding_entity.tags and not 'item' in colliding_entity.tags:
            game.get_game().collision_grid.remove_entity(entity)
            
            keep_y = game.get_game().collision_grid.get_collisions((entity.last_good_x, entity.y, entity.width, entity.height))
            keep_x = game.get_game().collision_grid.get_collisions((entity.x, entity.last_good_y, entity.width, entity.height))
            
            if len(keep_x) > 0 or len(keep_y) > 0:
                if len(keep_x) == 0:
                    entity.y = entity.last_good_y
                elif len(keep_y) == 0 :
                    entity.x = entity.last_good_x
                else:
                    entity.x = entity.last_good_x
                    entity.y = entity.last_good_y
            
            game.get_game().collision_grid.add_entity(entity)
            
            
class ItemComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height'])
        entity.pickup = False
        entity.carrying_player = None
        
        entity.register_handler('pickup', self.handle_pickup)
        entity.register_handler('update', self.handle_update)
        entity.register_handler('drop', self.handle_drop)

    def remove(self, entity):
        entity.unregister_handler('pickup', self.handle_pickup)
        entity.unregister_handler('update', self.handle_update)
        entity.unregister_handler('drop', self.handle_drop)

    def handle_pickup(self, entity, player):
        entity.pickup = True
        entity.carrying_player = player
        player.carrying_item = entity
        game.get_game().component_manager.remove("StaticCollisionComponent", entity)

    def handle_drop(self, entity, player):
        entity.pickup = False
        entity.carrying_player = None
        player.carrying_item = None
        game.get_game().component_manager.add("StaticCollisionComponent", entity)

    def handle_update(self, entity, dt):
        if entity.pickup and entity.carrying_player is not None:
            box_in_front = get_box_in_front(entity.carrying_player, entity.width, entity.height)

            entity.x, entity.y = box_in_front[0], box_in_front[1]


class CarComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['needed_item_types', ('dx', 0), ('dy', 0), 'x', 'y'])
        entity.driver = None
        entity.items = []
        entity.item_types = []
        entity.passengers = []
        
        entity.register_handler('use', self.handle_use)

    def remove(self, entity):
        entity.unregister_handler('use', self.handle_use)

    def handle_use(self, entity, item, player):
        CAR_IMAGES = ["items/car/Car-empty.png",
                      "items/car/Car-rear-wheel.png",
                      "items/car/Car-front-rear.png",
              "items/car/Car-engine-front.png",
              "items/car/Car-engine-rear.png",
              "items/car/Car-full.png"]
        
        if item:
            if item.type not in entity.item_types:
                item.handle('drop', player)
                
                entity.items.append(item)
                entity.item_types.append(item.item_type)
                
                game.get_game().items.remove(item)
                game.get_game().component_manager.remove('DrawComponent', item)
                game.get_game().component_manager.remove('ItemComponent', item)
                game.get_game().component_manager.remove('StaticCollisionComponent', item)
                
                entity.image = CAR_IMAGES[len(entity.items)]
                
        elif player and set(entity.item_types).issuperset(entity.needed_item_types):
            if entity.driver is None:
                game.get_game().component_manager.remove("StaticCollisionComponent", entity)
                entity.driver = player
                player.draw = False
                player.x, player.y = entity.x, entity.y
                entity.dx, entity.dy = -200, 2
                player.handle('dead', True)


class InputActionComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['player', 'shove_power'])
        entity.carrying_item = None
        
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, event):
        if event.player != entity.player:
            return
        
        if event.control == 'PICKUP':
            if not entity.carrying_item:
                entities_in_front = get_entities_in_front(entity)

                #print entities_in_front
                for i in entities_in_front:
                    if 'item' in i.tags:
                        i.handle('pickup', entity)
                        return
            else:
                entity.carrying_item.handle('drop', entity)
                
        if event.control == "USE":
            for other in get_entities_in_front(entity):
                other.handle('shove', entity.shove_power)


class DeadComponent(object):
    
    def add(self, entity):
        entity.dead = False
                
        entity.register_handler('dead', self.handle_dead)

    def remove(self, entity):
        entity.unregister_handler('dead', self.handle_dead)

    def handle_dead(self, entity, win):
        if win:
            entity.win = True
        else:
            entity.dead = True
        if entity.carrying_item:
            entity.carrying_item.handle('drop', entity)
        game.get_game().component_manager.remove('MovementComponent', entity)
        game.get_game().component_manager.remove('InputMovementComponent', entity)
        game.get_game().component_manager.remove('PlayerCollisionComponent', entity)
        game.get_game().component_manager.remove('AnimationComponent', entity)
        game.get_game().component_manager.remove('DrawComponent', entity)
        game.get_game().component_manager.remove('AttackComponent', entity)
        game.get_game().component_manager.remove('InputActionComponent', entity)
        

class ShoveComponent(object):
    
    def add(self, entity):
        entity.register_handler('shove', self.handle_shove)

    def remove(self, entity):
        entity.unregister_handler('shove', self.handle_shove) 
        
    def handle_shove(self, entity, power):
        entity.shove_timeout = 2
        entity.dx = 2
    
        
def verify_attrs(entity, attrs):
    missing_attrs = []
    for attr in attrs:
        if isinstance(attr, tuple):
            attr, default = attr
            if not hasattr(entity, attr):
                setattr(entity, attr, default)
        else:
            if not hasattr(entity, attr):
                missing_attrs.append(attr)
    if len(missing_attrs) > 0:
        raise AttributeError("entity [%s] is missing required attributes [%s]" % (entity._static_data_name, missing_attrs))
            

def get_entities_in_front(entity):
    COLLIDE_BOX_WIDTH = 100
    COLLIDE_BOX_HEIGHT = 100
    collision_box = get_box_in_front(entity, COLLIDE_BOX_WIDTH, COLLIDE_BOX_HEIGHT)

    return game.get_game().collision_grid.get_collisions(collision_box)

def get_box_in_front(entity, width, height):
    midpoint = get_midpoint(entity)
    player_dimensions = Vec2d(entity.width, entity.height)
    if entity.facing == 0: #right
        collision_box = (midpoint.x + player_dimensions.x/2, midpoint.y - height/2, width, height)
    elif entity.facing == 1: #down
        collision_box = (midpoint.x - width/2, midpoint.y + player_dimensions.y/2, width, height)
    elif entity.facing == 2: #left
        collision_box = (midpoint.x - player_dimensions.x/2 - width, midpoint.y - height/2, width, height)
    elif entity.facing == 3: #up
        collision_box = (midpoint.x - width/2, midpoint.y - player_dimensions.y/2 - height, width, height)

    return collision_box

def get_midpoint(entity):
    return Vec2d(entity.x + (entity.width/2), entity.y + (entity.height/2))