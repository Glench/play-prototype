import sys
import os

import pygame
import OpenGL.GL as gl

import asyncio
import random

pygame.init()
screen_width, screen_height = 800, 600
# pygame_display = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
_pygame_display = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)


all_sprites = []

_debug = True
def debug(on_or_off):
    global _debug
    if on_or_off == 'on':
        _debug = True
    elif on_or_off == 'off':
        _debug = False

def random_number(lowest=0, highest=100):
    return random.randint(lowest, highest)

def new_sprite(image='cat.png', x=0, y=0, size=1):
    return sprite(image=image, x=x, y=0, size=size)

class sprite(object):
    def __init__(self, image='cat.png', x=0, y=0, size=1):
        self.image = image
        self.x = x
        self.y = y
        self.angle = 0
        self.size = size

        self._pygame_surface = pygame.image.load(os.path.join(image))

        self._when_clicked_callback = None

        all_sprites.append(self)

    def move(self, steps):
        self.x += steps

    def rotate(angle):
        pass

    def go_to(self, sprite_or_x=None, y=None):
        if isinstance(sprite_or_x, sprite):
            self.x = sprite_or_x.x
            self.y = sprite_or_x.y
        else:
            self.x = sprite_or_x
            self.y = y 


    @property 
    def width(self):
        return self._pygame_surface.get_width()

    @property 
    def height(self):
        return self._pygame_surface.get_height()

    @property 
    def right(self):
        return self.x + self.width/2.

    def _pygame_x(self):
        return self.x + (screen_width/2.) - (self._pygame_surface.get_width()/2.)

    def _pygame_y(self):
        return self.y + (screen_height/2.) - (self._pygame_surface.get_height()/2.)

    def when_clicked(self, callback):
        self._when_clicked_callback = callback
        return callback

def new_text(words='hi :)', x=0, y=0, font='Arial.ttf', font_size=20, size=1, color='black'):
    return text(words=words, x=x, y=y, font=font, font_size=font_size, size=size, color=color)

class text(sprite):
    def __init__(self, words='hi :)', x=0, y=0, font='Arial.ttf', font_size=20, size=1, color='black'):
        self.words = words
        self.x = x
        self.y = y
        self.font = font
        self.font_size = font_size
        self.size = size

        self._pygame_font = pygame.font.Font(self.font, self.font_size)
        self._pygame_surface = self._pygame_font.render(words, False, (0, 0, 0))

        self._when_clicked_callback = None

        all_sprites.append(self)



_background_color = [255, 255, 255]
def background_color(color_name=None, red_amount=None, green_amount=None, blue_amount=None):
    if not color_name:
       _background_color[0] = max(red_amount*255, 255)
       _background_color[1] = max(green_amount*255, 255)
       _background_color[2] = max(blue_amount*255, 255)
    else:
        if color_name == 'red':
           _background_color[0] = 255
           _background_color[1] = 0
           _background_color[2] = 0
        elif color_name == 'green':
           _background_color[0] = 0
           _background_color[1] = 255 
           _background_color[2] = 0
        elif color_name == 'blue':
           _background_color[0] = 0
           _background_color[1] = 0 
           _background_color[2] = 255


def when_clicked(sprite):
    def real_decorator(callback):
        sprite.when_clicked(callback)
        return callback
    return real_decorator

def _play_x_to_pygame_x(sprite):
    return sprite.x + (width/2.) - (sprite._pygame_surface.get_width()/2.)

def _play_y_to_pygame_y(sprite):
    return sprite.y + (height/2.) - (sprite._pygame_surface.get_height()/2.)

_loop = asyncio.get_event_loop()
_loop.set_debug(True)

def _game_loop():
    click_detected = False
    click_x = None
    click_y = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_detected = True
            click_x, click_y = event.pos

    _pygame_display.fill(_background_color)

    # BACKGROUND COLOR
    # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
    #       does not support fill() on OpenGL surfaces
    # gl.glClearColor(_background_color[0], _background_color[1], _background_color[2], 1)
    # gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    for sprite in all_sprites:
        if click_detected and sprite._when_clicked_callback:

            if sprite._pygame_surface.get_rect().collidepoint(click_x-sprite._pygame_x(), click_y-sprite._pygame_y()):
                sprite._when_clicked_callback()

        _pygame_display.blit(sprite._pygame_surface, (sprite._pygame_x(), sprite._pygame_y()))

    pygame.display.flip()
    _loop.call_soon(_game_loop)
    return True


async def timer(seconds=1):
    await asyncio.sleep(seconds)
    return True

def repeat_forever(func):

    async def repeat_wrapper():
        await func()
        asyncio.create_task(repeat_wrapper())

    _loop.create_task(repeat_wrapper())
    return func

def when_program_starts(func):
    def wrapper():
        pass
    return func

def start_program():
    _loop.call_soon(_game_loop)
    try:
        _loop.run_forever()
    finally:
        _loop.close()


"""
cool stuff to add:
    scene class, hide and show scenes in one go (collection of sprites)
    mouse down
    mouse move
    mouse hover
    mouse hold
    debug UI for all sprites (bounding box plus values of: x,y,image,size,width,height click state, running commands)
    key pressed
    play.new_rectangle(x=0, y=0, width=100, height=200, color='gray', border_color='red', border_width=1)
    play.new_circle(x=0, y=0, radius=10, border_width=1, border_color='red')
    play.new_line(x=0, y=0, x_end=20, y_end=20, color='black')
    ellipse
    collision system (bouncing balls, platformer)

    glide to
    sprite.transparency(0.5)
    sprite.turn()
    sprite.remove()
    dog.go_to(cat.bottom) # dog.go_to(cat.bottom+5)
    text.font = 'blah', text.font_size = 'blah', text.words = 'blah', all need to have pygame surface recomputed
    sprite.image = 'blah.png" # change_image / animation system / costume, need to have pygame surface recomputed
    play sound / music
    play.music('jam.mp3', loop=False)
    play.volume = 2
    sprite.clone()
    sprite.point_to()
    play.mouse_position()
    sprite.is_touching(cat)
    play.gravity(vertical=1.0, horizontal=0)
    sprite.physics(heaviness=1, shape, x_velocity, y_velocity, obeys_gravity=False, bounces_off_walls=True, bounciness=1.0)
        sprite.physics_off()
        sprite.has_physics()
    sprite.show()/hide() - sprite.is_shown() sprite.is_hidden()
    sprite.size = 2
    play.background_image('backgrounds/waterfall.png', stretch=False, x=0,y=0)
    sprite.distance_to(cat)    # sprite.distance_to(cat.bottom)
    play.random_position()
    play.random_color()
    play.is_key_pressed('right') -> True

    for i in play.seconds(5):
        # loop repeatedly for 5 seconds?
    for count in play.repeat(5):
        # loop 5 times, one iteration per frame

    add images to cache for fast new sprite creation



[x] how to change background color once every half second?
[ ] how to do a series of actions 10 times only? (can't use forever loop. in scratch this would be when (flag) clicked, loop 10 times)
[ ] how to make a text input box simply?
[ ] how to make pong?
[ ] how to make paint app?
[ ] how to make click and drag boxes?
[ ] how to make simple jumping box character with gravity?
[ ] how to make more advanced platformer?

principle:
    - any keyword argument to an object can be set directly e.g.
        cat.x = 5

"""