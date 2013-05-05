import engine
import cProfile

game = engine.get_game()
#cProfile.run('game.run()', filename='profile')
game.run()