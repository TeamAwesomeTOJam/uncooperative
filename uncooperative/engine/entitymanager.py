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
        self._spatial_maps = {}
    
    def add_entity(self, entity):
        self.entities.add(entity)
        
        if hasattr(entity, 'name'):
            self._entities_by_name[entity.name] = entity
        
        if hasattr(entity, 'tags'):
            for tag in entity.tags:
                if tag in self._entities_by_tag:
                    self._entities_by_tag[tag].add(entity)
                else:
                    self._entities_by_tag[tag] = {entity}
                
                if tag in self._spatial_maps:
                    self._spatial_maps[tag].add(entity)
                else:
                    self._spatial_maps[tag] = spatialmap.SpatialMap(GRID_SIZE)
                    self._spatial_maps[tag].add(entity)
    
    def remove_entity(self, entity):       
        if hasattr(entity, 'tags'):
            for tag in entity.tags:
                self._entities_by_tag[tag].remove(entity)
                self._spatial_maps[tag].remove(entity)
        
        if hasattr(entity, 'name'):
            del self._entities_by_name[entity.name]
            
        self.entities.remove(entity)
    
    def update_position(self, entity):
        for tag in entity.tags:
            self._spatial_maps[tag].update(entity)
        
    def get_by_name(self, name):
        return self._entities_by_name[name]
        
    def get_by_tag(self, tag):
        try:
            return self._entities_by_tag[tag]
        except KeyError:
            return set()
    
    def get_in_area(self, tag, rect, precise=True):
        return self._spatial_maps[tag].get(rect, precise)