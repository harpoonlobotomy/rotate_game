"""want to make that game I saw in an add, where you have to correctly rotate clusters of 4 colours so they all line up."""

from PIL import Image, ImageDraw

def col_print(string):
    print_col_prints = False
    if print_col_prints:
        print(string)


base_image = "better_differentiation.png"

def get_point_spacing():
    """adds pixel_dict to img_data"""
    if img_data.base_image:
        with Image.open(img_data.base_image) as im:
            px = im.load()
            px_size = im.size

    else:
        print("No ability to generate images from naught yet, exiting.")
        exit()
    # note: (row, column) - so changing the first and not the second goes left>right.

    col_print(f"SPACING: {img_data.spacing}")
    spaced_x = int(img_data.dot_radius/2)

    for i in range(0, int(img_data.height/img_data.spacing)):
        col_print(f"img_data.height: {img_data.height} // i: {i}")
        spaced_y = int(img_data.dot_radius/2)

        for ib in range(0, int(img_data.width/img_data.spacing)):
            pixel_coord = (i, ib)
            col_print(f"PIXEL COORD: {pixel_coord}\nwidth: {img_data.width}, height: {img_data.height}")
            if (spaced_y > img_data.width) or (spaced_x > img_data.height):
                continue
            pixel_coord_2 = (spaced_x, spaced_y)
            img_x, img_y = px_size
            pixel_coordinate = ((i * img_data.spacing), (ib * img_data.spacing))
            col_print(f"px[pixel_coord_2: {px[pixel_coord_2]}]")
            col_print(f"pixel_coordinate: {pixel_coordinate}]")
            col_print(f"pixel_coord_2: {pixel_coord_2}]")
            #img_data.pixel_dict[pixel_coord] = px[pixel_coord_2]
            img_data.pixel_dict[pixel_coord] = px[pixel_coordinate]
            col_print(f"img_data.pixel_dict[pixel_coord]: {img_data.pixel_dict[pixel_coord]}")
            spaced_y = (spaced_y+img_data.spacing)
            img_data.str_to_coord[str(pixel_coord)] = pixel_coord

        spaced_x = spaced_x + img_data.spacing

class image_data:

    use_images_not_colours:bool = True # try to use tiled images instead of colours (not implemented)
    base_image:str=None
    filename:str=None
    is_fullscreen:bool = True

    grid_size = 6
    region_size:tuple = (640, 480)
    difficulty = 1
    background_colour = "maroon"
    is_fullscreen = True
    padding = 5

    width:int=None
    height:int=None
    dot_radius:int=72
    spacing_between_edges:int=13
    pixel_dict:dict={}

    start_screen=True # True if need to show the 'gallery' intro panel
    new_img_data:tuple[str, dict] = ()#new_image, coord_to_img_files # sending back from window so it's stored somewhere during the restart of window. bad way of doing it but sleep dep

    str_to_coord:dict = {}
    """[x, y coordinates] = (r, g, b values)"""

    def __init__(self):
        pass

    def set_file_data(self, base_file=None, filename=None, width=None, height=None, dot_radius=72, spacing_between=13):
        self.too_large = False
        import json
        settings = "rotate_settings.json"
        with open(settings, "r") as settings:
            settings_data = json.load(settings)

        self.grid_size = settings_data["grid_size"]
        self.difficulty = settings_data["difficulty"]
        self.background_colour = settings_data["background_colour"]
        self.region_size = settings_data["screen_size"]
        self.is_fullscreen = settings_data["fullscreen"]

        if base_file:
            print(f"BASE FILE: {base_file}, type: {type(base_file)}")
            if isinstance(base_file, Image.Image):
                print(f"DIR base_file: {dir(base_file)}")
                width, height = im.size
            else:
                with Image.open(base_file) as im:
                    width, height = im.size
                self.base_image = base_file
                col_print(f"width, height: {width, height}")

        """ Here need to set a default image size and scale if needed. Spacing etc needs to also change. This is set up for a premade grid, so maybe a whole different one that just goes by x pixels directly. Not sure."""
        self.filename = filename

    #if filename != "image_name_for_testing.png":

        self.width = width
        self.height = height

        if not self.width or not self.height:
            col_print(f"Not self.width or self.height: {self.width} / {self.height}")

        self.dot_radius = dot_radius
        self.spacing_between_edges = spacing_between

        self.spacing = int(dot_radius/2) + spacing_between + int(dot_radius/2)

        target_x, target_y = eval(self.region_size)
        target_x = int(target_x/2)
        target_y = int(target_y/2) # arbitrarily, img is half the screen size. Will figure a better way of doing it. Maybe an interim screen for image selection before the grid is generated, and the region area is defined then?
        if abs(target_x - width) > 100 or abs(target_y - height) > 100:
            print("IMAGE IS THE WRONG SIZE.")
            width_diff = abs(target_x - width)
            print(f"Width diff: {width_diff}")
            height_diff = abs(target_y - height)
            print(f"Height diff: {height_diff}")
            if width_diff > height_diff:
                print("Is more wrong in width than height. How/why does this matte? No idea.")
        with Image.open(base_file) as im:
            im = im.resize(size=(target_y, target_y))
            with Image.new("RGBA", size=(target_y, target_y)) as new_im:
                new_im.paste(im)
                new_im.save(self.filename, format="png")
                img_data.base_image = self.filename
                print(f"Base image saved at: {self.filename}")

        self.width = target_y
        self.height = target_y
        col_print(f"width at end: {self.width}")
        col_print(f"height at end: {self.height}")
        self.spacing = int(self.width / self.grid_size)
        self.dot_radius = int((self.spacing-5)/2)
        self.spacing_between_edges = int(self.spacing - self.dot_radius)
        col_print(f"self.dot_radius/spacing_between edges: {self.dot_radius} / {self.spacing_between_edges}")


    def get_child_dict(self):
        child_dict = {}

        for points in self.pixel_dict.keys():
            #print(f"Points for child_dict: {points}")
            spaced_x, spaced_y = points
            #print(f"spaced x: {spaced_x} / spaced_y: {spaced_y}")
            #child_points = list((x, y) for (x, y) in self.pixel_dict.keys() if (((x == (spaced_x + self.spacing) or x == (spaced_x - self.spacing)) and (y == spaced_y))) or (x == spaced_x and (y == (spaced_y + self.spacing) or y == (spaced_y - self.spacing))))# + spacing) or y == (spaced_y - spacing)))
            child_points = list((x, y) for (x, y) in self.pixel_dict.keys() if (((x == (spaced_x + 1) or x == (spaced_x - 1)) and (y == spaced_y))) or (x == spaced_x and (y == (spaced_y + 1) or y == (spaced_y - 1))))# + spacing) or y == (spaced_y - spacing)))
            #print(f"CHIld points: {child_points}")
            child_dict[points] = child_points
        return child_dict

class base_positions:

    children_dict:dict = {}
    coord_dict:dict = {}
    coords_list:list = []

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


    def align_children(self, selected_coord=None): # adding this so I can get the children in the correct 0,1,2,3 order to rotate properly.
        # children = self.children_dict[coord]
        print("in align_children")
        for point, children in self.children_dict.items():
            point_x, point_y = point
            if selected_coord and point != selected_coord:
                continue
            self.ordered_children[point] = {}
            for child in children:
                #print(f"Child in children: {child}")
                x, y = child
                if x == point_x and y == (point_y-1):
                    self.ordered_children[point]["top"] = child

                elif x == point_x and y == (point_y+1):
                    self.ordered_children[point]["bottom"] = child

                elif x == (point_x + 1) and y == point_y:
                    self.ordered_children[point]["right"] = child

                elif x == (point_x - 1) and y == point_y:
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
        print(f"Starting image made: {img_data.filename}")

def select_coords(column:int=2, row:int=2):
    selected_coord = (base_pos.coord_dict["columns"][column], base_pos.coord_dict["rows"][row])
    return selected_coord

img_data = image_data()
base_pos = base_positions()

def setup_grid(skip_making_image=True):
    base_pos.get_row_and_column()
    if not skip_making_image:
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

def clean_colours():
    def get_col_from_col_code(red, blue, green):
        """col_code is a tuple from pixel_dict, returns a "#FFFFFFF" style value."""
        return '#%02x%02x%02x' % (red, green, blue)
    for coord, colour_code in img_data.pixel_dict.items():
        if  len(colour_code) == 4:
            r, g, b, a = colour_code
            if a < 150:
                r = g = b = 0

            colour_code = get_col_from_col_code(r, b, g)
            img_data.pixel_dict[coord] = colour_code

def generate_children(coords_list):
    child_dict = {}
    #base_pos.coords_list = coords_list
    for entry in coords_list:
        row, column = entry
        child_points = list((x, y) for (x, y) in coords_list if (((x == (row + 1) or x == (row - 1)) and (y == column))) or (x == row and (y == (column + 1) or y == (column - 1))))# + spacing) or y == (spaced_y - spacing)))
        #print(f"Central: {entry}\nChild points: {child_points}")
        child_dict[entry] = child_points
    #print(f"child_dict: {child_dict}")
    return child_dict

def initial_setup(base_file=None, filename=None, width=None, height=None, dot_radius=72, spacing_between=13):

    if img_data.use_images_not_colours:
        print(f"use images not colours {img_data.use_images_not_colours}")
        if img_data.new_img_data and img_data.new_img_data[0] == base_file:
            print(f"new_img_data found for base file `{base_file}`: {img_data.new_img_data[0]}")
            base_file, coord_to_img_files, coords_list, image_size = img_data.new_img_data
        else:
            print(f"new_img_data not found for initial setup for base file {base_file}")
            from img_manipulation import generate_img_grid
            print("Giong to generate_img_grid from ln422")
            base_file, coord_to_img_files, coords_list, image_size = generate_img_grid(base_file, img_data.region_size, grid_size=img_data.grid_size)
            img_data.new_img_data = base_file, coord_to_img_files, coords_list, image_size

        #clean_colours()
        print(f"COORDS LIST before generate children: {coords_list}\n")
        child_dict = generate_children(coords_list)
        #child_dict = get_img_children(coord_to_img_files)

    """else:
    ## Now here, both routes to restart with an image go through img_manip first. So instead of getting the dict here, it should go through the dict already made in img_manip.
        img_data.set_file_data(base_file, filename, width, height, dot_radius, spacing_between)
        get_point_spacing()
        clean_colours()
        child_dict = img_data.get_child_dict()"""

    base_pos.set_dicts(child_dict)

##### GUI #####

def start_gui():
    from rotate_gui_01 import splash_window, main_window
    splash_window(img_data)
    while True:
        outcome = main_window(img_data, base_pos)
        if outcome:
            break
    return outcome

def main(base_image=base_image):

    output_filename = f"{base_image.replace(".png", "").split("/")[-1]}_output.png"
    #initial_setup(base_file=base_image, filename = output_filename)

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
            while True:
                setup_grid()
                outcome = start_gui()
                if outcome and outcome == "Done":
                    exit()
                if "restart" in outcome:
                    outcome = outcome.replace("restart_", "")
                    outcome_filename = outcome.replace(".png", "").split("/")[-1]
                    print(f"for restart initial setup: base_file = {outcome}, filename: {outcome_filename}")
                    initial_setup(base_file=outcome, filename = f"{outcome_filename}_output.png")

        else:
            row = 2
            column = 2
            setup_grid()
            coord = rotate_single_point(row=row, column=column)
            print_extras()
            print_point_data(coord)

main()
