from collections import namedtuple

import pygame

import game


DEADZONE = 0.15


InputEvent = namedtuple('InputEvent', ['player', 'control', 'value'])


class InputManager:

    def __init__(self):
        self._input_map = None
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

    def init_joysticks(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            
    def process_events(self):
        self._input_map = game.get_game().resource_manager.get('inputmap', 'default')
        processed_events = []
        
        for e in pygame.event.get():
            if e.type == pygame.JOYAXISMOTION:
                event_type = 'AXIS'
                device_id = e.which
                value, _ = self._normalize_axis(e.value, 0)
                if value >= 0:
                    event = self._new_event(event_type, device_id, "+%d" % e.axis, value)
                if value <= 0:
                    value = -1 * value
                    event =  self._new_event(event_type, device_id, "-%d" % e.axis, value)
                if event != None:
                    processed_events.append(event) 
            elif e.type == pygame.JOYBUTTONDOWN:
                event = self._new_event('BUTTON', e.which, e.button, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == pygame.JOYBUTTONUP:
                event = self._new_event('BUTTON', e.which, e.button, 0)
                if event != None:
                    processed_events.append(event)
            elif e.type == pygame.KEYDOWN:
                event = self._new_event('KEY', None, e.key, 1)
                if event != None:
                    processed_events.append(event)
            elif e.type == pygame.KEYUP:
                event = self._new_event('KEY', None, e.key, 0)
                if event != None:
                    processed_events.append(event)
            elif e.type == pygame.JOYHATMOTION:
                pass # TODO: this is going to get complicated
            else:
                pass
        
        return processed_events
    
    def _new_event(self, event_type, device_id, device_control, value):
        if device_id == None:
            pandc = self._input_map.get('%s %s' % (event_type, device_control))
        else:
            pandc = self._input_map.get('%s %s %s' % (event_type, device_id, device_control))
        
        if pandc == None:
            return None
        else:
            player, control = pandc
            return InputEvent(player, control, value)
    
    def _normalize_axis(self, x, y):              
        magnitude = ((x**2) + (y**2)) ** 0.5

        if magnitude < DEADZONE:
            new_x = 0
            new_y = 0
        else:
            new_x = (x / magnitude) * (magnitude - DEADZONE) / (1 - DEADZONE)
            new_y = (y / magnitude) * (magnitude - DEADZONE) / (1 - DEADZONE)
        
        return new_x, new_y
