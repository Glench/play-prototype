import play

play.background_color(red_amount=1.0, blue_amount=1.0, green_amount=1.0)

cat = play.sprite(image='cat.png', x=0, y=0, size=1)
text = play.text(words='click this cat!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

# @play.when_clicked(cat) also works
@cat.when_clicked
def do():
    cat.move(-20)
    
while play.forever():
    cat.move(1)
    text.go_to(cat)
