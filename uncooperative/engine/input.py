import pygame

def enum(**enums):
    return type("Enum", (), enums)

InputSource = enum(JOYSTICK=1, KEYBOARD=2)

class InputEvent:
    def __init__(self, event):
        """
        @type event: pygame.event.Event
        """
        self.event = event
        if event.type == pygame.JOYAXISMOTION or \
                event.type == pygame.JOYBALLMOTION or \
                event.type == pygame.JOYBUTTONDOWN or \
                event.type == pygame.JOYBUTTONUP or \
                event.type == pygame.JOYHATMOTION:
            self.event_source = InputSource.JOYSTICK
            self.joy = event.joy
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.KEYUP:
            self.event_source = InputSource.KEYBOARD


        if event.type == pygame.JOYAXISMOTION:
            self.axis = event.axis
            self.value = event.value
        elif event.type == pygame.JOYBALLMOTION:
            self.ball = event.ball
            self.rel = event.rel
        elif event.type == pygame.JOYBUTTONDOWN:
            self.button = event.button
        elif event.type == pygame.JOYBUTTONUP:
            self.button = event.button
        elif event.type == pygame.JOYHATMOTION:
            self.hat = event.hat
            self.value = event.value
        elif event.type == pygame.KEYDOWN:
            self.key = event.key
        elif event.type == pygame.KEYUP:
            self.key = event.key


class InputManager:
    def __init__(self):
        pass

    def init_joysticks(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()



