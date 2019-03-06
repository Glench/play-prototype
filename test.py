import play

cat = play.new_sprite(image='cat.png', x=0, y=0, size=100)

play.set_background_color((255,255,255))

label = play.new_text(words='click this cat!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')


# TODO:
#   - figure out terminology for rotate, pointing, degrees, turning, angle, etc
#   - fix y axis
#   - properly detect keypresses with shift+key, like !
#   - implement @when_key_released, @when_any_key_released
#   - combine rotation/size/transparency image transforms so they work together
#   - combine font/font size/rotation/size image transforms so they work together
#   - experiment with box2d
#   - figure out why click events on text don't work
# boring, easy work:
#   - add all color names (gray/grey, light blue, dark blue)



# TODO: why doesn't this work?
@play.repeat_forever
async def do():
    if play.sprite_is_clicked(cat):
        print('hi')
    if cat.is_clicked():
        print('isclick')

# @cat.when_clicked
# async def do():
#     label.words = ':3'
#     label.degrees = 90
#     label.x = -65
#     label.y = -55
#     label.font_size = 100
#     await play.timer(seconds=2)

#     label.words = 'click this cat!'
#     label.x = 0
#     label.y = 0
#     label.degrees = 0


typed_text = play.new_text(words='', x=-200, y=200, font='Arial.ttf', font_size=20, color=(255,255,255, .3))

@play.when_any_key_pressed
async def do(key):
    if key == 'space':
        key = ' '
    elif key in ['up', 'left', 'down', 'right', 'shift', 'meta', 'super', 'control']:
        key = ''

    if key == 'backspace':
        typed_text.words = typed_text.words[:-1]
    else:
        typed_text.words += key

# key_text = play.new_text(words='keys pressed: ', x=-200, y=-200, font='Arial.ttf', font_size=20, color='black')

# @play.repeat_forever
# async def do():
#     if play.key_is_pressed('up', 'w'):
#         cat.y -= 10

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

# temp_text = play.new_text(words=f'', x=0, y=-150, font='Arial.ttf', font_size=80, color='black')

# @play.when_key_pressed('space', 'backspace')
# async def do(key):
#     temp_text.words = f'{key} pressed!'
#     await play.timer(seconds=1)
#     temp_text.words = ''




# @cat.when_clicked
# async def do():
#     label.words = 'cat clicked! :3'
#     await play.timer(seconds=2)
#     label.words = ''

#     return 
#     if cat.size >= 200:
#         for number in play.repeat(100):
#             cat.increase_size(percent=-1)
#             label.increase_size(percent=-1)
#             await play.next_frame()
#     else:
#         for number in play.repeat(100):
#             cat.increase_size(percent=1)
#             label.increase_size(percent=1)
#             await play.next_frame()
#             # cat.turn(3)

# @play.repeat_forever
# async def do():
#     if key_text.is_clicked(): # FIXME: why doesn't this work?
#         print('hi')

# label.words = ''

# @play.repeat_forever
# async def do():
#     return
#     cat.point_towards(play.mouse)

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