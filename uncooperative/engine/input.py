import json, os
import pygame, game

def enum(**enums):
    return type("Enum", (), enums)

InputSource = enum(JOYSTICK=1, KEYBOARD=2)

class InputEvent:
    def __init__(self, event):
        """
        @type event: pygame.event.Event
        """
        input_map = game.get_game().resource_manager.get('inputmap', "input")

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
            self.button_down = True
        elif event.type == pygame.JOYBUTTONUP:
            self.button = event.button
            self.button_down = False
        elif event.type == pygame.JOYHATMOTION:
            self.hat = event.hat
            self.value = event.value
        elif event.type == pygame.KEYDOWN:
            self.key = event.key
            self.key_down = True
        elif event.type == pygame.KEYUP:
            self.key = event.key
            self.key_down = False

        for player_number, player_mapping in input_map.iteritems():
            if self.event_source == InputSource.KEYBOARD and self.key_down and player_mapping['type'] == "KEYBOARD":
                if player_mapping[self.key]:
                    self.action = player_mapping[self.key]
                    if self.action == "UP" or self.action == "RIGHT":
                        self.magnitude = 1
                    else:
                        self.magnitude = -1

                    self.player = player_number
                    return
            elif self.event_source == InputSource.JOYSTICK and player_mapping['type'] == "JOYSTICK":
                if player_mapping["joystick"] == self.joy:
                    self.player = player_number
                    if self.button_down and self.button == player_mapping[self.button]:
                        self.action = player_mapping[self.button]
                        return
                    elif self.axis == 0 or self.hat == 0:
                        if self.value > 0:
                            self.action = "UP"
                            self.magnitude = self.value
                            return
                        elif self.value < 0:
                            self.action = "DOWN"
                            self.magnitude = self.value
                            return
                    elif self.axis == 1 or self.hat == 1:
                        if self.value > 0:
                            self.action = "RIGHT"
                            self.magnitude = self.value
                            return
                        elif self.value < 0:
                            self.action = "LEFT"
                            self.magnitude = self.value
                            return


class InputManager:
    def __init__(self):
        pass

    def init_joysticks(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
