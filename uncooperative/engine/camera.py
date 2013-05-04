
class Camera(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_world(self, x, y):
        x_world = self.x + x
        y_world = self.y + y
        return (x_world, y_world)
        
    def to_camera(self, x, y):
        x_camera = x - self.x
        y_camera = y - self.y
        return(x_camera, y_camera)