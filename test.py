import play

play.background_color(red_amount=1.0, blue_amount=1.0, green_amount=1.0)

cat = play.new_sprite(image='cat.png', x=0, y=0, size=1)

label = play.new_text(words='click this cat!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

@cat.when_clicked
def do():
    cat.move(-40)

@play.repeat_forever
async def do():

    play.background_color('red')
    await play.timer(seconds=1)

    play.background_color('green')
    await play.timer(seconds=1)

    play.background_color('blue')
    await play.timer(seconds=1)

@play.repeat_forever
async def do():
    cat.move(1)
    label.go_to(cat)


play.start_program() # this line should be the last line in your program



# while play.repeat_forever():
#     # commands you want to happen constantly go here
#     cat.move(1)
#     label.go_to(cat)

# no commands below this line will work



# should this animate?:
# for number in range(10):
#     cat.move(-10)
#     cat.turn(5)
#     label.words = number

# maybe this instead
# for count in play.repeat(5): 1,2,3,4,5
#    ...
# or
# while play.repeat(5):
#    ...
# queues commands to be run on next frames
