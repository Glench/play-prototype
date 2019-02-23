import sys
import os

import pygame
import OpenGL.GL as gl

pygame.init()
width, height = 800, 600
# pygame_display = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
_pygame_display = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)


all_sprites = []

_debug = True
def debug(on_or_off):
    if on_or_off == 'on':
        _debug = True
    elif on_or_off == 'off':
        _debug = False

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
        return self.x + (width/2.) - (self._pygame_surface.get_width()/2.)

    def _pygame_y(self):
        return self.y + (height/2.) - (self._pygame_surface.get_height()/2.)

    def when_clicked(self, callback):
        self._when_clicked_callback = callback
        return callback

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

def when_clicked(sprite):
    def real_decorator(callback):
        sprite.when_clicked(callback)
        return callback
    return real_decorator

def _play_x_to_pygame_x(sprite):
    return sprite.x + (width/2.) - (sprite._pygame_surface.get_width()/2.)

def _play_y_to_pygame_y(sprite):
    return sprite.y + (height/2.) - (sprite._pygame_surface.get_height()/2.)

def forever():
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
    return True

"""
cool stuff to add:
    scene class, hide and show scenes in one go (collection of sprites)
    mouse down
    mouse move
    mouse hover
    mouse hold
    debug UI for all sprites (bounding box plus values of: x,y,image,size,width,height click state, running commands)
    key pressed
    timer(s)
    particle system
    play.rectangle(x=0, y=0, width=100, height=200, color='gray', border_color='red', border_width=1)
    play.circle(x=0, y=0, radius=10, border_width=1, border_color='red')
    ellipse
    line

    glide to
    wait 1 second
    ghost effect
    sprite.turn()
    sprite.remove()
    dog.go_to(cat.bottom)
    text.font = 
    play sound / music
    change sound volume
    sprite.clone()
    sprite.point_to()
    bounce
    sprite.is_touching()
    change_image / animation system / costume
    sprite.show/hide/disable
    sprite.change_size
    background image
    sprite.distance_to()
    play.random_position()
    play.random_color()
    play.random_number(from=0, to=100)


how to make a text input box simply?
how to make pong?
how to make paint app?
how to make click and drag boxes?
how to make simple jumping box with gravity?
how to make more advanced platformer?

"""