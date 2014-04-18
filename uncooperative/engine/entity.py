'''
Created on May 2, 2013

@author: jonathan
'''

import game


class Entity(object):
    
    def __init__(self, static_data_name, **kwargs):
        self._static_data_name = static_data_name      
        self._handlers = {}
        
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)
            
        if 'components' in self.__dict__ or 'components' in self.static._fields:
            for component in self.components:
                game.get_game().component_manager.add(component, self)

    def __getattr__(self, name):
        return getattr(self.static, name)
    
    @property
    def static(self):
        return game.get_game().resource_manager.get('definition', self._static_data_name)
        
    def register_handler(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)
        
    def unregister_handler(self, event, handler):
        try:
            self._handlers[event].remove(handler)
        except ValueError:
            pass
    
    def handle(self, event, *args):
        for handler in self._handlers.get(event, []):
            handler(self, *args)

