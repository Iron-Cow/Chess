# Improting Image class from PIL module
from PIL import Image

# Opens a image in RGB mode
im = Image.open("ChessPiecesArray.png")

# Size of the image in pixels (size of orginal image)
# (This is not mandatory)
width, height = im.size

# Setting the points for cropped image
left = 0
top = height / 2
right = 60
bottom = height

# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))

# Shows the image in image viewer
im1.save("wQ.png")
a = ['wQ', "wK", "wR", "wN", "wB", "wP"]
gap = 0
for white in a:
    left = 0 + gap
    top = height / 2
    right = 60 + gap
    bottom = height

    im1 = im.crop((left, top, right, bottom))
    im1.save(f"{white}.png")
    gap += 60

a = ['bQ', "bK", "bR", "bN", "bB", "bP"]
gap = 0
for black in a:
    left = 0 + gap
    top = 0
    right = 60 + gap
    bottom = height / 2

    im1 = im.crop((left, top, right, bottom))
    im1.save(f"{black}.png")
    gap += 60
