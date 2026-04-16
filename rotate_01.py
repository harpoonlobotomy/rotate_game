"""want to make that game I saw in an add, where you have to correctly rotate clusters of 4 colours so they all line up."""

"""
Thoughts:
make a grid.
at each gridpoint, add 4 surrounding points, with colours.
each gridpoint (except those at edges) can be traded with the neighbour (eg:
    a     b
 a  1  a  2  b   <<-- '1' controls all of a and can rotate them around itself. 2 controls all of b and the rightmost 'a' and can rotate them around itself.)
    a     b

So I need a way to manage grid points and their rotation (and to keep a 'before' version, to realign all parts to the 'correct' orientation (they start correct then rotate randomly to make the 'puzzle')), and the matching of each part. So each 'point' of each gridpoint has a 'target'.
Note: 'points' of gridpoints here are not the things that rotate, but are set. So in the example above,

    a     a
 a  1  b  2  b   <<-- '2' has rotated once clockwise, but the centre point (was a, now b) has the same 'target' - targets are for the space, not the conceptual 'point' that is rotating. Targets are on the ground, points are floating above them. Yes? Think so.
    a     b


The grid is drawn up with each gridpoint 'point' on its target. Then, each gridpoint is rotated a random number of times in a random order, and the goal is to get it all back to position.

background image can be random, pattern, image, whatever. Stripes/gradients probably a good start? Not sure.

Anyway. That's the intent. 9:14pm, 15/4/26

72px squares, roughly 13 pixels apart. (Will remake with better spacings later.)
use no_border version for testing.

So, midpoint of each square is 36 + 13 + 36 apart. top left square center is 36,36 from 0,0.

"""

from PIL import Image, ImageDraw

#png_file = "simple_square_test_no_border.png"
png_file = "better_differentiation.png"
mark_children = "mark_children_differ_vers_1.png"

#with open("simple_square_test_no_border.png", "rb") as fp:
#    px = Image.open(fp)

with Image.open(png_file) as im:
    px = im.load()
    width, height = im.size

# note: (row, column) - so changing the first and not the second goes left>right.

pixel_dict = {}
# width, height = im.size

spacing = 36 + 13 + 36
print(f"SPACING: {spacing}")
spaced_y = 36

for i in range(0, height):
    spaced_x = 36

    for i in range(0, width):
        pixel_coord = (spaced_x, spaced_y)
        if (spaced_x > width) or (spaced_y > height):
            continue
        pixel_dict[pixel_coord] = px[pixel_coord]
        spaced_x = (spaced_x+spacing)

    spaced_y = spaced_y + spacing

def make_starting_image(img_name):

    with Image.new(mode="RGBA", size=(width, height), color=(0,0,0)) as im:

        for coordinate, pixel_value in pixel_dict.items():

            draw = ImageDraw.Draw(im)
            draw.circle(coordinate, radius=32, fill=pixel_value, outline=(0,0,0))

        # write to stdout
        #im.save("recreate_with_circles_test1", "PNG")
        #im.save("mark_children.png", "PNG")
        im.save(img_name, "PNG")
        #im.save(sys.stdout, "PNG")

"""
Oh shit it actually worked. Okay.
Well not the rotating or anything, but recreating the grid as specified points and recreating them with PIL. Good start.
11:32pm.

So next I need to get the 'rotation children' for each point.
For each point, it's the ones 1 spacing from center.
"""

child_dict = {}

for points in pixel_dict.keys():
    spaced_x, spaced_y = points
    """print(f"POINT: x,y: {points}")
    print(f"spaced_x + spacing: {spaced_x + spacing}")
    print(f"spaced_x - spacing: {spaced_x - spacing}")
    print(f"spaced_y + spacing: {spaced_y + spacing}")
    print(f"spaced_y - spacing: {spaced_y - spacing}")"""
    #child_points = list((x, y) for (x, y) in pixel_dict.keys() if (x == (spaced_x + spacing) or x == (spaced_x - spacing)) and (y == (spaced_y + spacing) or y == (spaced_y - spacing)))
    child_points = list((x, y) for (x, y) in pixel_dict.keys() if (((x == (spaced_x + spacing) or x == (spaced_x - spacing)) and (y == spaced_y))) or (x == spaced_x and (y == (spaced_y + spacing) or y == (spaced_y - spacing))))# + spacing) or y == (spaced_y - spacing)))
    child_dict[points] = child_points
    #print(f"Child points of {points}:\n{child_points}")

#with Image.open("mark_children.png") as im:
def make_child_image():
    with Image.open(mark_children) as im:
        radius = 25
        for coordinate, pixel_value in pixel_dict.items():
            x_main, _ = coordinate
            radius = radius - 1
            if radius <= 10:
                radius = 25
            children = child_dict[coordinate]

            for child_coords in children:
                x, _ = child_coords
                if x == x_main:
                    a, b, c = pixel_value
                    pixel_value = tuple((a+35, b+35, c+35))
                draw = ImageDraw.Draw(im)
                #draw.circle(child_coords, radius=radius, fill=pixel_value, outline=(1,1,1))
                draw.circle(child_coords, radius=radius, outline=pixel_value, width=2)

        # write to stdout
        #im.save("mark_children.png", "PNG")
        im.save(mark_children, "PNG")
    #im.save(sys.stdout, "PNG")

"""
if len(children) == 2:
    a, b = children
    children = (b, a) # just swap em

elif len(children) > 2:
    if len(children) == 3:
        a, b, c = children
        children = (b, c, a) # rotate what you have
    else:
        a, b, c, d = children
        children = (b, c, d, a) # rotate 'em all

well that doesn't actually rotate anything, but conceptually.
Anyway. 11.40pm, going to try to sleep.
"""

class base_positions:

    children_dict:dict = {}
    coord_dict:dict = {}

    def __init__(self, children_dict):
        self.children_dict = children_dict
        pass

    def get_row_and_column(self):
        # pixel_coord = (spaced_x, spaced_y)
        rows = set()
        columns = set()
        pos_dict = {"rows": {}, "columns": {}}
        col_count = 0
        for i, coord in enumerate(pixel_dict): # is the dict that just stored the list of points + col values
            x, y = coord
            if x not in rows:
                rows.add(x)
                pos_dict["rows"][i] = x
            if y not in columns:
                columns.add(y)
                pos_dict["columns"][col_count] = y
                col_count += 1
        #print(f"ROWS: {sorted(rows)}")
        #print(f"COLUMNS: {sorted(columns)}")
        print(f"POS DICT: {pos_dict}")
        self.coord_dict = pos_dict
        pass

    def add_dots_at_children(self, coord):
        children = self.children_dict[coord]
        d_a_c = "dots_at_children.png"

        make_starting_image(d_a_c)

        with Image.open(d_a_c) as im:
            radius = 25

            x_main, _ = coord
            pixel_value = pixel_dict[coord]

            for child_coords in children:
                x, _ = child_coords
                if x == x_main:
                    a, b, c = pixel_value
                    pixel_value = tuple((a+35, b+35, c+35))
                draw = ImageDraw.Draw(im)
                #draw.circle(child_coords, radius=radius, fill=pixel_value, outline=(1,1,1))
                draw.circle(child_coords, radius=radius, outline=pixel_value, width=2)

            # write to stdout
            #im.save("mark_children.png", "PNG")
            im.save(d_a_c, "PNG")

base_pos = base_positions(child_dict)

base_pos.get_row_and_column()
selected_coord = (base_pos.coord_dict["rows"][2], base_pos.coord_dict["columns"][3])
base_pos.add_dots_at_children(selected_coord) # oh shit, this worked too. Nice. Now how to rotate them...
