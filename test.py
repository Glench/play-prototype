import play

play.set_background_color('black')

cat = play.new_sprite(image='cat.png', x=0, y=0, size=100, transparency=50)
alien = play.new_sprite(image='alien.png', x=0, y=0, size=100, transparency=51)

label = play.new_text(words='meow', x=0, y=0, font='Arial.ttf', font_size=120, color='blue', transparency=50)


# TODO:
#   - figure out terminology for rotate, pointing, degrees, turning, angle, etc
#   - fix y axis
#   - implement @when_key_released, @when_any_key_released
#   - experiment with box2d or pymunk
#   - figure out z-ordering, make sure click events work according to that
#   - play.new_rectangle(x=0, y=0, width=100, height=200, color='gray', border_color='red', border_width=1)
#   - play.new_circle(x=0, y=0, radius=10, color='blue', border_width=1, border_color='red')
#   - play.new_line(x=0, y=0, x_end=20, y_end=20, color='black')
#   - redo transparency like pygame zero: https://pygame-zero.readthedocs.io/en/stable/ptext.html
#   - performance test with lots of sprites
# boring, easy work:
#   - add all color names (gray/grey, light blue, dark blue)
#   - warn on sprite being set too small

# @cat.when_clicked
# @play.when_sprite_clicked(cat) TODO use `inspect` to allow using argument or not: inspect.getfullargspec(aMethod): https://stackoverflow.com/questions/218616/getting-method-parameter-names-in-python
# play.sprite_is_clicked(cat)

# @play.when_mouse_clicked
# @play.mouse.when_clicked
# play.mouse_is_clicked()
# play.mouse.is_clicked()

# @sprite.when_click_released
# play.mouse.when_click_released

def fade(sprite):
    if not hasattr(sprite, 'fade_out'):
        sprite.fade_out = True

    if sprite.fade_out:
        sprite.transparency -= 1
    else:
        sprite.transparency += 1
    if sprite.transparency == 0 or sprite.transparency == 100:
        sprite.fade_out = not sprite.fade_out


@play.repeat_forever
async def do():
    alien.go_to(play.mouse)

    cat.point_towards(play.mouse)

    fade(cat)
    fade(alien)
    fade(label)

@cat.when_clicked
async def do():
    label.words = 'clicked'
    for number in play.repeat(100):
        cat.size += 1
        await play.animate()

# @play.repeat_forever
# async def do():
#     play.set_background_color('blue')
#     await play.timer(seconds=1)
#     play.set_background_color('green')
#     await play.timer(seconds=1)
#     play.set_background_color('red')
#     await play.timer(seconds=1)



# @play.when_program_starts
# async def do():
#     await play.timer(seconds=1)
#     cat.transparency = 50
#     await play.timer(seconds=1)
#     cat.transparency = 100
#     label.transparency = 0


# key_text = play.new_text(words='key pressed: ', x=-200, y=-200, font='Arial.ttf', font_size=20, color='black')

# @play.when_any_key_pressed
# async def do(key):
#     key_text.words = f'key pressed: {key}'

    # if key == 'up':
    #     cat.y -= 20
    # if key == 'down':
    #     cat.y += 20
    # if key == 'right':
    #     cat.x += 20
    # if key == 'left':
    #     cat.x -= 20


# @cat.when_clicked
# async def do():
#     label.words = 'cat clicked! :3'

#     if cat.size >= 200:
#         for number in play.repeat(100):
#             cat.size -= 1
#             label.size -= 1
#             await play.next_frame()
#     else:
#         for number in play.repeat(100):
#             label.words = number
#             cat.size += 1
#             label.size += 1
#             await play.next_frame()

#     label.words = ''

# @play.repeat_forever
# async def do():
#     if key_text.is_clicked(): # FIXME: why doesn't this work?
#         print('hi')

# label.words = ''


#     label.go_to(cat)

    # FIXME: switching the order of these two statements causes the text not to rotate 
    # label.words = cat.distance_to(play.mouse)
    # label.degrees = cat.degrees

# cat.should_move_forward = 1

# @play.repeat_forever
# async def do():
#     cat.move(3*cat.should_move_forward)
#     cat.turn(degrees=3*cat.should_move_forward)    
#     if cat.x > play.screen_width/2.:
#         cat.should_move_forward = -1
#     elif cat.x < play.screen_width/-2.:
#         cat.should_move_forward = 1

#     label.go_to(cat)
#     label.turn_toward(cat.degrees)


# @play.repeat_forever
# async def do():

#     play.set_background_color('red')
#     await play.timer(seconds=1)

#     play.set_background_color('green')
#     await play.timer(seconds=1)

#     play.set_background_color('blue')
#     await play.timer(seconds=1)

play.start_program() # this line should be the last line in your program