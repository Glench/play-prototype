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

        self._is_clicked = False

        self._pygame_surface_original = pygame.image.load(os.path.join(image)).convert()
        self._pygame_surface_original.set_colorkey((255,255,255)) # set background to transparent
        self._pygame_surface = self._pygame_surface_original

        self._when_clicked_callbacks = []

        all_sprites.append(self)

    def is_clicked(self):
        return self._is_clicked

    def move(self, steps):
        self.x += steps

    def turn(self, degrees=10):
        self.degrees = self.degrees + degrees

    @property 
    def degrees(self):
        return self._degrees

    @degrees.setter
    def degrees(self, _degrees):
        self._degrees = _degrees
        self._pygame_surface = pygame.transform.rotate(self._pygame_surface_original, self._degrees*-1)

    def point_towards(self, angle):
        try:
            x, y = angle.x, angle.y
            self.degrees = math.degrees(math.atan2(y-self.y, x-self.x))
        except AttributeError:
            self.degrees = angle

    def increase_size(self, percent=10):
        self.size += percent
        ratio = self.size/100.
        self._pygame_surface = pygame.transform.scale(self._pygame_surface_original,
            (round(self._pygame_surface_original.get_width() * ratio), round(self._pygame_surface_original.get_height() * ratio)))

    def go_to(self, sprite_or_x=None, y=None):
        """
        Example:

            # text will follow around the mouse
            text = play.new_text(words='yay', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

            @play.repeat_forever
            async def do():
                text.go_to(play.mouse)
        """
        assert(not sprite_or_x is None)

        try:
            self.x = sprite_or_x.x
            self.y = sprite_or_x.y
        except AttributeError:
            self.x = sprite_or_x
            self.y = y 

    def distance_to(self, sprite_or_x=None, y=None):
        assert(not sprite_or_x is None)

        try:
            x = sprite_or_x.x
            y = sprite_or_x.y
        except AttributeError:
            x = sprite_or_x
            y = y

        dx = self.x - x
        dy = self.y - y

        return math.sqrt(dx**2 + dy**2)


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

    def when_clicked(self, async_callback):
        async def wrapper():
            wrapper.is_running = True
            await async_callback()
            wrapper.is_running = False
        wrapper.is_running = False
        self._when_clicked_callbacks.append(wrapper)
        return wrapper

class _mouse(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self._is_clicked = False
        self._when_clicked_callbacks = []

    def is_clicked(self):
        return self._is_clicked

    def when_clicked(self, async_callback):
        async def wrapper():
            wrapper.is_running = True
            await async_callback()
            wrapper.is_running = False
        wrapper.is_running = False
        self._when_clicked_callbacks.append(wrapper)
        return wrapper

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
        self._color = color

        self._is_clicked = False

        self._pygame_font = pygame.font.Font(self.font, self.font_size)
        self._pygame_surface_original = self._pygame_font.render(self._words, False, color_name_to_rgb(self.color))
        self._pygame_surface = self._pygame_surface_original

        self._when_clicked_callbacks = []

        all_sprites.append(self)

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, string):
        self._words = str(string)
        self._pygame_surface_original = self._pygame_font.render(self._words, False, color_name_to_rgb(self.color))
        self._pygame_surface = self._pygame_surface_original

    @property 
    def color(self):
        return self._color

    @color.setter
    def set_color(self, color):
        self._color = color
        self._pygame_surface_original = self._pygame_font.render(self._words, False, color_name_to_rgb(self.color))
        self._pygame_surface = self._pygame_surface_original




background_color = (255, 255, 255)
def set_background_color(color):
    global background_color

    # I chose to make set_background_color a function so that we can give
    # good error messages at the call site if a color isn't recognized.
    # If we didn't have a function and just set background_color like this:
    #
    #       play.background_color = 'gbluereen'
    #
    # then any errors resulting from that statement would appear somewhere
    # deep in this library instead of in the user code.

    if type(color) == tuple:
        background_color = color
    else:
        background_color = color_name_to_rgb(color)

def when_clicked(*sprites):
    # TODO
    for sprite in sprites:
        sprite.when_clicked(callback)
    return real_decorator

pygame.key.set_repeat(200, 16)
_pressed_keys = set()
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
    """
    Returns True if any of the keys are pressed.

    Example:

        @repeat_forever
        async def do():
            if play.is_key_pressed('up', 'w'):
                print('up or w pressed')
    """
    for key in keys:
        if key in _pressed_keys:
            return True
    return False

def _play_x_to_pygame_x(sprite):
    return sprite.x + (width/2.) - (sprite._pygame_surface.get_width()/2.)

def _play_y_to_pygame_y(sprite):
    return sprite.y + (height/2.) - (sprite._pygame_surface.get_height()/2.)

_loop = asyncio.get_event_loop()
_loop.set_debug(True)

_keys_pressed_this_frame = []
def _game_loop():
    _keys_pressed_this_frame.clear() # do this instead of `keys_pressed_this_frame = []` to save memory

    click_happened_this_frame = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_happened_this_frame = True
            mouse._is_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse._is_clicked = False
        if event.type == pygame.MOUSEMOTION:
            mouse.x, mouse.y = event.pos[0] - screen_width/2., event.pos[1] - screen_height/2.
        if event.type == pygame.KEYDOWN:
            _pressed_keys.add(pygame_key_to_name(event.key))
            _keys_pressed_this_frame.append(pygame_key_to_name(event.key))
        if event.type == pygame.KEYUP:
            _pressed_keys.remove(pygame_key_to_name(event.key))



    ####################################
    # @when_any_key_pressed callbacks
    ####################################
    if _pressed_keys:
        for key in _keys_pressed_this_frame:
            for callback in _keypress_callbacks:
                if not callback.is_running and (callback.keys is None or key in callback.keys):
                    _loop.create_task(callback(key))


    ####################################
    # @mouse.when_clicked callbacks
    ####################################
    if click_happened_this_frame and mouse._when_clicked_callbacks:
        for callback in mouse._when_clicked_callbacks:
            if not callback.is_running:
                _loop.create_task(callback())


    #############################
    # @repeat_forever callbacks
    #############################
    for callback in _repeat_forever_callbacks:
        if not callback.is_running:
            _loop.create_task(callback())

    # 1.  get pygame events
    #       - set mouse position, clicked, keys pressed, keys released
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



    _pygame_display.fill(color_name_to_rgb(background_color))

    # BACKGROUND COLOR
    # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
    #       does not support fill() on OpenGL surfaces
    # gl.glClearColor(_background_color[0], _background_color[1], _background_color[2], 1)
    # gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    for sprite in all_sprites:

        #################################
        # @sprite.when_clicked events
        #################################
        sprite._is_clicked = False
        if mouse.is_clicked() and sprite._when_clicked_callbacks:
            # get_rect().collidepoint() is local coordinates, e.g. 100x100 image, so have to translate
            if sprite._pygame_surface.get_rect().collidepoint((mouse.x+screen_width/2.)-sprite._pygame_x(), (mouse.y+screen_height/2.)-sprite._pygame_y()):
                sprite._is_clicked = True

                # only run sprite clicks on the frame the mouse was clicked
                if click_happened_this_frame:
                    for callback in sprite._when_clicked_callbacks:
                        if not callback.is_running:
                            _loop.create_task(callback())

        _pygame_display.blit(sprite._pygame_surface, (sprite._pygame_x(), sprite._pygame_y()))

    pygame.display.flip()
    _loop.call_soon(_game_loop)
    return True


async def timer(seconds=1):
    await asyncio.sleep(seconds)
    return True

async def next_frame():
    await asyncio.sleep(0)

_repeat_forever_callbacks = []
def repeat_forever(func):
    """
    Calls the given function repeatedly.

    Example:

        text = play.new_text(words='hi there!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

        @play.repeat_forever
        async def do():
            text.turn(degrees=15)

    """
    async def repeat_wrapper():
        repeat_wrapper.is_running = True
        await func()
        repeat_wrapper.is_running = False

    repeat_wrapper.is_running = False
    _repeat_forever_callbacks.append(repeat_wrapper)
    return func


_when_program_starts_callbacks = []
def when_program_starts(func):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    _when_program_starts_callbacks.append(wrapper)
    return func

def repeat(number_of_times):
    return range(1, number_of_times+1)

def start_program():
    for func in _when_program_starts_callbacks:
        _loop.create_task(func())

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
    play.new_circle(x=0, y=0, radius=10, color='blue', border_width=1, border_color='red')
    play.new_line(x=0, y=0, x_end=20, y_end=20, color='black')
    ellipse
    collision system (bouncing balls, platformer)
    play.mouse.is_touching() # cat.go_to(play.mouse)
    @sprite.when_touched

    sprite.glide_to(other_sprite, seconds=1)
    sprite.transparency(0.5)
    sprite.remove()
    dog.go_to(cat.bottom) # dog.go_to(cat.bottom+5)
    text.font = 'blah', text.font_size = 'blah', text.words = 'blah', all need to have pygame surface recomputed
    sprite.image = 'blah.png", sprite.size, sprite.angle, sprite.transparency # change_image / animation system / costume, need to have pygame surface recomputed
    play sound / music
    play.music('jam.mp3', loop=False)
    play.stop_music('jam.mp3')
    play.sound('jam.mp3')
    play.volume = 2
    sprite.clone()
    sprite.is_touching(cat)
    play.gravity(vertical=1.0, horizontal=0)
    sprite.physics( x_velocity, y_velocity, obeys_gravity=True, bounces_off_walls=True, heaviness=1, bounciness=1.0)
        sprite.physics_off()
        sprite.is_physics_on()
        box2d is_fixed_rotation good for platformers
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