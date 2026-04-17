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
#mark_children = "mark_children_differ_vers_1.png"
#img_name = "dots_at_children.png"
#img_name = "coords_print_test.png"
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
def make_child_image(img_name):
    with Image.open(img_name) as im:
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
        im.save(img_name, "PNG")
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

    ordered_children:dict = {}
    """ordered_children[centre_coordinates][position_str]"""

    def __init__(self, children_dict):
        self.children_dict = children_dict
        pass

    def get_row_and_column(self):
        # pixel_coord = (spaced_x, spaced_y)
        rows = set()
        columns = set()
        self.coord_dict = {"rows": {}, "columns": {}}
        col_count = 0
        for i, coord in enumerate(pixel_dict): # is the dict that just stored the list of points + col values
            x, y = coord
            if x not in rows:
                rows.add(x)
                self.coord_dict["rows"][i] = x
            if y not in columns:
                columns.add(y)
                self.coord_dict["columns"][col_count] = y
                col_count += 1
        #print(f"ROWS: {sorted(rows)}")
        #print(f"COLUMNS: {sorted(columns)}")
        print(f"POS DICT: {self.coord_dict}")

    def align_children(self, selected_coord=None): # adding this so I can get the children in the correct 0,1,2,3 order to rotate properly.
        # children = self.children_dict[coord]

        for point, children in self.children_dict.items():
            point_x, point_y = point
            if selected_coord and point != selected_coord:
                continue
            #print(f"POINT: {point}")
            self.ordered_children[point] = {}
            for i, child in enumerate(children):
                x, y = child
                if x == point_x and y < point_y:
                    self.ordered_children[point]["top"] = child
                    #print(f"Child is top: {child}")
                elif x == point_x and y > point_y:
                    self.ordered_children[point]["bottom"] = child
                    #print(f"Child is bottom: {child}")

                elif x > point_x and y == point_y:
                    self.ordered_children[point]["right"] = child
                    #print(f"Child is right: {child}")

                elif x < point_x and y == point_y:
                    self.ordered_children[point]["left"] = child
                    #print(f"Child is left: {child}")
                else:
                    print(f"Coord is not top/bottom/left/right of {point}: {child}\ncoord x: {x}, main_point x: {point_x}")

                """if i == 0:
                    self.ordered_children[point]["top"] = child
                    print(f"Child is top: {child}")

                    top_row, centre_col = child
                elif x > top_row and y == centre_col:
                    self.ordered_children[point]["bottom"] = child
                    print(f"Child is bottom: {child}")
                elif x > top_row and y > centre_col:
                    self.ordered_children[point]["right"] = child
                    print(f"Child is right: {child}")
                elif x > top_row and y < centre_col:
                    self.ordered_children[point]["left"] = child
                    print(f"Child is left: {child}")
                else:
                    print(f"Coord is not top/bottom/left/right of {point}: {child}")"""

        print(f"self.ordered_children: {self.ordered_children}")

    def add_dots_at_children(self, coord, img_name):
        children = self.children_dict[coord]

        with Image.open(img_name) as im:
            radius = 25

            x_main, _ = coord
            pixel_value = pixel_dict[coord]
            child_colours = {}
            for i, child_coords in enumerate(children):
                child_col = pixel_dict[child_coords]
                child_colours[i] = child_col
            print(f"CHILDREN in add_dots_at-children: {children}")
            for i, child_coords in enumerate(children):
                #print(f"i in child coords: {i}")
                if i+1 == len(child_colours):
                    child_col = child_colours[0]
                else:
                    child_col = child_colours[i+1]
                #print(f"Child col: {child_col}")
                """x, _ = child_coords
                if x == x_main:
                    a, b, c = pixel_value
                    pixel_value = tuple((a+35, b+35, c+35))"""
                draw = ImageDraw.Draw(im)
                #draw.circle(child_coords, radius=radius, fill=pixel_value, outline=(1,1,1))
                draw.circle(child_coords, radius=radius, fill=child_col, width=2)
                draw.text(xy=child_coords, text=str(i), fill="#000000")
                """Currently this is wrong, because the 'children' are
                   0
                1     2
                   3
                which makes perfect sense but I'm thinking of it as
                   0
                3     1
                   2
                Okay.
                """
            im.save(img_name, "PNG")
            # write to stdout
            #im.save("mark_children.png", "PNG")

    def print_all_coords(self, img_name):

        with Image.open(img_name) as im:
            for coord in pixel_dict:
                x, y = coord
                x-=int(len(str(coord)))+10
                y-= 18
                coord_placement = (x, y)
                draw = ImageDraw.Draw(im)
                draw.text(xy=coord_placement, text=str(coord), fill="#FFFFFF")
        im.save(img_name, "PNG")

    def print_children_for_coord(self, img_name, coord=None):# testing

        children = self.ordered_children[coord]
        unordered_children = self.children_dict[coord]

        with Image.open(img_name) as im:
            radius = 25

            x_main, _ = coord
            pixel_value = pixel_dict[coord]

            print(f"[print_children_for_coord] CHILDREN: {children}")
            draw = ImageDraw.Draw(im)
            draw.text(xy=coord, text=str(f"CENTER\n{coord}"), fill="#FFFFFF")

            def draw_ordered(draw, children):
                for position, child_coords in children.items():
                    child_col = pixel_dict[child_coords]
                    print(f"position in child coords: {position}\n")
                    print(f"coords: {child_coords} // Child col: {child_col}")

                    #draw.circle(child_coords, radius=radius, fill=pixel_value, outline=(1,1,1))
                    draw.circle(child_coords, radius=radius, fill=child_col, width=2)
                    draw.text(xy=child_coords, text=str(position), fill="#000000")

            def draw_coords(draw, unordered_children):
                for child in unordered_children:
                    draw.text(xy=child, text=str(f"{child}"), fill="#FFFFFF")

            draw_coords(draw, unordered_children)
            #draw_ordered(draw, children)
            im.save(img_name, "PNG")
            # write to stdout
            #im.save("mark_children.png", "PNG")
            im.save(img_name, "PNG")

    def get_rotate_pos(self, coords, children):

        print(f"[get_rotate_pos] // children: {children}")
        rotated_children = {}
        for item in children:
            for child in children:
                if len(children) == 2:
                    continue
                print(f"child: {child} / item: {item}")
                if child != item:
                    rotated_children[child] = (self.ordered_children[coords][item], pixel_dict[self.ordered_children[coords][item]])

        return rotated_children


    def get_correct_child_for_rotation(self, centre_position, child, children, target_position=None, start_position=None):
        """basically doing this
        rotated_children["top"] = (child, pixel_dict[children["top"]])
        but if no 'top', pick the next best option.
        My impulse is to do it by numbers; if only two, just use the only other option, but that feels like the wrong way to do it."""

        pos_dict = {
            "right": "top",
            "bottom": "right",
            "left": "bottom",
            "top": "left"
        }

        def reorder(specified, children):
            order = list(children)#["right", "bottom", "left", "top"]
            i = order.index(specified)
            return order[i+1:] + order[:i+1]
        """def reorder(specified):
            order = ["right", "bottom", "left", "top"]
            i = order.index(specified)
            return order[i+1:] + order[:i]"""

        def rotate_values(centre_pos, pos, pivot, children=None):
            if not children:
                order = ["right", "bottom", "left", "top"]
            else:
                order = list(children)

            new_order = reorder(pivot, order)
            values = [pos[k] for k in new_order]
            colours = [pixel_dict[self.ordered_children[centre_pos][k]] for k in new_order]

            values = dict(zip(values, colours))
            print(f"values: {values}")
            rotated = {}
            for i, new_key in enumerate(new_order):
                old_key = order[i]   # ← THIS is the important part
                coord = pos[old_key]
                rotated[new_key] = {coord: values[coord]}
            #rotated = {
            #    new_key: {coord: values[coord]}
            #    for new_key, coord in zip(new_order, (pos[k] for k in new_order))
            #}
            #rotated = dict(zip(new_order, values))
            return rotated

        rotated_children = {}
        for i, item in enumerate(children):

            rotated_children = rotate_values(centre_position, self.ordered_children[centre_position], item, children)

            old_rotated_children = {}
            if len(children) == 4:
                old_rotated_children["top"] = (children["right"], pixel_dict[children["top"]])
                old_rotated_children["right"] = (children["bottom"], pixel_dict[children["right"]])
                old_rotated_children["bottom"] = (children["left"], pixel_dict[children["bottom"]])
                old_rotated_children["left"] = (children["top"], pixel_dict[children["left"]])
            #if len(children) != 4:
            #    rotated_children = rotate_values(centre_position, self.ordered_children[centre_position], item, children)

            #new_children = reorder(item, children)
            #print(f"old_children: {children}")
            #print(f"new_children: {new_children}")
            #rotated_children[item] = (self.ordered_children[centre_position][new_children[i]], pixel_dict[self.ordered_children[centre_position][new_children[i]]])

        """if len(children) == 2:
        else:
            for item in children:
                print(f"item in children: {item}")
                if pos_dict[item] in children:
                    print(f"pos_dict[item] is in children: {pos_dict[item]}")
                else:
                    print(f"pos_dict[item] is not children: {pos_dict[item]}")"""

        print(f"\nROTATED CHILDREN: {rotated_children}\n")
        print(f"\nOLD ROTATED CHILDREN: {rotated_children}\n")
        return rotated_children
            #for i in children:
                #print(f"i in children: {i} // child: {child}")
                #rotated_children[i] = (child, None)

        """else:
            if self.ordered_children[centre_position].get(target_position):
                return (child, pixel_dict[self.ordered_children[centre_position][target_position]])"""

    def order_children(self, children):
        """to ensure they follow the ordering of ["right", "bottom", "left", "top"]; currently, those in the far right column don't."""
        order = ["top", "right", "bottom", "left"]
        print(f"Original children: {children}")
        children_list = list(i for i in order if i in children)
        print(f"reordered children: {children}")
        new_children = {}
        for child in children_list:
            new_children[child] = children[child]
        return new_children

    def reindex_children(self, children):
        order = ["top", "right", "bottom", "left"]
        #order = list(children)
        if len(children) == 2 or len(children) == 4:
            children = list(children)[1:] + list(children)[:1] #<-- can probably do without 'specified' and just use children alone for this.
            print(f"reordered len(children) == 2 or len(children) == 4: {children}")
            return children
        specified = list(i for i in order if not i in children)

        if specified:
            specified = specified[0]

        i = order.index(specified)
        new_order = order[i+1:] + order[:i]
        if list(new_order) == list(children):
            new_order = new_order[1:] + new_order[:1] #<-- can probably do without 'specified' and just use children alone for this.
        return new_order



    def add_dots_at_correct_children(self, coord, img_name):

        children = self.ordered_children[coord]
        print(f"[add_dots_at_correct_children] CHILDREN: {children}")
        children = self.order_children(children)
        rotated_children = {}
        child_a = None
        child_b = None

        reordered = self.reindex_children(children)
        #print(f"CHILDREN: {children} // REORDERED: {reordered}")
        for child in children:
            orig_index = list(children).index(child)
            new_index = list(reordered).index(child)
            #print(f"list(children)[new_index]: {list(children)[new_index]}")
            rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], pixel_dict[children[list(children)[new_index]]])


        """if len(children) == 2:
            for child in children:
                if not child_a:
                    child_a = child
                else:
                    child_b = child
            for child in children:
                if child == child_a:
                    rotated_children[child_a] = (children[child_b], pixel_dict[children[child_a]])
                else:
                    rotated_children[child_b] = (children[child_a], pixel_dict[children[child_b]])

        elif len(children) == 3:
            reordered = self.reindex_children(children)
            #print(f"CHILDREN: {children} // REORDERED: {reordered}")
            for child in children:
                orig_index = list(children).index(child)
                new_index = list(reordered).index(child)
                #print(f"list(children)[new_index]: {list(children)[new_index]}")
                rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], pixel_dict[children[list(children)[new_index]]])

        elif len(children) == 4:
            rotated_children["top"] = (children["right"], pixel_dict[children["top"]])
            rotated_children["right"] = (children["bottom"], pixel_dict[children["right"]])
            rotated_children["bottom"] = (children["left"], pixel_dict[children["bottom"]])
            rotated_children["left"] = (children["top"], pixel_dict[children["left"]])"""

        with Image.open(img_name) as im:
            radius = 25

            for position, child_coords in rotated_children.items():
                if not child_coords:
                    continue
                child_coords, child_colour = child_coords
                print(f"child_coords: {child_coords} / child_colour: {child_colour}")
                #pixel_value = pixel_dict[child_coords]

                draw = ImageDraw.Draw(im)
                #draw.circle(child_coords, radius=radius, fill=pixel_value, outline=(1,1,1))
                draw.circle(child_coords, radius=radius, fill=child_colour, width=2)
                draw.text(xy=child_coords, text=str(position), fill="#000000")

            # write to stdout
            #im.save("mark_children.png", "PNG")
            im.save(img_name, "PNG")

    def add_rows_and_columns(self, img_name):

        img_w_coords = "dots_with_row_and_column.png"

        #with Image.open(d_a_c) as im:
        #    pass

        with Image.new(mode="RGBA", size=(width+30, height+30), color=(0,0,0)) as im:

            #im.save(sys.stdout, "PNG")
            with Image.open(img_name) as image_2:

                im.paste(image_2, (30,30))

            done_row_nos = set()
            done_col_nos = set()
            row_0 = self.coord_dict["rows"][0]
            column_0 = self.coord_dict["columns"][0]
            for column_no, col_coord in self.coord_dict["columns"].items():
                for row_no, coord in self.coord_dict["rows"].items():
                    if row_no in done_row_nos:
                        continue
                    #print(f"COORD: {coord}")
                    draw = ImageDraw.Draw(im)
                    if row_no == 0:
                        text = str(row_no)
                    else:
                        text = "X " + str(row_no)
                    draw.text(xy=(coord, col_coord), text=text, fill="#FFFFFF")
                    done_row_nos.add(row_no)

            for column_no, col_coord in self.coord_dict["columns"].items():
                if col_coord in done_col_nos or column_no == 0:
                    continue
                #print(f"column COORD: {col_coord}")
                draw = ImageDraw.Draw(im)
                draw.text(xy=(column_0, col_coord), text="Y " + str(column_no), fill="#FFFFFF")
                done_col_nos.add(row_no)

            # write to stdout
            #im.save("recreate_with_circles_test1", "PNG")
            #im.save("mark_children.png", "PNG")
            im.save(img_w_coords, "PNG")

def select_coords(column:int=2, row:int=2):
    selected_coord = (base_pos.coord_dict["columns"][column], base_pos.coord_dict["rows"][row])
    return selected_coord


base_pos = base_positions(child_dict)

def setup_grid(img_name):
    base_pos.get_row_and_column()
    make_starting_image(img_name)
    base_pos.align_children() # probably makes far more sense to do it all at once here

def print_extras(img_name):
    base_pos.print_all_coords(img_name)
    base_pos.add_rows_and_columns(img_name)

#selected_coord = (base_pos.coord_dict["rows"][2], base_pos.coord_dict["columns"][3])
def rotate_single_point(img_name, row=2, column=2, coords=None):
    if coords:
        selected_coord = coords
    else:
        selected_coord = select_coords(row, column)
    print(f"Selected coord: {selected_coord}")
    #base_pos.align_children(selected_coord)
    #base_pos.add_dots_at_children(selected_coord) # oh shit, this worked too. Nice. Now how to rotate them...
    ##base_pos.print_children_for_coord(selected_coord)
    base_pos.add_dots_at_correct_children(selected_coord, img_name)

def print_point_data(coord, img_name):

    with Image.open(img_name) as im:

        draw = ImageDraw.Draw(im)
        draw.rectangle((2, 2, 128, 15), fill="#FFFFFF")
        draw.text(xy=(4, 4), text=f"CENTREPOINT: {coord}", fill="#000000")

        # write to stdout
        #im.save("mark_children.png", "PNG")
        im.save(img_name, "PNG")

def main():

    test_all=True
    if test_all:
        for i, coord in enumerate(pixel_dict):
            img_name = f"coords_print_test_{i}.png"
            setup_grid(img_name)
            print_extras(img_name)
            rotate_single_point(img_name, coords=coord)
            print_point_data(coord, img_name)

    else:
        img_name = "image_name_for_testing.png"
        setup_grid(img_name)
        print_extras(img_name)

main()
