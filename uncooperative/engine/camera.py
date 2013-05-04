
class Camera(object):

    def __init__(self, x, y):
    #def __init__(self, player):
        #self.player = player
        self.x_=x
        self.y_=y

    def x(self):
        #return self.player.props.x
        return self.x_

    def y(self):
        #return self.player.props.y
        return self.y_

    def pos(self):
        return (self.x(),self.y())
    
    def to_world(self, x, y):
        x_world = self.x + x
        y_world = self.y + y
        return (x_world, y_world)
        
    def to_camera(self, x, y):
        x_camera = x - self.x
        y_camera = y - self.y
        return(x_camera, y_camera)
