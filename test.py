import play

play.set_background_color('white')

cat = play.new_sprite(image='cat.png', x=0, y=0, size=100, transparency=100)
alien = play.new_sprite(image='alien.png', x=0, y=0, size=100, transparency=100)

label = play.new_text(words='meow', x=0, y=0, font='Arial.ttf', font_size=50, color='black', transparency=100)


# TODO:
#   - figure out terminology for rotate, pointing, degrees, turning, angle, etc
#   - fix y axis
#   - implement @when_key_released, @when_any_key_released
#   - experiment with box2d or pymunk
#   - figure out z-ordering, make sure click events work according to that
#   - play.new_rectangle(x=0, y=0, width=100, height=200, color='gray', border_color='red', border_width=1)
#   - play.new_circle(x=0, y=0, radius=10, color='blue', border_width=1, border_color='red')
#   - play.new_line(x=0, y=0, x_end=20, y_end=20, color='black')
#   - sprite.flip_horizontal(), sprite.flip_vertical()
#   - sprite.clone()
#   - class StartScreen(scene)
#   - performance test with lots of sprites
#   - should there be set_size, set_transparency, etc?
#       - shows up in autocomplete / menu
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



@play.repeat_forever
async def do():

    alien.go_to(play.mouse)

    cat.point_towards(play.mouse)


    # fade(cat)
    # fade(alien)
    # fade(label)


# @play.repeat_forever
# async def do():
#     play.set_background_color('blue')
#     await play.timer(seconds=1)

#     play.set_background_color('green')
#     await play.timer(seconds=1)

#     play.set_background_color('red')
#     await play.timer(seconds=1)

@play.when_program_starts
async def do():
    label.words = 'program started!'
    await play.timer(seconds=2)
    label.words = 'meow'


def fade(sprite):
    if not hasattr(sprite, 'fade_out'):
        sprite.fade_out = True

    if sprite.fade_out:
        sprite.transparency -= 1
    else:
        sprite.transparency += 1
    if sprite.transparency == 0 or sprite.transparency == 100:
        sprite.fade_out = not sprite.fade_out




# key_text = play.new_text(words='key pressed: ', x=-200, y=-200, font='Arial.ttf', font_size=20, color='black')
# @play.when_any_key_pressed
# async def do(key):
#     key_text.words = f'key pressed: {key}'

#     if key == 'up':
#         cat.y -= 20
#     if key == 'down':
#         cat.y += 20
#     if key == 'right':
#         cat.x += 20
#     if key == 'left':
#         cat.x -= 20


# @cat.when_clicked
# async def do():
#     label.words = 'cat clicked! :3'

#     if cat.size >= 200:
#         for count in play.repeat(100):
#             if count > 30:
#                 label.words = 100-count
#             cat.size -= 1
#             label.size -= 1
#             await play.animate()
#     else:
#         for count in play.repeat(100):
#             if count > 30:
#                 label.words = count
#             cat.size += 1
#             label.size += 1
#             await play.animate()

#     await play.timer(seconds=.4)
#     label.words = ''

# @play.repeat_forever
# async def do():
#     label.degrees = cat.degrees
#     label.words = cat.distance_to(play.mouse)




play.start_program() # this line should be the last line in your program