import play

play.background_color(red_amount=1.0, blue_amount=1.0, green_amount=1.0)

cat = play.sprite(image='cat.png', x=0, y=0, size=1)
label = play.text(words='click this cat!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

@cat.when_clicked
def do():
    cat.move(-40)
    
while play.forever():
    cat.move(1)
    label.go_to(cat)