'''
Created on May 3, 2013

@author: jonathan
'''

import game


class ComponentManager(object):

    def __init__(self):
        self.components = {}
        
    def register_component(self, name, component):
        self.components[name] = component
        
    def add(self, name, entity):
        self.components[name].add(entity)
        
    def remove(self, name, entity):
        self.components[name].remove(entity)
        
        
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
        entity.props.x += entity.props.dx
        entity.props.y += entity.props.dy