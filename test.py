import play

play.background_color(red_amount=1.0, blue_amount=1.0, green_amount=1.0)

cat = play.new_sprite(image='cat.png', x=0, y=0, size=1)

label = play.new_text(words='click this cat!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

# TODO:
#   - try queuing up commands so can do `for i in play.repeat(10)` instead of `async for i in play.repeat(10)`
#   - figure out terminology for rotate, pointing, degrees, turning, etc
#   - implement `when_program_starts`
#   - refactor event loop
#   - 

@play.when_program_starts
async def do():
    cat.x = -10
    await play.timer(seconds=5)
    cat.x = 0


@cat.when_clicked
async def do():
    pass
    # cat.rotate_to(angle=90)
    # # this works:
    # async for i in play.repeat(36):
    #     cat.rotate(degrees=10)
    #     await play.timer(0.5)
    #
    # # but it would be better to do:
    # for i in play.repeat(10):
    #   ...
    #
    # # or this could work:
    for i in play.repeat(10):
        cat.turn(10)
        await play.animate()

@play.repeat_forever
async def do():
    label.go_to(cat)
    cat.point_to(play.mouse)
    label.angle(degrees=cat.degrees)

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
