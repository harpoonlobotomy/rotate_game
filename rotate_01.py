"""want to make that game I saw in an add, where you have to correctly rotate clusters of 4 colours so they all line up."""

from PIL import Image, ImageDraw

base_image = "better_differentiation.png"

def generate_starting_image():
    """adds pixel_dict to img_data"""
    if img_data.base_image:
        with Image.open(img_data.base_image) as im:
            px = im.load()

    else:
        print("No ability to generate images from naught yet, exiting.")
        exit()
    # note: (row, column) - so changing the first and not the second goes left>right.

    print(f"SPACING: {img_data.spacing}")
    spaced_y = int(img_data.dot_radius/2)

    for _ in range(0, img_data.height):
        spaced_x = int(img_data.dot_radius/2)

        for _ in range(0, img_data.width):
            pixel_coord = (spaced_x, spaced_y)
            if (spaced_x > img_data.width) or (spaced_y > img_data.height):
                continue
            img_data.pixel_dict[pixel_coord] = px[pixel_coord]
            spaced_x = (spaced_x+img_data.spacing)

        spaced_y = spaced_y + img_data.spacing

class image_data:

    base_image:str=None
    filename:str=None

    width:int=None
    height:int=None
    dot_radius:int=72
    spacing_between_edges:int=13
    pixel_dict:dict={}
    """[x, y coordinates] = (r, g, b values)"""

    def __init__(self):
        pass

    def set_file_data(self, base_file=None, filename=None, width=None, height=None, dot_radius=72, spacing_between=13):

        if base_file:
            self.base_image = base_file
            with Image.open(base_file) as im:
                width, height = im.size
                print(f"width, height: {width, height}")

        self.filename = filename

        self.width = width
        self.height = height

        if not self.width or not self.height:
            print(f"Not self.width or self.height: {self.width} / {self.height}")

        self.dot_radius = dot_radius
        self.spacing_between_edges = spacing_between

        self.spacing = int(dot_radius/2) + spacing_between + int(dot_radius/2)

    def get_child_dict(self):
        child_dict = {}

        for points in self.pixel_dict.keys():
            spaced_x, spaced_y = points
            child_points = list((x, y) for (x, y) in self.pixel_dict.keys() if (((x == (spaced_x + self.spacing) or x == (spaced_x - self.spacing)) and (y == spaced_y))) or (x == spaced_x and (y == (spaced_y + self.spacing) or y == (spaced_y - self.spacing))))# + spacing) or y == (spaced_y - spacing)))
            child_dict[points] = child_points
        return child_dict

class base_positions:

    children_dict:dict = {}
    coord_dict:dict = {}

    ordered_children:dict = {}
    """ordered_children[centre_coordinates][position_str]"""

    def __init__(self):
        pass

    def set_dicts(self, children_dict):
        self.children_dict = children_dict
        pass

    def get_row_and_column(self):
        # pixel_coord = (spaced_x, spaced_y)
        rows = set()
        columns = set()
        self.coord_dict = {"rows": {}, "columns": {}}
        col_count = 0
        for i, coord in enumerate(img_data.pixel_dict): # is the dict that just stored the list of points + col values
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
        #print(f"POS DICT: {self.coord_dict}")

    def align_children(self, selected_coord=None): # adding this so I can get the children in the correct 0,1,2,3 order to rotate properly.
        # children = self.children_dict[coord]

        for point, children in self.children_dict.items():
            point_x, point_y = point
            if selected_coord and point != selected_coord:
                continue
            #print(f"POINT: {point}")
            self.ordered_children[point] = {}
            for child in children:
                x, y = child
                if x == point_x and y < point_y:
                    self.ordered_children[point]["top"] = child

                elif x == point_x and y > point_y:
                    self.ordered_children[point]["bottom"] = child

                elif x > point_x and y == point_y:
                    self.ordered_children[point]["right"] = child

                elif x < point_x and y == point_y:
                    self.ordered_children[point]["left"] = child
                else:
                    print(f"Coord is not top/bottom/left/right of {point}: {child}\ncoord x: {x}, main_point x: {point_x}")

            #print(f"self.ordered_children[point]: {self.ordered_children[point]}")
            self.ordered_children[point] = self.order_children(self.ordered_children[point])
            #print(f"self.ordered_children[point]: {self.ordered_children[point]}")


    def print_all_coords(self):

        with Image.open(img_data.filename) as im:
            for coord in img_data.pixel_dict:
                x, y = coord
                x-=int(len(str(coord)))+10
                y-= 18
                coord_placement = (x, y)
                draw = ImageDraw.Draw(im)
                draw.text(xy=coord_placement, text=str(coord), fill="#FFFFFF")
        im.save(img_data.filename, "PNG")


    def order_children(self, children):
        """to ensure they follow the ordering of ["right", "bottom", "left", "top"]; currently, those in the far right column don't."""
        order = ["top", "right", "bottom", "left"]
        #print(f"Original children: {children}")
        children_list = list(i for i in order if i in children)
        #print(f"reordered children: {children}")
        new_children = {}
        for child in children_list:
            new_children[child] = children[child]
        return new_children

    def reindex_children(self, children):
        order = ["top", "right", "bottom", "left"]
        #order = list(children)
        if len(children) == 2 or len(children) == 4:
            children = list(children)[1:] + list(children)[:1] #<-- can probably do without 'specified' and just use children alone for this.
            #print(f"reordered len(children) == 2 or len(children) == 4: {children}")
            return children
        specified = list(i for i in order if not i in children)

        if specified:
            specified = specified[0]

        i = order.index(specified)
        new_order = order[i+1:] + order[:i]
        if list(new_order) == list(children):
            new_order = new_order[1:] + new_order[:1] #<-- can probably do without 'specified' and just use children alone for this.
        return new_order


    def add_dots_at_correct_children(self, coord):

        children = self.ordered_children[coord]
        #print(f"[add_dots_at_correct_children] CHILDREN: {children}")
        #children = self.order_children(children)
        rotated_children = {}
        child_a = None
        child_b = None

        reordered = self.reindex_children(children)
        #print(f"CHILDREN: {children} // REORDERED: {reordered}")
        for child in children:
            orig_index = list(children).index(child)
            new_index = list(reordered).index(child)
            #print(f"list(children)[new_index]: {list(children)[new_index]}")
            rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], img_data.pixel_dict[children[list(children)[new_index]]])


        with Image.open(img_data.filename) as im:
            radius = 25
            for position, child_coords in rotated_children.items():
                if not child_coords:
                    continue
                child_coords, child_colour = child_coords
                #print(f"child_coords: {child_coords} / child_colour: {child_colour}")
                #pixel_value = pixel_dict[child_coords]
                x, y = child_coords
                x -= int(len(position)/2)+5
                draw = ImageDraw.Draw(im)
                if img_data.pixel_dict[child_coords] == child_colour:
                    a, b, c = child_colour
                    child_colour = tuple((a+45, b+45, c+45))
                #draw.circle(child_coords, radius=radius, fill=pixel_value, outline=(1,1,1))
                draw.circle(child_coords, radius=radius, fill=child_colour, width=2)
                child_coords = x, y
                draw.text(xy=child_coords, text=str(position), fill="#000000")

            im.save(img_data.filename, "PNG")

    def add_rows_and_columns(self):

        with Image.new(mode="RGBA", size=(img_data.width+30+20, img_data.height+30+20), color=(0,0,0)) as im:

            #im.save(sys.stdout, "PNG")
            with Image.open(img_data.filename) as image_2:

                im.paste(image_2, (30,30))

            done_row_nos = set()
            done_col_nos = set()

            column_0 = self.coord_dict["columns"][0]
            for column_no, col_coord in self.coord_dict["columns"].items():
                for row_no, coord in self.coord_dict["rows"].items():
                    if row_no in done_row_nos:
                        continue
                    draw = ImageDraw.Draw(im)
                    if row_no == 0:
                        text = str(row_no)
                    else:
                        text = "X " + str(row_no)
                    draw.text(xy=(coord-5, col_coord-10), text=text, fill="#FFFFFF")
                    done_row_nos.add(row_no)

            for column_no, col_coord in self.coord_dict["columns"].items():
                if col_coord in done_col_nos or column_no == 0:
                    continue
                draw = ImageDraw.Draw(im)
                draw.text(xy=(column_0-5, col_coord-10), text="Y " + str(column_no), fill="#FFFFFF")
                done_col_nos.add(row_no)

            im.save(img_data.filename, "PNG")


def make_starting_image():

    with Image.new(mode="RGBA", size=(img_data.width, img_data.height), color=(0,0,0)) as im:

        for coordinate, pixel_value in img_data.pixel_dict.items():

            draw = ImageDraw.Draw(im)
            draw.circle(coordinate, radius=32, fill=pixel_value, outline=(0,0,0))

        im.save(img_data.filename, "PNG")

def select_coords(column:int=2, row:int=2):
    selected_coord = (base_pos.coord_dict["columns"][column], base_pos.coord_dict["rows"][row])
    return selected_coord

img_data = image_data()
base_pos = base_positions()

def setup_grid():
    base_pos.get_row_and_column()
    make_starting_image()
    base_pos.align_children()

def print_extras():
    base_pos.print_all_coords()
    base_pos.add_rows_and_columns()

def rotate_single_point(row=2, column=2, coords=None):
    if coords:
        selected_coord = coords
    else:
        selected_coord = select_coords(row, column)
        #print(f"Selected coord: {selected_coord}")

    base_pos.add_dots_at_correct_children(selected_coord)
    return selected_coord

def print_point_data(coord):
    """can add more here later. Just some metadata for tests."""
    with Image.open(img_data.filename) as im:

        draw = ImageDraw.Draw(im)
        draw.rectangle((2, 2, 128, 15), fill="#FFFFFF")
        draw.text(xy=(4, 4), text=f"CENTREPOINT: {coord}", fill="#000000")

        im.save(img_data.filename, "PNG")

def initial_setup(base_file=None, filename=None, width=None, height=None, dot_radius=72, spacing_between=13):
    img_data.set_file_data(base_file, filename, width, height, dot_radius, spacing_between)
    generate_starting_image()
    child_dict = img_data.get_child_dict()
    base_pos.set_dicts(child_dict)

##### GUI #####

def start_gui():
    from rotate_gui_01 import splash_window, main_window
    splash_window()
    while True:
        if main_window(img_data.pixel_dict, base_pos.coord_dict):
            break

def main():

    initial_setup(base_file=base_image, filename = "image_name_for_testing.png")

    test_all=False#True
    if test_all:
        for i, coord in enumerate(img_data.pixel_dict):
            img_data.filename = f"coords_print_test_{i}.png"
            setup_grid()
            rotate_single_point(coords=coord)
            print_extras()
            print_point_data(coord)

    else:
        run_gui=True
        if run_gui:
            setup_grid()
            start_gui()
        else:
            row = 2
            column = 2
            setup_grid()
            coord = rotate_single_point(row=row, column=column)
            print_extras()
            print_point_data(coord)

main()
