'''
Created on May 4, 2013

@author: jonathan
'''

class SpatialMap(object):
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = {}
        self.reverse_map = {}
    
    def add(self, entity):
        try:
            grid_squares = self._get_grid_squares((entity.x, entity.y, entity.width, entity.height))
            for square in grid_squares:
                if square in self.map:
                    self.map[square].add(entity)
                else:
                    self.map[square] = {entity}
                
            self.reverse_map[entity] = grid_squares
        except AttributeError:
            pass
                
    def remove(self, entity):
        try:
            for square in self.reverse_map[entity]:
                if square in self.map:
                    self.map[square].discard(entity)          
            
            for square in self._get_grid_squares((entity.x, entity.y, entity.width, entity.height)):
                if square in self.map:
                    self.map[square].discard(entity) 
                
            del self.reverse_map[entity]
        except AttributeError:
            pass
    
    def update(self, entity):
        self.remove(entity)
        self.add(entity)     
    
    def get(self, rect, precise=True):
        possible_intersections = set()
        for square in self._get_grid_squares(rect):
            if square in self.map:
                possible_intersections.update(self.map[square])
        
        if precise:
            intersections = set()
            for entity in possible_intersections:
                entity_rect = (entity.x, entity.y, entity.width, entity.height)
                if self._rects_intersect(rect, entity_rect):
                    intersections.add(entity)
            return intersections

        return possible_intersections
    
    def _rects_intersect(self, a, b):
        a_x, a_y, a_w, a_h = a
        b_x, b_y, b_w, b_h = b
        
        if (a_x > b_x + b_w 
                or b_x > a_x + a_w
                or a_y > b_y + b_h
                or b_y > a_y + a_h):
            return False
        else:
            return True
        
    def _get_grid_squares(self, rect):
        min_grid_x = int(rect[0] / self.grid_size)
        max_grid_x = int((rect[0] + rect[2]) / self.grid_size + 1)
        min_grid_y = int(rect[1] / self.grid_size)
        max_grid_y = int((rect[1] + rect[2]) / self.grid_size + 1)
        return [(x, y) for x in range(min_grid_x, max_grid_x + 1) for y in range(min_grid_y, max_grid_y + 1)]
