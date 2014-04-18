'''
Created on May 2, 2013

@author: jonathan
'''


class EntityManager(object):
    
    def __init__(self):
        self.entities = set()
        self._entities_by_name = {}
        self._entities_by_tag = {}
    
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
    
    def remove_entity(self, entity):
        if hasattr(entity, 'tags'):
            for tag in entity.tags:
                self._entities_by_tag[tag].remove(entity)
        
        if hasattr(entity, 'name'):
            del self._entities_by_name[entity.name]
        
        self.entities.remove(entity)
        
    
    def get_by_name(self, name):
        return self._entities_by_name[name]
        
    def get_by_tag(self, tag):
        return self._entities_by_tag.get(tag, set())