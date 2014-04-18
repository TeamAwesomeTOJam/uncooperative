'''
Created on May 2, 2013

@author: jonathan
'''

import spatialmap


GRID_SIZE = 32


class EntityManager(object):
    
    def __init__(self):
        self.entities = set()
        self._entities_by_name = {}
        self._entities_by_tag = {}
        self._spatial_map = spatialmap.SpatialMap(GRID_SIZE)
    
    def add_entity(self, entity):
        self.entities.add(entity)
        
        if hasattr(entity, 'name'):
            self._entities_by_name[entity.name] = entity
        
        if hasattr(entity, 'tags'):
            for tag in entity.tags:
                self._entities_by_tag.setdefault(tag, set()).add(entity)
        
        self._spatial_map.add(entity)
    
    def remove_entity(self, entity):
        self._spatial_map.remove(entity)
        
        if hasattr(entity, 'tags'):
            for tag in entity.tags:
                self._entities_by_tag[tag].remove(entity)
        
        if hasattr(entity, 'name'):
            del self._entities_by_name[entity.name]
        
        self.entities.remove(entity)
    
    def update_position(self, entity):
        self._spatial_map.update(entity)
        
    def get_by_name(self, name):
        return self._entities_by_name[name]
        
    def get_by_tag(self, tag):
        return self._entities_by_tag.get(tag, set())
    
    def get_in_area(self, rect, precise=True):
        return self._spatial_map.get(rect, precise)