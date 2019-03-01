color_names = {
    'black':        (  0,   0,   0),
    'white':        (255, 255, 255),
    'red':          (255,   0,   0),
    'green':        (0  , 255,   0),
    'blue':         (0  ,   0, 255),
}

def color_name_to_rgb(name):
    if type(name) == tuple:
        return name
        
    try:
        return color_names[name]
    except KeyError:
        raise Exception("Color name not recognized: {}".format(name))