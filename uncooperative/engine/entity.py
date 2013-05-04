'''
Created on May 2, 2013

@author: jonathan
'''
from game import get_game


class Entity(object):
    
    def __init__(self, definition, properties=None, components=None):
        
        self.props = EntityProperties(definition)
        self.handlers = {}
        
        for component in get_game().resource_manager.get('definition', definition)['components']:
            get_game().component_manager.add(component, self)
        
        if properties:
            for key, value in properties.items():
                setattr(self.props, key, value)
                
        if components:
            for component in components:
                get_game().component_manager.add(component, self)
                
    
    def register_handler(self, event, handler):
        self.handlers[event] = self.handlers.get(event, []).append(handler)
        
    def unregister_handler(self, event, handler):
        try:
            del self.handlers[event][self.handlers[event].index(handler)]
        except:
            pass
    
    def handle(self, event, *args):
        for handler in self.handlers.get(event, []):
            handler(self, *args)
            

class EntityProperties(object):

    def __init__(self, definition):
        self._definition = definition
        
    def __getattr__(self, name):
        try:
            get_game().resource_manager.get('definition', self._definition)['properties'][name]
        except KeyError, ke:
            raise AttributeError(ke)
