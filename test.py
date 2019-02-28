import play

play.background_color(red_amount=1.0, blue_amount=1.0, green_amount=1.0)

cat = play.new_sprite(image='cat.png', x=0, y=0, size=100)

label = play.new_text(words='click this cat!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

key_text = play.new_text(words='last key pressed: ', x=-200, y=-200, font='Arial.ttf', font_size=20, color='white')

# TODO:
#   - figure out terminology for rotate, pointing, degrees, turning, angle, etc
#   - implement `when_program_starts`
#   - refactor event loop
#   - @play.when_key_pressed
#       - properly detect keypresses with shift+key
#       - how to deal with held-down key?
#       - how to deal with multiple keys pressed
#   - @play.when_key_pressed('up')
#   - @play.when_keys_pressed('up', 'down', 'left', 'right')

@play.when_program_starts
async def do():
    cat.x = -10
    await play.timer(seconds=5)
    cat.x = 0

@play.when_key_pressed
async def do(key):
    key_text.words = 'last key pressed: {}'.format(key)

    if key == 'up':
        cat.y -= 20
    if key == 'down':
        cat.y += 20
    if key == 'right':
        cat.x += 20
    if key == 'left':
        cat.x -= 20

@cat.when_clicked
async def do():
    print(label.words)
    if cat.size >= 200:
        for number in play.repeat(100):
            cat.increase_size(percent=-1)
            label.increase_size(percent=-1)
            await play.next_frame()
    else:
        for number in play.repeat(100):
            cat.increase_size(percent=1)
            label.increase_size(percent=1)
            await play.next_frame()
            # cat.turn(3)

@play.repeat_forever
async def do():
    label.go_to(cat)
    cat.point_towards(play.mouse)
    label.degrees = cat.degrees

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


@play.repeat_forever
async def do():

    play.background_color('red')
    await play.timer(seconds=1)

    play.background_color('green')
    await play.timer(seconds=1)

    play.background_color('blue')
    await play.timer(seconds=1)


play.start_program() # this line should be the last line in your program

# sprite.go_to()
# sprite.turn(degrees=10)
# sprite.point_to(angle=45)
#   sprite.point_to(cat)
#   sprite.point_to(x,y)
#   sprite.point_to(play.mouse)
# sprite.move()
