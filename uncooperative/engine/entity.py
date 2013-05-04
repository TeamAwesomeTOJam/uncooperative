'''
Created on May 2, 2013

@author: jonathan
'''
import game


class Entity(object):
    
    def __init__(self, definition, properties=None, components=None):
        
        def flatten_includes(definition, flattened=None):
            if flattened == None:
                flattened = []
            flattened.append(definition)
            def_map = game.get_game().resource_manager.get('definition', definition)
            if 'includes' in def_map:
                for include in def_map['includes']:
                    flattened = flatten_includes(include, flattened=flattened)
            
            return flattened
        
        
        definitions = flatten_includes(definition)
        
        self.props = EntityProperties(definitions)
        self.handlers = {}
        
        for component in game.get_game().resource_manager.get('definition', definition)['components']:
            game.get_game().component_manager.add(component, self)
        
        if properties:
            for key, value in properties.items():
                setattr(self.props, key, value)
                
        if components:
            for component in components:
                game.get_game().component_manager.add(component, self)
                
                    
    def register_handler(self, event, handler):
        if not self.handlers.get(event):
            self.handlers[event] = []
        self.handlers.get(event).append(handler)
        
    def unregister_handler(self, event, handler):
        try:
            del self.handlers[event][self.handlers[event].index(handler)]
        except:
            pass
    
    def handle(self, event, *args):
        for handler in self.handlers.get(event, []):
            handler(self, *args)
            

class EntityProperties(object):

    def __init__(self, definitions):
        self._definitions = definitions
        
    def __getattr__(self, name):
        for definition in self._definitions:
            props = game.get_game().resource_manager.get('definition', definition)['properties']
            if name in props: 
                return props[name]
        raise AttributeError
