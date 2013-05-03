from grid import Grid
from grid import Vec2
from random import randint
class GridGenerator:
    def __init__(self, grid = Grid(5,5)):
        self.grid = grid
        self.ni = grid.ni
        self.nj = grid.nj

    def makeCircle(self,center,radius):#center: Vec2, radius: Vec2
        for m in range(self.ni):
            for n in range(self.nj):
                if (m-center.x)**2 + (n-center.y)**2 < radius**2:
                    self.grid[m][n] = 0

    def makeSquare(self,corner,side):#center: Vec2, radius: Vec2
        for m in range(side.x):
            for n in range(side.y):
                    self.grid[corner.x+m][corner.y+n] = 0
        

    def randomDepthFirstSearch(self,origin,blocksize):#origin: Vec2, bttomleft: Vec2, topright: Vec2
        path = [origin]
        hasMoves = True
        unvisited = Grid(int(self.ni/blocksize.x),int(self.nj/blocksize.y))

        while 1:
            validMoves = [
                    Vec2(0,1),
                    Vec2(0,-1),
                    Vec2(1,0),
                    Vec2(-1,0)
                    ]

            hasMoved = False
            while len(validMoves) > 0:
                rand = randint(0,len(validMoves)-1)
                diff = validMoves.pop(rand)
                potPos = path[-1] + Vec2(diff.x*2,diff.y*2)
                if potPos.x < 0 or potPos.y < 0:
                    continue
                try:
                    if unvisited.get(potPos) == 1:#can move!
                        unvisited.set(potPos,0)
                        unvisited.set(path[-1] + diff,0)
                        path.append(potPos)
                        hasMoved = True
                        break
                    else:
                        raise IndexError
                except IndexError:
                    continue
            if hasMoved:
                print(unvisited)
                continue
            elif len(path)==1:
                break
            else:
                path.pop()
        for m in range(unvisited.ni):
            for n in range(unvisited.nj):
                for i in range(blocksize.x):
                    for j in range(blocksize.y):
                        try:
                            self.grid[m*blocksize.x + i][n * blocksize.y + j] = unvisited[m][n]
                        except IndexError:
                            continue










