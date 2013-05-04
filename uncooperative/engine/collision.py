'''
Created on May 4, 2013

@author: jonathan
'''

class CollisionGrid(object):
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = {}
    
    def get_grid_squares(self, rect):
        min_grid_x = int(rect[0] / self.grid_size)
        max_grid_x = int((rect[0] + rect[2]) / self.grid_size + 1)
        min_grid_y = int(rect[1] / self.grid_size)
        max_grid_y = int((rect[1] + rect[2]) / self.grid_size + 1)
        return [(x, y) for x in range(min_grid_x, max_grid_x + 1) for y in range(min_grid_y, max_grid_y + 1)]
    
    def add_entity(self, entity):
        for square in self.get_grid_squares_for_entity(entity):
            self.map.setdefault(square, []).append(entity)
                
    def remove_entity(self, entity):
        for square in self.get_grid_squares_for_entity(entity):
            self.map.setdefault(square, []).remove(entity)
    
    def get_possible_collisions(self, rect):
        possible_collisions = []
        for square in self.get_grid_squares(rect):
            if square in self.map:
                possible_collisions += self.map[square]
        return possible_collisions
    
    def get_possible_collisions_for_entity(self, entity):
        return self.get_possible_collisions((entity.props.x, entity.props.y, entity.props.width, entity.props.height))
    
    def get_collisions(self, rect):
        possible_collisions = self.get_possible_collisions(rect)
        collisions = []
        for entity in possible_collisions:
            entity_rect = (entity.props.x, entity.props.y, entity.props.width, entity.props.height)
            if self.rects_collide(rect, entity_rect):
                collisions.append(entity)
        return collisions
             
    def get_collisions_for_entity(self, entity):
        return self.get_collisions((entity.props.x, entity.props.y, entity.props.width, entity.props.height))
    
    def rects_collide(self, a, b):
        a_x, a_y, a_w, a_h = a
        b_x, b_y, b_w, b_h = b
        
        if (a_x > b_x + b_w 
                or b_x > a_x + a_w
                or a_y > b_y + b_h
                or b_y > a_y + a_h):
            return False
        else:
            return True
        