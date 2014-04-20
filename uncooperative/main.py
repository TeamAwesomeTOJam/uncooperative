import engine
import cProfile

game = engine.get_game()
#cProfile.Profile.bias = 3.6744963255e-06
#cProfile.run('game.run()', filename='profile')
game.run()