'''
Created on May 4, 2013

@author: jonathan
'''

import game


class AnimationComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.on_update)
        entity.register_handler('play-animation', self.on_play_animation)
        game.get_game().register_for_updates(entity)
        
        entity.props.current_animation = 'default'
        entity.props.animation_pos = 0
        entity.props.animation_should_loop = True
        print entity.props.animations.keys()
        entity.props.image = entity.props.animations[entity.props.current_animation]['frames'][0]
        
    def remove(self, entity):
        entity.unregister_handler('update', self.on_update)
        entity.unregister_handler('play-animation', self.on_play_animation)
        
    def on_update(self, entity, dt):
        entity.props.animation_pos += dt
        if entity.props.animation_pos >= entity.props.animations[entity.props.current_animation]['duration']:
            if entity.props.animation_should_loop:
                entity.props.animation_pos = entity.props.animation_pos % entity.props.animations[entity.props.current_animation]['duration']
            else:
                entity.handle('animation-finished', entity.props.current_animation)
                entity.props.current_animation = entity.props.name+'default'
                entity.props.animation_pos = 0
                entity.props.animation_should_loop = True
        frame_number = int(entity.props.animation_pos / entity.props.animations[entity.props.current_animation]['duration'] * len(entity.props.animations[entity.props.current_animation]['frames']))
        entity.props.image = entity.props.animations[entity.props.current_animation]['frames'][frame_number]
        
    def on_play_animation(self, entity, animation, loop=False):
        entity.props.current_animation = animation
        entity.props.animation_should_loop = loop
        entity.animation_pos = 0
        
        
