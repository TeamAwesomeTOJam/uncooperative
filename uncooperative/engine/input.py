import pygame, game

def enum(**enums):
    return type("Enum", (), enums)

InputSource = enum(JOYSTICK=1, KEYBOARD=2)

class InputEvent:
    def __init__(self, event, **kwargs):
        """
        @type event: pygame.event.Event
        """
        input_map = game.get_game().resource_manager.get('inputmap', "input")

        self.event = event
        self.event_source, self.joy, self.axis, self.value = None, None, None, None
        self.ball, self.rel, self.button, self.button_down = None, None, None, None
        self.hat, self.action, self.magnitude = None, None, None
        self.key_up, self.key_down = None, None

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
            if self.event_source == InputSource.KEYBOARD and player_mapping['input'] == "KEYBOARD":
                string_key = pygame.key.name(self.key)
                if player_mapping.get(string_key):
                    self.action = player_mapping[string_key]
                    if self.action == "DOWN" or self.action == "RIGHT":
                        if self.key_down:
                            self.magnitude = 1
                        else:
                            self.magnitude = 0
                    else:
                        if self.key_down:
                            self.magnitude = -1
                        else:
                            self.magnitude = 0
                    if self.action == "UP" or self.action == "DOWN":
                        self.axis = 1
                    else:
                        self.axis = 0

                    self.player = player_number
                    return
            elif self.event_source == InputSource.JOYSTICK and player_mapping['input'] == "JOYSTICK":
                if player_mapping.get("joystick") == self.joy:
                    self.player = player_number
                    if self.hat == player_mapping['hat']:
                        if kwargs["axis"] is not None:
                            self.axis = kwargs["axis"]
                            self.value = event.value[kwargs["axis"]]
                            if self.axis == 1:
                                self.value = -1 * self.value
                    
                    action = player_mapping.get(str(self.button))
                    if action:
                        self.action = action

                    if self.axis == 0:
                        if self.value >= 0:
                            self.action = "UP"
                            self.magnitude = self.value
                            return
                        elif self.value < 0:
                            self.action = "DOWN"
                            self.magnitude = self.value
                            return
                    elif self.axis == 1:
                        if self.value >= 0:
                            self.action = "RIGHT"
                            self.magnitude = self.value
                            return
                        elif self.value < 0:
                            self.action = "LEFT"
                            self.magnitude = self.value
                            return
                    
                    if self.button is not None and self.button == player_mapping.get(self.button):
                        self.action = player_mapping[self.button]
                        return

def create_input_events(event):
    events = []
    if event.type == pygame.JOYHATMOTION:
        events.append(InputEvent(event, axis=0))
        events.append(InputEvent(event, axis=1))
    else:
        events.append(InputEvent(event))
    
    return events

class InputManager:
    def __init__(self):
        pass

    def init_joysticks(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
