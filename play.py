import sys
import os

import pygame
import OpenGL.GL as gl

import asyncio
import random
import math

from keypress import pygame_key_to_name
from color import color_name_to_rgb

pygame = pygame
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

def new_sprite(image='cat.png', x=0, y=0, size=100):
    return sprite(image=image, x=x, y=0, size=size)

class sprite(object):
    def __init__(self, image='cat.png', x=0, y=0, size=100):
        self.image = image
        self.x = x
        self.y = y
        self._degrees = 0
        self.size = size


        self._pygame_surface_original = pygame.image.load(os.path.join(image)).convert()
        self._pygame_surface_original.set_colorkey((255,255,255)) # set background to transparent
        self._pygame_surface = self._pygame_surface_original

        self._when_clicked_callback = None

        all_sprites.append(self)

    def move(self, steps):
        self.x += steps

    def turn(self, degrees=10):
        self._degrees += degrees
        self._pygame_surface = pygame.transform.rotate(self._pygame_surface_original, self._degrees*-1)

    @property 
    def degrees(self):
        return self._degrees

    @degrees.setter
    def degrees(self, _degrees):
        self._degrees = _degrees
        self._pygame_surface = pygame.transform.rotate(self._pygame_surface_original, self._degrees*-1)

    def point_towards(self, angle):
        if isinstance(angle, sprite) or isinstance(angle, _mouse):
            x, y = angle.x, angle.y
            self._degrees = math.degrees(math.atan2(y, x))
        else:
            self._degrees = angle
        self._pygame_surface = pygame.transform.rotate(self._pygame_surface_original, self._degrees*-1)

    def increase_size(self, percent=10):
        self.size += percent
        ratio = self.size/100.
        self._pygame_surface = pygame.transform.scale(self._pygame_surface_original,
            (round(self._pygame_surface_original.get_width() * ratio), round(self._pygame_surface_original.get_height() * ratio)))

    def go_to(self, sprite_or_x=None, y=None):
        if isinstance(sprite_or_x, sprite) or isinstance(sprite_or_x, _mouse):
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

class _mouse(object):
    x = 0
    y = 0

mouse = _mouse()

def new_text(words='hi :)', x=0, y=0, font='Arial.ttf', font_size=20, color='black'):
    return text(words=words, x=x, y=y, font=font, font_size=font_size, size=100, color=color)

class text(sprite):
    def __init__(self, words='hi :)', x=0, y=0, font='Arial.ttf', font_size=20, size=100, color='black'):
        self._words = words
        self.x = x
        self.y = y
        self.font = font
        self.font_size = font_size
        self.size = size

        self._pygame_font = pygame.font.Font(self.font, self.font_size)
        self._pygame_surface_original = self._pygame_font.render(self._words, False, (0, 0, 0))
        self._pygame_surface = self._pygame_surface_original

        self._when_clicked_callback = None

        all_sprites.append(self)

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, string):
        self._words = string
        self._pygame_surface_original = self._pygame_font.render(self._words, False, (0, 0, 0))
        self._pygame_surface = self._pygame_surface_original




_background_color = (255, 255, 255)
def background_color(color=None, red_amount=None, green_amount=None, blue_amount=None):
    global _background_color
    if not color:
        _background_color = (
            max(red_amount*255, 255), 
            max(green_amount*255, 255),
            max(blue_amount*255, 255)
        )
    elif isinstance(color, tuple):
        _background_color = color
    else:
        _background_color = color_name_to_rgb(color)

def when_clicked(sprite):
    def real_decorator(callback):
        sprite.when_clicked(callback)
        return callback
    return real_decorator

pygame.key.set_repeat(100, 16)
_pressed_keys = []
_keypress_callbacks = []

def when_any_key_pressed(func):
    async def wrapper(*args, **kwargs):
        wrapper.is_running = True
        await func(*args, **kwargs)
        wrapper.is_running = False
    wrapper.keys = None
    wrapper.is_running = False
    _keypress_callbacks.append(wrapper)
    return wrapper

def when_key_pressed(*keys):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await func(*args, **kwargs)
            wrapper.is_running = False
        wrapper.keys = keys
        wrapper.is_running = False
        _keypress_callbacks.append(wrapper)
        return wrapper
    return decorator

def is_key_pressed(*keys):
    for key in keys:
        if key in _pressed_keys:
            return True
    return False

def repeat_forever(func):

    async def repeat_wrapper():
        await func()
        asyncio.create_task(repeat_wrapper())

    _loop.create_task(repeat_wrapper())
    return func

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
    global _pressed_keys
    _pressed_keys.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_detected = True
            click_x, click_y = event.pos
        if event.type == pygame.MOUSEMOTION:
            mouse.x, mouse.y = event.pos[0] - screen_width/2., event.pos[1] - screen_height/2.
        if event.type == pygame.KEYDOWN:
            _pressed_keys.append(pygame_key_to_name(event.key))


    if _pressed_keys:
        for key in _pressed_keys:
            for callback in _keypress_callbacks:
                if not callback.is_running and (callback.keys is None or key in callback.keys):
                    _loop.create_task(callback(key))
    # 1.  get pygame events
    #       - set mouse position, clicked, keys pressed
    # 2.  run when_program_starts callbacks
    # 3.  run physics simulation
    # 4.  compute new pygame_surfaces (scale, rotate)
    # 5.  run repeat_forever callbacks
    # 6.  run mouse/click callbacks (make sure more than one isn't running at a time)
    # 7.  run keyboard callbacks (make sure more than one isn't running at a time)
    # 8.  run when_touched callbacks
    # 9.  render background
    # 10. render sprites (with correct z-order)
    # 11. call event loop again


    _pygame_display.fill(_background_color)

    # BACKGROUND COLOR
    # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
    #       does not support fill() on OpenGL surfaces
    # gl.glClearColor(_background_color[0], _background_color[1], _background_color[2], 1)
    # gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    for sprite in all_sprites:
        if click_detected and sprite._when_clicked_callback:

            if sprite._pygame_surface.get_rect().collidepoint(click_x-sprite._pygame_x(), click_y-sprite._pygame_y()):
                _loop.create_task(sprite._when_clicked_callback())
                # sprite._when_clicked_callback()

        _pygame_display.blit(sprite._pygame_surface, (sprite._pygame_x(), sprite._pygame_y()))

    pygame.display.flip()
    _loop.call_soon(_game_loop)
    return True


async def timer(seconds=1):
    await asyncio.sleep(seconds)
    return True

async def next_frame():
    await asyncio.sleep(0)

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

def repeat(number_of_times):
    return range(1, number_of_times+1)
    # set global queuing flag
    # for x in range(1, number_of_times+1):
    #     await asyncio.sleep(0)
    #     yield x
    # return 

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
    play.mouse.is_touching() # cat.go_to(play.mouse)
    @sprite.when_touched

    sprite.glide_to(other_sprite, seconds=1)
    sprite.transparency(0.5)
    sprite.turn()
    sprite.remove()
    dog.go_to(cat.bottom) # dog.go_to(cat.bottom+5)
    text.font = 'blah', text.font_size = 'blah', text.words = 'blah', all need to have pygame surface recomputed
    sprite.image = 'blah.png", sprite.size, sprite.angle # change_image / animation system / costume, need to have pygame surface recomputed
    play sound / music
    play.music('jam.mp3', loop=False)
    play.stop_music('jam.mp3')
    play.sound('jam.mp3')
    play.volume = 2
    sprite.clone()
    sprite.point_to()
    play.mouse_position()
    sprite.is_touching(cat)
    play.gravity(vertical=1.0, horizontal=0)
    sprite.physics( x_velocity, y_velocity, obeys_gravity=True, bounces_off_walls=True, heaviness=1, bounciness=1.0)
        sprite.physics_off()
        sprite.is_physics_on()
    sprite.show()/hide() - sprite.is_shown() sprite.is_hidden()
    sprite.size = 2
    play.background_image('backgrounds/waterfall.png', fit_to_screen=False, x=0,y=0)
    sprite.distance_to(cat)    # sprite.distance_to(cat.bottom)
    play.random_position()
    play.random_color()
    play.is_key_pressed('right') -> True
    sprite.flip(direction='left') sprite.flip(direction='down')

    for i in play.seconds(5):
        # loop repeatedly for 5 seconds?

    add images to cache for fast new sprite creation
    figure out how to make fonts look better



[x] how to change background color once every half second?
[x] how to do a series of actions 10 times only? (can't use forever loop. in scratch this would be when (flag) clicked, loop 10 times)
[ ] how to make a text input box simply?
[ ] how to make pong?
[ ] how to make paint app?
[ ] how to make click and drag boxes?
[ ] how to make simple jumping box character with gravity?
[ ] how to make more advanced platformer?
[ ] how to make shooter? http://osmstudios.com/tutorials/your-first-love2d-game-in-200-lines-part-1-of-3
[ ] how to make point and click tic-tac-toe?

funny game idea: pong game where paddle shrinks unless you get powerups that spawn randomly in your zone

principle:
    - any keyword argument to an object can be set directly e.g.
        cat = play.new_sprite(image='cat.png', x=0, y=0, ...)
        cat.image = 'cat_with_tongue.png'
        cat.x += 5
        cat.y = 5

"""