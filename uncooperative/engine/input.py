import pygame

class InputEvent:
    def __init__(self, button, down):
        self.button = button
        self.down = down
        self.up = not down



class InputManager:
    def __init__(self):
        while 1:
            self.init_joystick()
            self.read_joystick()

    def init_joysticks(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

    def read_joystick(self):



