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


class AnimationComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.on_update)
        entity.register_handler('play-animation', self.on_play_animation)
        
        entity.current_animation = 'default'
        entity.animation_pos = 0
        entity.animation_should_loop = True

        entity.image = getattr(entity.animations, entity.current_animation).frames[0]
        
    def remove(self, entity):
        entity.unregister_handler('update', self.on_update)
        entity.unregister_handler('play-animation', self.on_play_animation)
        
    def on_update(self, entity, dt):
        entity.animation_pos += dt
        if entity.animation_pos >= getattr(entity.animations, entity.current_animation).duration:
            if entity.animation_should_loop:
                entity.animation_pos = entity.animation_pos % getattr(entity.animations, entity.current_animation).duration
            else:
                entity.handle('animation-finished', entity.current_animation)
                entity.current_animation = 'default'
                entity.animation_pos = 0
                entity.animation_should_loop = True
        frame_number = int(entity.animation_pos / getattr(entity.animations, entity.current_animation).duration * len(getattr(entity.animations, entity.current_animation).frames))
        entity.image = getattr(entity.animations, entity.current_animation).frames[frame_number]
        
    def on_play_animation(self, entity, animation, loop=False):
        if animation == entity.current_animation and entity.animation_should_loop and loop:
            pass
        else:
            entity.current_animation = animation
            entity.animation_should_loop = loop
            entity.animation_pos = 0


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
            entity.x += entity.dx * dt
            entity.y += entity.dy * dt
            game.get_game().entity_manager.update_position(entity)
            
            collisions = game.get_game().entity_manager.get_in_area('collide', (entity.x, entity.y, entity.width, entity.height)) - {entity} 
            for collided_entity in collisions:
                collided_entity.handle('collision', entity)
                entity.handle('collision', collided_entity)


class InputMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 0), ('dy', 0), 'name'])
        entity.facing = 1
              
        entity.register_handler('input', self.handle_input)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
    
    def handle_input(self, entity, event):
        if event.target != entity.name or event.action not in ['RIGHT', 'UP', 'LEFT', 'DOWN']:
            return
        
        if event.action == 'RIGHT':
            entity.dx = event.value * entity.speed
        elif event.action == 'UP':
            entity.dy = -1 * event.value * entity.speed
        elif event.action == 'LEFT':
            entity.dx = -1 * event.value * entity.speed
        elif event.action == 'DOWN':
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
        
    def handle_draw(self, entity, surface, transform):
        surface.blit(game.get_game().resource_manager.get('sprite', entity.image), transform(entity.x + entity.image_x, entity.y + entity.image_y))


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


class PlayerCollisionComponent(object):
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('dx', 0), ('dy', 0), ('last_good_x', entity.x), ('last_good_y', entity.y)])
        entity.register_handler('collision', self.handle_collision)

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)

    def handle_collision(self, entity, colliding_entity):
        if colliding_entity == entity.carrying_item:
            return
        
        if 'car' in colliding_entity.tags:
            colliding_entity.handle('use', entity.carrying_item, entity)
        
        y_axis_collisions = game.get_game().entity_manager.get_in_area('collide', (entity.last_good_x, entity.y, entity.width, entity.height)) - {entity}
        x_axis_collisions = game.get_game().entity_manager.get_in_area('collide', (entity.x, entity.last_good_y, entity.width, entity.height)) - {entity}
        
        if len(x_axis_collisions) > 0:
            entity.x = entity.last_good_x
        
        if len(y_axis_collisions) > 0:
            entity.y = entity.last_good_y
        
        game.get_game().entity_manager.update_position(entity)

        
class ZombieCollisionComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('dx', 0), ('dy', 0), ('last_good_x', entity.x), ('last_good_y', entity.y)])
        entity.register_handler('collision', self.handle_collision)

    def remove(self, entity):
        entity.unregister_handler('collision', self.handle_collision)

    def handle_collision(self, entity, colliding_entity):
        # zombies can't collide with other zombies
        if not 'zombie' in colliding_entity.tags and not 'item' in colliding_entity.tags:
            y_axis_collisions = game.get_game().entity_manager.get_in_area('collide', (entity.last_good_x, entity.y, entity.width, entity.height)) - {entity}
            x_axis_collisions = game.get_game().entity_manager.get_in_area('collide', (entity.x, entity.last_good_y, entity.width, entity.height)) - {entity}
            
            if len(x_axis_collisions) > 0:
                entity.x = entity.last_good_x
            
            if len(y_axis_collisions) > 0:
                entity.y = entity.last_good_y
            
            game.get_game().entity_manager.update_position(entity)
            
            
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

    def handle_drop(self, entity, player):
        entity.pickup = False
        entity.carrying_player = None
        player.carrying_item = None

    def handle_update(self, entity, dt):
        if entity.pickup and entity.carrying_player is not None:
            box_in_front = get_box_in_front(entity.carrying_player, entity.width, entity.height)

            entity.x, entity.y = box_in_front[0], box_in_front[1]
            game.get_game().entity_manager.update_position(entity)


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
            if item.item_type not in entity.item_types:
                item.handle('drop', player)
                
                entity.items.append(item)
                entity.item_types.append(item.item_type)
                
                game.get_game().entity_manager.remove_entity(item)
                game.get_game().component_manager.remove('DrawComponent', item)
                game.get_game().component_manager.remove('ItemComponent', item)
                
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
        verify_attrs(entity, ['name', 'shove_power'])
        entity.carrying_item = None
        
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, event):
        if event.target != entity.name:
            return
        
        if event.action == 'PICKUP' and event.value > 0:
            if not entity.carrying_item:
                entities_in_front = get_entities_in_front(entity)

                #print entities_in_front
                for i in entities_in_front:
                    if 'item' in i.tags:
                        i.handle('pickup', entity)
                        return
            else:
                entity.carrying_item.handle('drop', entity)
                
        if event.action == "USE" and event.value > 0:
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

    return game.get_game().entity_manager.get_in_area('collide', collision_box)

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