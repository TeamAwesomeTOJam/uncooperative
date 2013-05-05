from grid import Grid
from grid import Vec2
from random import randint, gauss, shuffle
from vec2d import Vec2d


class GridGenerator:
    def __init__(self, gsize = (128,128), blocksize=Vec2(7,7)):
        #print gsize
        self.grid = Grid(gsize[0],gsize[1])
        self.ni = self.grid.ni
        self.nj = self.grid.nj
        self.blocksize = blocksize
        self.roomgridnumtiles = 16

    def makeCircle(self,center,radius):#center: Vec2, radius: Vec2
        for m in range(self.ni):
            for n in range(self.nj):
                if (m-center.x)**2 + (n-center.y)**2 < radius**2:
                    self.grid[m][n] = 0

    def makeSquare(self,center,side):#center: Vec2, radius: Vec2
        for m in range(-side.x,side.x):
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
                                    myrange.y = .2
                                    start.x = move.x * .25 + .5+.5
                                    
                                if move.y != 0:
                                    myrange.x = .2
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
            


    def recurse(self,currentpos):
        centervec = Vec2d(currentpos.x*self.roomgridnumtiles+self.roomgridnumtiles/2,currentpos.y*self.roomgridnumtiles+self.roomgridnumtiles/2)
        
        self.makeSquare(centervec, Vec2d(6,6))
        
        dirs = [Vec2d(1,0),Vec2d(0,1),Vec2d(-1,0),Vec2d(0,-1)]
        shuffle(dirs)
        for d in dirs:
            check = currentpos + d
            #print check.x,check.y
            if check.x < 0 or check.x >= self.roomgridx or check.y < 0 or check.y >= self.roomgridy:
                pass
            elif self.visitedGrid[check.x][check.y]:
                self.visitedGrid[check.x][check.y] = 0
                self.makeSquare(centervec+((self.roomgridnumtiles/2)*d),Vec2d(1,1)+abs(d))
                self.recurse(check)
        

    def genMap(self):
        
        self.roomgridx = self.ni/self.roomgridnumtiles
        self.roomgridy = self.nj/self.roomgridnumtiles
        self.visitedGrid = Grid(self.roomgridx,self.roomgridy)
        currentroomx = self.roomgridx/2
        currentroomy = self.roomgridy/2
        self.recurse(Vec2d(currentroomx,currentroomy))
        
        
        
        
        
        #self.randomDepthFirstSearch()
#         self.makeSquare(Vec2(7,7), Vec2(5,5))
#         roomgridsize = 15
#         roomsizex = 14
#         roomsizey = 14
#         for bigx in range(self.ni/roomgridsize):
#             for bigy in range(self.nj/roomgridsize):
#                 center = Vec2(bigx*roomgridsize+roomgridsize/2,bigy*roomgridsize+roomgridsize/2)
#                 if randint(0,1):
#                     sizex = max(int(7-gauss(0,1)),0)
#                     sizey = max(int(7-gauss(0,1)),0)
#                     shiftx = randint(-1,1)
#                     shifty = randint(-1,1)
#                     self.makeSquare(center, Vec2(roomsizex/2,roomsizey/2))
                #print bigx*self.blocksize.x+self.blocksize.x/2,bigy*self.blocksize.y+self.blocksize.y/2
                #self.makeSquare(Vec2(bigx*self.blocksize.x+self.blocksize.x/2,bigy*self.blocksize.y+self.blocksize.y/2), Vec2(self.blocksize.x-2,self.blocksize.y-2))
#         for times in range(int(self.ni**.7)):
#             self.makeSquare(Vec2(randint(0,self.ni),randint(0,self.ni)),\
#                     Vec2(5*randint(0,int(self.ni/10)),5*randint(0,int(self.nj/10))))
        self.makeSquare(Vec2(self.ni/2,self.nj/2),Vec2(7,7))
        return self.grid







