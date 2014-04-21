import cProfile
import os
import sys

import engine


def run(profile=False):
    game = engine.get_game((1280,720), os.path.join(sys.path[0], 'res'))
    
    if profile:
        cProfile.Profile.bias = 3.6744963255e-06
        cProfile.run('game.run(engine.AttractMode())', filename='profile')
    else:
        game.run(engine.AttractMode())