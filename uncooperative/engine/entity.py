'''
Created on May 2, 2013

@author: jonathan
'''
import game
from vec2d import Vec2d


class Entity(object):
    
    def __init__(self, definition, properties=None, components=None):
        
        def flatten_includes(definition, flattened=None):
            if flattened is None:
                flattened = []
            flattened.append(definition)
            def_map = game.get_game().resource_manager.get('definition', definition)
            if 'includes' in def_map:
                for include in def_map['includes']:
                    flattened = flatten_includes(include, flattened=flattened)
            
            return flattened
        
        self.handlers = {}
        
        definitions = flatten_includes(definition)
        self.props = EntityProperties(definitions)

        if properties is not None:
            for key, value in properties.items():
                setattr(self.props, key, value)        
        
        for defn in definitions:
            for component in game.get_game().resource_manager.get('definition', defn)['components']:  
                game.get_game().component_manager.add(component, self)
        
        if components is not None:
            for component in components:
                game.get_game().component_manager.add(component, self)
                
                    
    def register_handler(self, event, handler):
        self.handlers.setdefault(event, []).append(handler)
        
    def unregister_handler(self, event, handler):
        try:
            self.handlers[event].remove(handler)
        except ValueError:
            pass
    
    def handle(self, event, *args):
        for handler in self.handlers.get(event, []):
            handler(self, *args)


    def get_entities_in_front(self):
        COLLIDE_BOX_WIDTH = 100
        COLLIDE_BOX_HEIGHT = 100
        collision_box = self.get_box_in_front(COLLIDE_BOX_WIDTH, COLLIDE_BOX_HEIGHT)

        return game.get_game().collision_grid.get_collisions(collision_box)

    def get_box_in_front(self, BOX_WIDTH, BOX_HEIGHT):
        midpoint = self.props.get_midpoint()
        player_dimensions = Vec2d(self.props.width, self.props.height)
        if self.props.facing == 0: #right
            collision_box = (midpoint.x + player_dimensions.x/2, midpoint.y - BOX_HEIGHT/2, BOX_WIDTH, BOX_HEIGHT)
        elif self.props.facing == 1: #down
            collision_box = (midpoint.x - BOX_WIDTH/2, midpoint.y + player_dimensions.y/2, BOX_WIDTH, BOX_HEIGHT)
        elif self.props.facing == 2: #left
            collision_box = (midpoint.x - player_dimensions.x/2 - BOX_WIDTH, midpoint.y - BOX_HEIGHT/2, BOX_WIDTH, BOX_HEIGHT)
        elif self.props.facing == 3: #up
            collision_box = (midpoint.x - BOX_WIDTH/2, midpoint.y - player_dimensions.y/2 - BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT)

        return collision_box


class EntityProperties(object):

    def __init__(self, definitions):
        self._definitions = definitions
        
    def __getattr__(self, name):
        for definition in self._definitions:
            props = game.get_game().resource_manager.get('definition', definition)['properties']
            if name in props:
                setattr(self, name, props[name])
                return props[name]
        setattr(self, name, None)        
        return None

    def get_midpoint(self):
        return Vec2d(self.x + (self.width/2), self.y + (self.height/2))
