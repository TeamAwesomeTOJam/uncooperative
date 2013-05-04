from grid import Grid
from grid import Vec2
from random import randint
class GridGenerator:
    def __init__(self, grid = Grid(128,128), blocksize=Vec2(7,7)):
        self.grid = grid
        self.ni = grid.ni
        self.nj = grid.nj
        self.blocksize = blocksize

    def makeCircle(self,center,radius):#center: Vec2, radius: Vec2
        for m in range(self.ni):
            for n in range(self.nj):
                if (m-center.x)**2 + (n-center.y)**2 < radius**2:
                    self.grid[m][n] = 0

    def makeSquare(self,center,side):#center: Vec2, radius: Vec2
        for m in range(side.y,side.x):
            for n in range(-side.y,side.y):
                try:
                    self.grid[center.x+m][center.y+n] = 0
                except IndexError:
                    continue
        

    def randomDepthFirstSearch(self):
        path = [Vec2(0,0)]
        hasMoves = True
        unvisited = Grid(int(self.ni/self.blocksize.x),int(self.nj/self.blocksize.y))

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
                continue
            elif len(path)==1:
                break
            else:
                path.pop()
        moves = [
                Vec2(0,1),
                Vec2(0,-1),
                Vec2(1,0),
                Vec2(-1,0)
                ]
        for m in range(unvisited.ni):
            for n in range(unvisited.nj):
                mypos = Vec2(m,n)
                myval = unvisited[m][n]
                if myval == 0:
                    for move in moves:
                        try:
                            theirval = unvisited.get(mypos+move)
                            if theirval == 0:
                                #this is all arbitray positioning stuff :)
                                myrange = Vec2(.3, .3)
                                start = Vec2(1,1)
                                if move.x != 0:
                                    myrange.y = .3
                                    start.x = move.x * .25 + .5+.5
                                    
                                if move.y != 0:
                                    myrange.x = .3
                                    start.y = move.y * .25 + .5+.5
                                
    
    
                                myrange = Vec2(int(myrange.x * self.blocksize.x), int(myrange.y * self.blocksize.y))
                                start = Vec2(int(start.x * self.blocksize.x), int(start.y *self.blocksize.y))
                                for i in range(-myrange.x,myrange.x):
                                    for j in range(-myrange.y,myrange.y):
                                        try:
                                            pos = Vec2(m*self.blocksize.x + start.x + i,n * self.blocksize.y +start.y + j)
                
                                            self.grid.set(pos,myval)
                                        except IndexError:
                                            continue
                        except IndexError:
                            continue
            



    def genMap(self):
        self.randomDepthFirstSearch()
        for times in range(int(self.ni**.7)):
            self.makeSquare(Vec2(randint(0,self.ni),randint(0,self.ni)),\
                    Vec2(5*randint(0,int(self.ni/10)),5*randint(0,int(self.nj/10))))







