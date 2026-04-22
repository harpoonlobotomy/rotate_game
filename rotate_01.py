"""want to make that game I saw in an add, where you have to correctly rotate clusters of 4 colours so they all line up."""

from PIL import Image, ImageDraw

def logger(string):
    logging = False#True
    if logging:
        print(f"[ LOGGER ] `{string}`")

def col_print(string):
    print_col_prints = False
    if print_col_prints:
        print(string)


#base_image = "better_differentiation.png"

class image_data:
    logger("start of image_data class (has no def init)")
    use_images_not_colours:bool = True # try to use tiled images instead of colours (not implemented)
    base_image:str=None
    filename:str=None
    is_fullscreen:bool = True

    grid_size = 5
    rotations_count:int = None
    region_size:tuple = (500, 500)
    difficulty = 1
    is_fullscreen = True
    padding = 5

    width:int=None
    height:int=None

    pixel_dict:dict={}

    start_screen=True # True if need to show the 'gallery' intro panel
    new_img_data:tuple[str, dict] = ()#new_image, coord_to_img_files # sending back from window so it's stored somewhere during the restart of window. bad way of doing it but sleep dep

    """[x, y coordinates] = (r, g, b values)"""

    def __init__(self):
        pass

class base_positions:
    logger("start of base_positions class (has no def init)")
    children_dict:dict = {}
    coord_dict:dict = {}
    coords_list:list = []

    ordered_children:dict = {}
    """ordered_children[centre_coordinates][position_str]"""

    def __init__(self):
        pass

    def set_dicts(self, children_dict):
        logger("set_dicts")
        self.children_dict = children_dict
        pass

    def align_children(self, selected_coord=None): # adding this so I can get the children in the correct 0,1,2,3 order to rotate properly.
        logger("align_children")
        # children = self.children_dict[coord]
        #print(f"Children dict: {self.children_dict}")
        for point, children in self.children_dict.items():
            point_x, point_y = point
            if selected_coord and point != selected_coord:
                print(f"selected_coord and point != selected cooord: {selected_coord}")
                continue
            self.ordered_children[point] = {}
            for child in children:
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
        #print(f"ORDERED CHILDREN AFTER generation in align_children:\n{self.ordered_children}")
        #print(f"self.ordered_children[point]: {self.ordered_children[point]}")
        #base_pos.ordered_children = self.ordered_children


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
        ordered_existing = list(i for i in order if i in children) # any reason to not just do this instead of making an exclusion list?
        #specified = list(i for i in order if not i in children)
        new_order = ordered_existing[1:] + ordered_existing[:1]
        #print(f"STARTING ORDER: {list(children)}\nNEW ORDER: {new_order}")

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
            #rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], img_data.pixel_dict[children[list(children)[new_index]]])
            rotated_children[list(children)[orig_index]] = (children[list(children)[new_index]], img_data.pixel_dict[children[list(children)[orig_index]]])

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
    #base_pos.get_row_and_column()
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

def generate_children(coords_list):
    logger("generate_children")
    child_dict = {}
    #base_pos.coords_list = coords_list
    for entry in coords_list:
        row, column = entry
        child_points = list((x, y) for (x, y) in coords_list if (((x == (row + 1) or x == (row - 1)) and (y == column))) or (x == row and (y == (column + 1) or y == (column - 1))))# + spacing) or y == (spaced_y - spacing)))
        #print(f"Central: {entry}\nChild points: {child_points}")
        child_dict[entry] = child_points
    return child_dict

def initial_setup(base_file=None):
    logger("initial_setup")
    if img_data.use_images_not_colours:
        if img_data.new_img_data and img_data.new_img_data[0] == base_file:
            print(f"new_img_data found for base file `{base_file}`: {img_data.new_img_data[0]}")
            base_file, coord_to_img_files, coords_list, image_size = img_data.new_img_data
        else:
            print(f"new_img_data not found for initial setup for base file {base_file}")
            from img_manipulation import generate_img_grid
            print("Going to generate_img_grid from ln274")
            base_file, coord_to_img_files, coords_list, image_size = generate_img_grid(base_file, img_data.region_size, grid_size=img_data.grid_size)
            img_data.new_img_data = base_file, coord_to_img_files, coords_list, image_size

        #clean_colours()
        #print(f"COORDS LIST before generate children: {coords_list}\n")
        logger("getting child dict in initial_setup")
        child_dict = generate_children(coords_list)
        base_pos.set_dicts(child_dict)
    return img_data.new_img_data

##### GUI #####

def start_gui(skip_splash=False):
    logger("start_gui")
    from rotate_gui_01 import splash_window, main_window
    if not skip_splash:
        splash_window()
    while True:
        outcome = main_window(img_data, base_pos)
        if outcome:
            break
    return outcome

def main():

    #output_filename = f"{base_image.replace(".png", "").split("/")[-1]}_output.png"
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
            outcome = None
            while True:
                #setup_grid()
                outcome = start_gui(skip_splash = True if outcome else False)
                if outcome and outcome == "Done":
                    exit()
                if "restart" in outcome and outcome != "restart":
                    outcome = outcome.replace("restart_", "")
                    outcome_filename = outcome.replace(".png", "").split("/")[-1]
                    print(f"for restart initial setup: base_file = {outcome}, filename: {outcome_filename}")
                    initial_setup(base_file=outcome)#, filename = f"{outcome_filename}_output.png")

        else:
            row = 2
            column = 2
            setup_grid()
            coord = rotate_single_point(row=row, column=column)
            print_extras()
            print_point_data(coord)

if "__main__" == __name__:
    main()
