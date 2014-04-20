'''
Created on May 4, 2013

@author: jonathan
'''

class AnimationComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.on_update)
        entity.register_handler('play-animation', self.on_play_animation)
        
        entity.current_animation = 'default'
        entity.animation_pos = 0
        entity.animation_should_loop = True

        entity.image = getattr(entity.animations, entity.current_animation).frames[0]
        
    def remove(self, entity):
        entity.unregister_handler('update', self.on_update)
        entity.unregister_handler('play-animation', self.on_play_animation)
        
    def on_update(self, entity, dt):
        entity.animation_pos += dt
        if entity.animation_pos >= getattr(entity.animations, entity.current_animation).duration:
            if entity.animation_should_loop:
                entity.animation_pos = entity.animation_pos % getattr(entity.animations, entity.current_animation).duration
            else:
                entity.handle('animation-finished', entity.current_animation)
                entity.current_animation = 'default'
                entity.animation_pos = 0
                entity.animation_should_loop = True
        frame_number = int(entity.animation_pos / getattr(entity.animations, entity.current_animation).duration * len(getattr(entity.animations, entity.current_animation).frames))
        entity.image = getattr(entity.animations, entity.current_animation).frames[frame_number]
        
    def on_play_animation(self, entity, animation, loop=False):
        if animation == entity.current_animation and entity.animation_should_loop and loop:
            pass
        else:
            entity.current_animation = animation
            entity.animation_should_loop = loop
            entity.animation_pos = 0
        
        
