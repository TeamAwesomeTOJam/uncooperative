#!/usr/bin/env python2
from grid import Grid
from gridgen import GridGenerator
from grid import Vec2


g = Grid(128,128)

print g
gg = GridGenerator(g)
gg.genMap()
'''
gg.randomDepthFirstSearch(Vec2(0,0),Vec2(7,7))
gg.makeSquare(Vec2(15,35),Vec2(10,10))
gg.makeSquare(Vec2(35,45),Vec2(20,40))
gg.makeSquare(Vec2(15,35),Vec2(50,20))
gg.makeSquare(Vec2(75,95),Vec2(50,10))
gg.makeSquare(Vec2(85,35),Vec2(10,70))
'''
print g
