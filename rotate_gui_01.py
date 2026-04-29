from time import sleep
import math
import FreeSimpleGUI as sg

scramble_icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACRElEQVRYR82XsU7DQAyGc+pIJzrBiMTIM8CUShVdKnVgBMEzsDGw8QwgMTJU6gICKRM8AzsrU5lgRId8OV98jp07REWbqZc69uf/fI5jiozLWmuNMRmWjYm1tjAZDyW9QnBwC778TxVkuH3i/qveb4NtCiILABPhAObroYGZ9IrydRYA4EeOCp0ANHt06NSggeHGpOcCSwBePTXO+gLw7FUFfPaSAtEzSkGKCkjBncaf93EBkuAaQAoiAsDAWPWkkOrAFIAF12pAKmB6MhwADcyD03UAUDJHeeAYssyjNdoBiFHljsWuV+WjdDdUPwcQjf1NPNKggGs0q7ocQE6Ho91NgzXDp/qvapTsmq6X9MfF+gB83BwURxc76k5QBcCWX4PZeXPLK4Ad024ctrsnWFMFqFMJpAsgCk62oBMATlI1araAZ6U5Bf+q7fy7VqE/Dj1DzB6PMQIsrvdF6bmskl2wweAeIBwz9saMAnUpAIYpAB4csoXLdT/WtsvdeStJ2NZwCqTCiiCqUYEKRGAkcw1ACu5KBQHA8ebpc2tvOUCrE/rgITDKTWpAC75eAKtqw65efvMySrVsTCRjGG6GVngo93WMALxgoX5ofxicvbh1OIp+pG8NtXxkTg0kGgBmjiB0CMkaSHgNaNuSAkA/qACuiRKtEVCdiiWIcus4sN5dvqm1SwG6grsi7DoBHIICwHMahFADy/ku+HcAPCFYSByg2psWi+lVS0SqwFK+DfEFIwGIW0hGsj8DcBVyu2bOhyn4+gEUzdgcAabqsgAAAABJRU5ErkJgggAA'
def logger(string):

    logging = False#True
    if logging == True:
        print(string)

def extra_print(string):
    print_col_prints = False
    if print_col_prints:
        print(string)

def make_settings_file(settings):

    default_settings = {
        "allow_resize": True,
        "grid_size": 4,
        "background_colour": "#00345B",
        "fullscreen": True,
        "maximised_size": "(1920, 1027)",
        "main_window_size": "(1920, 1027)",
        "thumbnail_size": 200,
        "gallery_region_size": "(1333, 887)"
    }

    import json
    with open(settings, 'w') as outfile:
        json.dump(default_settings, outfile)

class theme_data():

    def __init__(self):
        logger("initing theme_data")
        import json, os
        settings = "rotate_settings.json"
        if not os.path.isfile(settings):
            make_settings_file(settings)

        with open(settings, "r") as settings:
            settings_data = json.load(settings)

        self.settings_data = settings_data
        self.allow_resize = settings_data["allow_resize"]
        self.grid_size = settings_data["grid_size"]
        self.background_colour = settings_data["background_colour"]
        self.maximised_size = settings_data["maximised_size"]
        if isinstance(self.maximised_size, str):
            self.maximised_size = eval(self.maximised_size)
        if self.allow_resize:
            self.window_size = settings_data["main_window_size"]
            self.start_maximised = settings_data["fullscreen"]
            self.thumbnail_size = settings_data["thumbnail_size"]
        else:
            self.window_size = (1360, 850)#self.maximised_size
            self.start_maximised = True
            self.thumbnail_size = 200

        self.gallery_region_size = settings_data["gallery_region_size"]

        if isinstance(self.window_size, str):
            self.window_size = eval(self.window_size)

        print(f"theme.window_size: {self.window_size}, type: {type(self.window_size)}")
        self.screen_x = self.window_size[0]#480
        self.screen_y = self.window_size[1]

        self.gallery_columns = 5

        self.is_grid_screen = False #marker for which panels are in view.

      ### panel areas for fn hinting ###
        # main window
        self.main_window:sg.Frame = None
        self.central:sg.Column = None
        # panels in central: #
        self.gallery:sg.Column = None
        self.grid_panel:sg.Column = None
        self.grid_box:sg.Graph = None

        # panels in side: #
        self.true_side:sg.Column = None

        self.settings_panel_width_bar:tuple = (271,1)

    theme_dict:dict = {
        "arcade": {'BACKGROUND': "#38354a",#31374e",
                    'TEXT': "#d8d8d8",
                    'INPUT': "#45523F",
                    'TEXT_INPUT': "#f5db74",
                    'SCROLL': "#003e9b",
                    'BUTTON': ('black', "#589CB8"),#"#ffda57"),##ffd657"),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 3,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0,
                    'dot_colour': "#d35700",
                    'font': "courier 14 bold",
                    "alt_tally_bg": "#433e5e",
                    "title_bg": "#382b43",#362b43",
                    #"title_bg": "#31374e",
                    "gold_text": "#f0c762",# "#ffd365",
                    'ACCENT1': '#FF0266','ACCENT2': '#FF5C93','ACCENT3': '#C5003C',
                    }}

    sg.theme_add_new('arcade', theme_dict["arcade"])
    theme_name = "arcade"
    sg.theme(theme_name)

    maximised_size:tuple = (0,0)
    game_started = False
        #sg.theme('farkle_tan')
    difficulty:int = 0
    """0 = easy, 1 = medium, 2 = hard"""
    difficulty_str:str = "easy"

    difficulty_legend = {
        0: "easy",
        1: "standard",
        2: "hard"
    }

    clicks = 0
    #background_colour = "#82000F"
    #background_colour = "#243D47"
    background_colour = "#00345B"
    highlight_button_colour = "#5E9980"
    button_colour = "#589CB8"
    start_screen:bool = True # is what shows the 'gallery' and lets me get the region dimensions.

    def save_settings(self):
        # TODO: If settings json not found, generate on first startup with default vals.
        self.settings_data["grid_size"] = self.grid_size
        self.settings_data["background_colour"] = self.background_colour
        #self.settings_data["screen_size"] = ##   "screen_size": "(1920, 1080)",
        self.settings_data["fullscreen"] = self.start_maximised
        self.settings_data["maximised_size"] = str(self.maximised_size)
        self.settings_data["main_window_size"] = str(t.window_size)
        self.settings_data["thumbnail_size"] = self.thumbnail_size
        self.settings_data["gallery_region_size"] = str(self.gallery_region_size)
        import json
        settings = "rotate_settings.json"
        with open(settings, "w") as settings:
            json.dump(self.settings_data, settings, indent=2)

t = theme_data()

#sg.main_global_pysimplegui_settings()
def get_col_from_col_code(red, green, blue):
    """col_code is a tuple from pixel_dict, returns a "#FFFFFFF" style value."""
    return '#%02x%02x%02x' % (red, green, blue)

class buttonInstance:

    def __init__(self, coords):
        self.coords = coords
        """buttonInstance.coords == tuple"""
        self.target_image = g.clean_dict[coords]["target_image"]
        self.current_image = self.target_image


    def __repr__(self):
        return f"self.coords: {self.coords}  self.current_image: {self.current_image}  self.target_image: {self.target_image}"

    def change_image(self, new_image):
        self.current_image = new_image

class buttonClass:

    def __init__(self):
        logger("initing buttonClass")
        self.by_coord:dict[tuple: buttonInstance] = {}
        """self.by_coord : [tuple coords] = <buttonInstance>"""
        self.clean_dict:dict = {} # for the post-converted '36,36' > '0,0' / '121,36' > '1, 0' < - is this still accurate? #TODO

    def clear_buttondata(self):
        self.by_coord:dict = {}
        self.clean_dict:dict = {}

    def img_from_coords(button:buttonInstance, coords=None):#, row=None, column=None):
        """row_{row}_col_{column}.png"""
        logger(f"[ img_from_coords ]  button: {button} / coords: {coords}")
        if button:
            if button:
                return button.target_image

        if not coords:
            print(f"No row/column found from `button` : {button} / `row` : {row} / `column` : {column}")

        else:
            row, column = coords
            img_filename = f"row_{row}_col_{column}.png"
            return img_filename

    def button_press(self, coord:buttonInstance):
        logger(f"BUTTON PRESS: {coord}")
        print(f"BUTTON PRESS: {coord}")
        #print(f"g.clean_dict[coord]: {g.clean_dict[coord]}")
        rotated_children = {}
        if isinstance(coord, str) or isinstance(coord, tuple):
            if isinstance(coord, str):
                coord = eval(coord)
            children = g.clean_dict[coord]["children"]
        else:
            children = coord.children
        reordered = g.reindex_children(children)
        for child in children:
            orig_index = list(children).index(child)
            new_index = list(reordered).index(child)
            rotated_children[list(children)[orig_index]] = (children[list(children)[new_index]], b.by_coord[children[list(children)[orig_index]]].current_image)

        return rotated_children

b = buttonClass()

"""def splash_window():
    logger("splash window")
    #Using the splash screen to get the size of the maximised window

    splashscreen_window = sg.Window(' •• SCRAMBLE ••', layout=[[sg.Canvas(size=(1,1))]], keep_on_top=True, finalize=True, margins=(10,10), no_titlebar=True, alpha_channel=0)

    splashscreen_window.maximize()

    #while True:
    #    event, _ = splashscreen_window.read(timeout=100)
    #    #print(f"splashscreen_window.Size: {splashscreen_window.Size}")
    #    if splashscreen_window.get_screen_dimensions() and splashscreen_window.get_screen_dimensions() != (None, None):   #fullscreen version
    #        #t.screen_x, t.screen_y = splashscreen_window.get_screen_dimensions()
    #        splashscreen_window.close()

        if splashscreen_window.is_closed():
            break"""

class gridClass:

    def __init__(self):
        logger("init gridClass")
        #self.unordered_child_dict = {} # don't imagine I need this but here for now.
        self.ordered_children = {}
        self.puzzle_img_filename:str = None
        self.coord_to_img_files:dict = {} # < -- [row][column] > onward
        self.clean_dict = {} # < -- [coords] > onward
        self.bbox_dict = {}
        self.grid:sg.Graph = None#self.make_grid(simple=True)
        self.rows:int = t.grid_size
        self.cols:int = t.grid_size
        self.padding = 8

        self.thumbnail_width = t.thumbnail_size
        self.img_width = t.screen_y/2 if t.screen_x > t.screen_y else t.screen_x/2
        self.cell_w = int(self.img_width / self.rows)
        self.cell_h = int(self.img_width / self.cols)
        self.target_image_size = (500, 500) # derived from element size, not img pixels.

        self.gallery_panel = None # just testing
        self.grid_region_size:tuple[int, int]  = (50,50) # <- just the grid area itself (img sized)
        self.start_screen = True # whether to open window to the gallery or not
        self.rotations_count = None

        self.gallery_list = [] # list of filepaths for gallery images.

    def clear_grid_data(self):
        print("run this to clear all grid data.\nalso use this to trigger an equivalent fn in buttonClass.")
        self.ordered_children = self.clean_dict = self.bbox_dict = self.coord_to_img_files = self.unordered_child_dict = {}
        self.puzzle_img_filename:str = None
        self.grid:sg.Graph = None
        self.target_image_size:int = (500, 500)
        self.grid_region_size:tuple[int, int]  = (50,50)
        self.grid_panel_size:tuple[int, int] = (125, 125)
        b.clear_buttondata()

    def make_grid(self, simple=True):

        if simple:
            t.screen_x, t.screen_y
            if t.screen_x > t.screen_y:
                width = t.screen_y*.66
            else:
                width = t.screen_x*.66
        else:
            width = g.target_image_size[0]

        self.grid = sg.Graph(
            canvas_size=(width, width),
            graph_bottom_left=(0, width),
            graph_top_right=(width, 0),
            enable_events=True,
            key="grid", pad=16, background_color="aqua"#, expand_x=True, expand_y=True#, visible=False
        )
        return self.grid

    def set_up_gridClass(self):
        self.rows = t.grid_size
        self.cols = t.grid_size # separate in case I do rectangles later.
        self.cell_w = int(self.target_image_size[0] / self.cols)
        self.cell_h = int(self.target_image_size[0] / self.rows)

        self.white_square:str = None # to use for flashing hints
        self.white_w_transparency:str = None # to use for flashing hints
        self.white_square_width:int = 0

    def reindex_children(self, children):
        order = ["top", "right", "bottom", "left"]
        if len(children) == 2 or len(children) == 4:
            children = list(children)[1:] + list(children)[:1]
            return children
        ordered_existing = list(i for i in order if i in children)
        new_order = ordered_existing[1:] + ordered_existing[:1]

        return new_order

    def order_children(self, children):
        order = ["top", "right", "bottom", "left"]
        children_list = list(i for i in order if i in children)
        new_children = {}
        for child in children_list:
            new_children[child] = children[child]
        return new_children


    def align_children(self, selected_coord=None, unordered_children={}): # adding this so I can get the children in the correct 0,1,2,3 order to rotate properly.
        logger("align_children")
        for point, children in unordered_children.items():
            #print(f"point, children in unordered_child_dict: {point} / {children}")
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
            #print(f"self.ordered_children[point] after: {self.ordered_children[point]}\n")

    def generate_children(self, coords_list):
        logger("generate_children")
        child_dict = {}
        for entry in coords_list:
            row, column = entry
            child_points = list((x, y) for (x, y) in coords_list if (((x == (row + 1) or x == (row - 1)) and (y == column))) or (x == row and (y == (column + 1) or y == (column - 1))))
            child_dict[entry] = child_points
        return child_dict

    def make_clean_dict(self):
        logger("make_clean_dict")
        if not g.coord_to_img_files:
            print(f"No new_img_data: {g.coord_to_img_files}")
            return

        if g.coord_to_img_files:
            print("new_img_data found")
            for row_no in g.coord_to_img_files:
                for col_no in g.coord_to_img_files[row_no]:
                    filename = g.coord_to_img_files[row_no][col_no]
                    coord = row_no, col_no
                    self.clean_dict[coord] = {"children": g.ordered_children[(row_no, col_no)], "target_image": filename}


g = gridClass()


def initial_setup(base_file):
    logger("running initial_setup")

    from img_manipulation import raw_img_data

    print("Going to generate_img_grid from ln338")
    g.puzzle_img_filename, g.coord_to_img_files, g.bbox_dict, coords_list, g.img_width = raw_img_data.generate_img_grid(base_file, g.target_image_size, grid_size=t.grid_size, padding = g.padding)

    unordered_child_dict = g.generate_children(coords_list)
    g.align_children(unordered_children=unordered_child_dict)

    g.make_clean_dict()

    return


def main_window(start_hidden=True):
    logger("main_window of rotate_gui_01")
    sg.theme(t.theme_name)
    if g.start_screen:
        g.clear_grid_data()#b.clear_buttondata()

    def update_window_size_data():
        window.refresh()
        t.thumbnail_size = g.thumbnail_width
        t.window_size = window.size
        t.gallery_region_size = window["gallery"].get_size()
        if window.size == t.maximised_size:
            t.start_maximised = True
        else:
            t.start_maximised = False
        t.save_settings()

    def make_gallery_list(image=None, make_squares = True, force_thumbnails = False):

        force_make = False
        print("Making thumbnails.")
        from img_manipulation import make_square_png
        squared_dir, thumbs_dir, thumb_list = make_square_png(add_image=image, make_squares=make_squares, make_thumbnails=True, thumbnail_size = int(g.thumbnail_width), force_make=force_make, force_thumbnails = force_thumbnails)

        g.gallery_list = thumb_list
        print("thumbnails made")

    h_sep_padding = (20,10)

    make_gallery_list(make_squares=True)
    font_size = 14

    show_stretchers = "yellow"
    debug_colours = False#True

    std_background_1 = "gray"
    std_background_2 = "#38354a"

    def change_image():
        file_selected = sg.popup_get_file(message="Select a .png file to use as the base image", title="Select a .PNG file", file_types=(("PNG Files", "*.png"),))
        if file_selected:
            return file_selected

    def update_clicks(reset=False, newline=True):
        if reset and reset == "clicks":
            t.clicks = 0
            text = f"Clicks: {t.clicks}"
        elif not reset:
            t.clicks += 1
            text = f"Clicks: {t.clicks}"
        else:
            t.clicks = 0
            text = reset
        extra = "\n" if newline else ''
        window["click_counter"].update(f"{extra}{text}")

    def check_if_completed(record_incomplete=False):
        """RETURNS LIST OF BUTTON INSTANCES"""
        not_complete = False
        incorrect_buttons = []
        for button in b.by_coord.values():
            if button.current_image != button.target_image:
                not_complete = True
                if record_incomplete:
                    incorrect_buttons.append(button)

        if record_incomplete and not_complete:
            return incorrect_buttons

        if not not_complete:
            update_clicks(reset = f"Completed with {t.clicks} clicks!\nScramble to play again.")


    def show_incorrect(fix_incorrect=False):
        incorrect_buttons = check_if_completed(record_incomplete=True)
        """incorrect_buttons == list of buttonInstances"""

        if not incorrect_buttons:
            print("No incorrect buttons to highlight.")
            return
        print(f"\n\ng.cell_w: {g.cell_w}\n\n")
        #g.cell_w: 156
        from time import sleep
        for button in incorrect_buttons:
            button:buttonClass.buttonInstance
            x, y = button.coords
            if fix_incorrect:
                white_square = g.white_square
            else:
                white_square = g.white_w_transparency

            if not g.white_square_width or g.white_square_width != int(g.cell_w-(g.padding*2)): # this weird hardcode is the thumbnail size. I need to test various sizes to get a formula in place instead of the current sequence of ints etc.
                white_square = None

            if not white_square:
                from img_manipulation import make_square
                white_square, square_width = make_square(g.cell_w, "white", g.padding, transparent_centre=True if not fix_incorrect else False)
                g.white_square_width = square_width
                if fix_incorrect:
                    g.white_square = white_square
                else:
                    g.white_w_transparency = white_square

            button_box = g.bbox_dict[x][y]
            g.grid.draw_image(filename=white_square, location = (button_box[0][0]+(g.padding/2), button_box[0][1]+(g.padding/2)))
            unpressed_button(button_box[0], button_box[1])

            window.refresh()
            sleep(.05)

        window.refresh()
        sleep(.5)

        for button in incorrect_buttons:
            button:buttonInstance
            if fix_incorrect:
                button.current_image = button.target_image

            new_image = button.current_image
            x, y = button.coords
            update_clicked_square(x, y, new_image, click_off=True)
            #window[str(button.coords)].update(button_color=("black", saved_colours[button]))
            window.refresh()
            sleep(.03)
        window.refresh()

            #restore_colour =

    def set_solved():
        show_incorrect(fix_incorrect=True)
        update_clicks(reset="Waiting to scramble...\n", newline=True)

    def rotate_children(rotated_children, update=False):

        for _, child_coords in rotated_children.items():
            child_coords, child_image = child_coords
            b.by_coord[child_coords].change_image(child_image)

            row, column = child_coords
            update_clicked_square(row, column, child_image, click_off=True)

    def scramble_colours():
        logger("scramble_colours")
        window["click_counter"].update("\nGood luck!")

        points_to_rotate = {
            "0": 6,
            "1": 12,
            "2": 20
        }

        no_of_rotations = points_to_rotate[str(t.difficulty)] # thinking instead of difficulty defining rotations, it's grid size. Or possible both. Advanced mode where you can set no of rotations _ grid size probably. But for now, difficulty=grid size.
        # So instead of that... what, always 2/3rds of the grid? That feels like an advanced setting option too. At least half. I like the idea of at least some being in the right place.

        import random
        from time import sleep
        if g.rotations_count:
            number_of_clicks = g.rotations_count
        else:
            number_of_clicks = random.randint(1,3)
        buttons_to_click = random.choices(population=list(b.by_coord), k=int(len(b.by_coord)/3))
        for button in buttons_to_click:
            rotated_children = b.button_press(button)
            if number_of_clicks > 1:
                for _ in range(number_of_clicks-1):
                    rotate_children(rotated_children, update=False)
                    sleep(.02)
                    window.refresh()
                    #col_print(f"Children to rotate: {rotated_children}")
                    #update_clicked_square(row, column, click_off=False)
            #print(f"ROTATED CHILDREN: {rotated_children}")
            rotate_children(rotated_children)
        t.clicks = 0


    def make_button(coord):
        #print(f"about to make button for coord")#: {coord}\ng.clean_dict:\n{g.clean_dict}\n\n")
        button_inst = buttonInstance(coord)
        b.by_coord[coord] = button_inst


    def unpressed_button(top_left, bottom_right):
        g.grid.draw_rectangle(top_left=top_left, bottom_right=bottom_right, line_color="black", line_width=2)
        g.grid.draw_rectangle(top_left=(top_left[0]+1, top_left[1]+1), bottom_right=(bottom_right[0]-1, bottom_right[1]-1), line_color="white", line_width=1)


    def initial_grid_drawing():
        logger("initial_grid_drawing")

        b.by_coord = {}
        print("about to draw image")
        g.grid.draw_image(filename=g.puzzle_img_filename, location=(0, 0))

        print(f"g.width: {g.img_width} // g.height: {g.img_width}")
        for row, column in g.bbox_dict.items():
            for tile in column:
                make_button((row, tile))
                unpressed_button(g.bbox_dict[row][tile][0], g.bbox_dict[row][tile][1])#top_left, bottom_right)
        return


    def update_clicked_square(row, column, new_image=None, click_off=False):

        if row > t.grid_size -1 or column > t.grid_size-1:
            #print(f"Clicked a grid reference that shouldn't exist: {row},{column}. The grid size is {g.grid_size}")
            return
        button_box = g.bbox_dict[row][column]

        if not new_image:
            target_button = b.by_coord[(row, column)]
            filename = target_button.current_image

        else:
            filename = new_image

        if click_off:
            """
            REMINDER: THIS:
             (button_box[0][0]+(g.padding/2), button_box[0][1]-(g.padding/2)))
            is looking for TOP LEFT CORNER ONLY.
            """
            #print(f"g.padding = {g.padding}. 1/2 g.padding = {g.padding/2}. g.cell_w = {g.cell_w} // g.cell_w + g.padding/2 = {g.cell_w + (g.padding/2)}")
            #print(f"click_off draws image here: \n\n{button_box[0][0]+(g.padding/2), button_box[0][1]+(g.padding/2)}\n\n")
            g.grid.draw_image(filename=filename, location = (int(button_box[0][0]+(g.padding/2)), int(button_box[0][1]+(g.padding/2))))
            unpressed_button(button_box[0], button_box[1])
        else:
            g.grid.draw_rectangle(top_left=button_box[0], bottom_right=button_box[1], line_color="white", line_width=2)

        window["grid"].update()


    def set_during_buttons_enable(enable=True, include_scramble = True):
        if include_scramble:
            window["set_scramble"].update(disabled = not enable)
        window["get_hint"].update(disabled = not enable)
        window["set_perfect"].update(disabled = not enable)


    def set_gridsize(new_gridsize):

        new_gridsize = int(new_gridsize.replace("gridsize_", ""))
        if new_gridsize != t.grid_size:
            t.grid_size = new_gridsize
            highlight_gridsize_button()
            return True

    def set_rotations():
        new_rotations = sg.popup_get_text(message=f"Current rotations count is {g.rotations_count}. Please enter a new rotation count.", title="Enter a new rotations count value")
        if new_rotations:
            if len(new_rotations.strip()) > 2:
                sg.popup("Please set a reasonable number of rotations.")
            try:
                new_rotations = int(new_rotations.strip())
                sg.popup(f"New rotations set to {new_rotations}. Changes will take effect next time you load an image or select from gallery.")
                g.rotations_count = new_rotations
                return new_rotations
            except Exception as e:
                print(f"Error: {e}")


    def fade_in_out(fade_in=False):

        end_val = 1 if fade_in else 0
        for i in range(0, 10):
            if fade_in:
                val = 1 * ((i + .1)/10)
            else:
                val = 1 - ((i + .1)/10)
            window.set_alpha(val)
            #window.refresh()
            sleep(.06)
        window.set_alpha(end_val)


    def setup_button(text, key=None, size=(None, None), font="courier 12", start_disabled=False, colour=t.button_colour, tooltip=None, padding = None):
        if not key:
            if text:
                key = f"{text}_key"
        if not size:
            size = (len(text) + 2, 1)
        return sg.Button(button_text=text, size=size, key=key, use_ttk_buttons=True, auto_size_button=True, font=font, disabled_button_color="gray", disabled=start_disabled, button_color=colour, tooltip=tooltip, pad=padding if padding else (5,4))


    def setup_text(text, key=None, size=None, font="courier 16", padding=None):
        colour = "white"
        if not key:
            key = f"{text}_key"

        return sg.Text(text=text, key=key, size=size if size else (None, None), justification="center", text_color=colour, font=font, pad=padding if padding else 2)

    def get_panel_dimensions():
        window.refresh()
        t.central = window["central"].get_size()

        g.grid_panel_size = window['grid_panel'].get_size()
        g.grid_panel_size = (g.grid_panel_size[1], g.grid_panel_size[1])
        g.target_image_size = (int(t.central[1]*.82), int(t.central[1]*.82))

    def generate_new_grid(selected_imgname, user_selected=False):

        window["gallery_text"].hide_row()
        window["gallery"].hide_row()
        window["gallery"].expand(expand_y=False, expand_row=False)
        #print(f"squared region size: {g.grid_panel_size}")
        #print(f"target image size (80% of grid region size): {g.target_image_size}")
        if not user_selected:
            g.puzzle_img_filename = selected_imgname.replace("_thumbnails", "").replace("_thumbnail", "_squared")

        g.coord_to_img_files = {}

        g.start_screen=False
        initial_setup(g.puzzle_img_filename)

        g.set_up_gridClass()
        print(f"g.target_image_size before set_up_grid: {g.target_image_size}")
        g.grid.set_size(g.target_image_size)
        print(f"g.grid.get_size() just after setup and gridClass setup: {g.grid.get_size()}")
        print("After set_up_grid")

        window["gallery_text"].hide_row()
        window["grid"].unhide_row()
        #window["grid"].update()
        window["grid_panel"].unhide_row()
        window["grid_panel"].expand(expand_y=True, expand_row=True)
        update_clicks(reset="Waiting to scramble...\n", newline=True)
        window["click_counter"].unhide_row()
        print(f"grid.canvassize: {g.grid.CanvasSize}")
        graph_bottom_left=(0, g.target_image_size[0])
        g.grid.BottomLeft = graph_bottom_left
        graph_top_right=(g.target_image_size[0], 0)
        g.grid.TopRight = graph_top_right

        initial_grid_drawing()
        #window["grid_panel"].update()
        #window.refresh()

    def get_gallery_and_thumbnail_size():
        print(f"g.target_image_size: {g.target_image_size}") # it's only 2% off from what I gotby eye for the gallery region, so just use it again here.
        thumbnail_max_width, thumbnail_max_height = g.target_image_size
        no_of_rows = math.ceil(len(g.gallery_list) / t.gallery_columns)
        thumbnail_max_width = thumbnail_max_width/t.gallery_columns
        thumbnail_max_height = thumbnail_max_height/no_of_rows
        print(f"thumbnail_max_weight: {thumbnail_max_width}, thumbnail_max_height: {thumbnail_max_height}")
        if thumbnail_max_height < thumbnail_max_width:
            return thumbnail_max_height
        else:
            return thumbnail_max_width

    def move_to_gallery():
        """ set the appropriate buttons, text output etc for the 'gallery' screen.\nAlso clear grid data + button associations."""

        window["click_counter"].hide_row()
        window["grid_panel"].hide_row()
        window["gallery"].unhide_row()
        get_panel_dimensions()
        thumbnail_width = get_gallery_and_thumbnail_size()
        window["gallery"].expand(expand_row=True)
        window.refresh()
        print(f"gallery.get_size: {window["gallery"].get_size()}")
        g.start_screen=True
        t.is_grid_screen = False


    def move_to_grid(image_for_grid=None):
        """ set the appropriate buttons, text output etc for the 'grid' screen."""
        if not image_for_grid:
            image_for_grid = g.puzzle_img_filename

        t.is_grid_screen = True
        window["set_gallery"].update(disabled = False)
        generate_new_grid(image_for_grid)
        window["set_scramble"].update(disabled=False, button_color=t.highlight_button_colour)

    def calculate_gal_button_size():
        t.gallery.size
        len(g.gallery_list)

    def button_yielder():

        button_layout =  [
                        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                        ]

        for j in range(0, t.gallery_columns+1):
            button_layout.append(
                        [sg.Button(button_text="", image_source=g.gallery_list[i + (j * t.gallery_columns)], file_types=(("ALL files", ".*"),),
                                key=f"imgkey_{g.gallery_list[i + (j * t.gallery_columns)]}", image_size=(g.thumbnail_width,g.thumbnail_width), pad=5)
                                        for i in range(t.gallery_columns) if i + (t.gallery_columns * j) < len(g.gallery_list)])

        button_layout.append([sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)])

        return button_layout

    def set_ratios():
        print(f"Whole window size: {window.size}")
        print(f"Main window size: {t.main_window.get_size()}")

    def highlight_gridsize_button():

        gridsize_keys = list(i for i in window.AllKeysDict if isinstance(i, str) and i.startswith("gridsize_") and len(i) < 11)
        if gridsize_keys:
            for key in gridsize_keys:
                if key == f"gridsize_{t.grid_size}":
                    window[key].update(button_color = t.highlight_button_colour)
                else:
                    window[key].update(button_color = t.button_colour)

    def update_window_size(do_maximise=False, move_on=False):
        fade_on_grid_change = False
        if not t.allow_resize:
            return
        print("\n[ UPDATING WINDOW SIZE ]\n")
        new_screen_x, new_screen_y = window.size
        if new_screen_x == t.screen_x and new_screen_y == t.screen_y:
           print("Screen is the same size as it already was, ignoring.")
           return
        new_thumbnail_width = get_gallery_and_thumbnail_size()

        print(f"New_thumbnail_width: {new_thumbnail_width}")
        if new_thumbnail_width > 200:
            new_thumbnail_width = 200
        elif 200 - new_thumbnail_width < 20:
            return
        g.thumbnail_width = new_thumbnail_width
        if do_maximise:
            #print("do_maximise")
            if g.thumbnail_width == 200:
                #print("apparently g.thumbnail_width is already 200.")
                return
            g.thumbnail_width = 200 # default thumbnail size, can keep it safe somewhere later

        if fade_on_grid_change:
            fade_in_out(fade_in=False)
        t.screen_x = new_screen_x
        t.screen_y = new_screen_y

        if not t.is_grid_screen:
            make_gallery_list(force_thumbnails=True) # without this, 'image_size' just uses a smaller portion of the existing image

            #print("window.AllKeysDict:\n\n", window.AllKeysDict, "\n\n")
            for key in window.AllKeysDict:
                if isinstance(key, str) and key.startswith("imgkey_"):
                    thumb = window[key]
                    thumb:sg.Button
                    thumb.update(image_source=key.replace("imgkey_", ""), image_size=(g.thumbnail_width, g.thumbnail_width))
                    thumb.update()

        window.refresh()
        update_window_size_data()
        if fade_on_grid_change:
            fade_in_out(fade_in=True)
        t.save_settings()
        if move_on:
            if t.is_grid_screen:
                move_to_grid()
            else:
                move_to_gallery()


    grid = g.make_grid(simple=True)

    text_layout = [
            [setup_text(text="\nWaiting to scramble...\n", key="click_counter", size=(20,4))]
    ]

    grid_panel = [
            [grid],
            [sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour),
                    sg.Frame(title="", layout=text_layout, element_justification="center"),
                    sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour)]]

#### Side panel ###

    all_settings = [
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [setup_button("\n - scramble - \n", key="set_scramble", start_disabled=True, colour=t.highlight_button_colour, font="Courier 16 bold")],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [sg.HorizontalSeparator(p=h_sep_padding)],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [setup_button(text=f"Custom image", key="set_image")],
        [setup_button(text="Show incorrect", key="get_hint", start_disabled=True)],
        [setup_button(text="Start over", key="set_perfect", start_disabled=True)],
        [setup_button(text=f"Return to Gallery", key="set_gallery", start_disabled=True)],
        [sg.HorizontalSeparator(p=h_sep_padding)],
        [setup_button(text="Exit", key="exit")],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
    ]

    gridsize_buttons = [
        [setup_button(text=i, key=f"gridsize_{i}", padding = (2,2)) for i in (3, 4, 5, 6, 7)]
    ]

    adv_settings = [
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [sg.HorizontalSeparator(p=h_sep_padding)],
        [setup_button(text=f"Change grid size", key="adv_gridsize")],
        [sg.Column(layout = gridsize_buttons, key="gridsize_buttons", visible=True)],
        [setup_button(text=f"Change number of rotations", key="adv_rotations")],
        [sg.HorizontalSeparator(p=h_sep_padding)],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
            ]

    main_settings = [
                  [sg.Column(layout=all_settings, element_justification="center", justification="right", vertical_alignment="center", expand_y=False, background_color="red" if debug_colours else t.background_colour)]
                  ]

    advanced_settings = [
                  [sg.Column(layout=adv_settings, element_justification="center", justification="right", vertical_alignment="center", expand_y=False, background_color="red" if debug_colours else t.background_colour)]
                  ]

    side_panel = [
                    [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                    [sg.Frame(title="", layout=[[sg.Frame(title="", layout=main_settings, relief="ridge", border_width=7, pad=50)]], relief="groove", border_width=5, pad=((10, 20), 5))],
                    [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                    [sg.Frame(title="", layout=[[sg.Frame(title="", layout=advanced_settings, relief="ridge", border_width=7, pad=20)]], relief="groove", border_width=5, pad=((10, 20), 5))],
                    [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
                ]

    pillar_middle = [[
                    sg.Canvas(size=(5, None), expand_y=True, background_color="#0E1B25", pad=(1,3)),
                    sg.VerticalSeparator(color="black", pad=(3,13)),
                    sg.Stretch(background_color="#00345B"),
                    sg.VerticalSeparator(color="black", pad=(4,12)),
                    sg.Stretch(background_color="#00345B"),
                    sg.VerticalSeparator(color="black", pad=(3,14)),
                    sg.Canvas(size=(5, None), expand_y=True, background_color="#0E1B25", pad=(1,3))
                    ]]
    pillar = [
        [sg.Frame(title="", layout=[[sg.Canvas()]], element_justification="center", size=(90,25), pad=((0,0), (5,0)), relief="raised", border_width=2)],
        [sg.Frame(title="", layout=[[sg.Column(layout = pillar_middle, background_color="#00345B", expand_y=True, vertical_alignment="center")]], relief="sunken", pad=(10, 0), background_color="gray", expand_y=True, border_width=2)],
        [sg.Frame(title="", layout=[[sg.Canvas()]], element_justification="center", size=(90,25), pad=((0,0), (0,5)), relief="raised", border_width=2)]
    ]

    outer_side = [
        [sg.Canvas(size=(1,1), background_color = "orange" if debug_colours else  t.background_colour, key="settings_height_bar"),
        sg.Column(layout=pillar, expand_y=True, background_color="orange" if debug_colours else t.background_colour, element_justification="center", pad=((10,10),(0,0))),
        sg.Column(side_panel, key="side", element_justification="center", vertical_alignment="center",
                        background_color="dark blue" if debug_colours else t.background_colour, pad=0, expand_x=False, expand_y=True)]
    ]

    outer_grid = [
            [sg.Column(layout=grid_panel, key="grid_panel", background_color="magenta" if debug_colours else t.background_colour,
                  pad=(5,5), justification="center", element_justification='center', vertical_alignment='center', expand_x=True, expand_y=True, visible=True)],
            [(setup_text("\n - choose an image - \n", padding=0, key="gallery_text"))],
            [sg.Column(layout=button_yielder(), key="gallery", background_color="dark blue" if debug_colours else t.background_colour,
                  pad=(5,5), element_justification='center', vertical_alignment='center', expand_x=True, expand_y=True, visible=True)]
    ]

    layout = [[sg.Frame(title=" •• SCRAMBLE •• ", key="main_window",
                layout=[[
                        sg.Column(layout=outer_grid, key="central",
                                    background_color="maroon" if debug_colours else t.background_colour, pad=((35,5),(5)),# , pad=(5,5),
                                    element_justification='center', vertical_alignment='center', expand_x=True, expand_y=True),
                        sg.pin(sg.Column(layout=outer_side, expand_y=True, background_color="yellow" if debug_colours else t.background_colour, key="true_side", justification="right", vertical_alignment="c", pad=0)
                        )]],
                font=("courier", 10, "bold"), relief="groove", pad=(5), border_width=5, expand_x=True, expand_y=True,
                background_color="green" if debug_colours else t.background_colour, element_justification="right")]
            ]

    window = sg.Window(' •• SCRAMBLE •• ', layout, keep_on_top=False, finalize=True, margins=(3,3), icon=scramble_icon,
                       no_titlebar=False, resizable=t.allow_resize, titlebar_background_color=t.background_colour, return_keyboard_events=True, # no_titlebar=not t.allow_resize
                       enable_window_config_events=True, element_justification="center", alpha_channel=0 if start_hidden else .8, transparent_color="#D0FF00")


    logger("main window init'd")
    last_held_xy = None
    if t.start_maximised:
        window.maximize()
        window.refresh()
        t.maximised_size = window.size
    else:
        window.set_size(size=(t.screen_x, t.screen_y))

    t.game_started = size_got = hide_grid = settings_saved = False

    while True:
        event, values = window.read(timeout=500)

        if hide_grid:
            move_to_gallery()
            window.refresh()
            hide_grid = False
            get_gallery_and_thumbnail_size()
            fade_in_out(fade_in=True)

        if g.start_screen and not size_got:
            size_got=True
            g.start_screen = False

            panel_size = window['grid_panel'].get_size()
            if panel_size[0] != 1:
                t.main_window = window["main_window"]
                t.central = window["central"]
                t.true_side = window["true_side"]
                window["settings_height_bar"].set_size((1, window.size[0]-5)) #< - forces the settings panel to be full height
                t.true_side.expand(expand_row=True, expand_y=True, expand_x=False)
                print(f"t.true_side.get_size(): {t.true_side.get_size()}")
                window.refresh()
                t.gallery = window["gallery"]
                t.grid_panel = window["grid_panel"]
                t.grid_box = window["grid"]
                hide_grid=True

                g.grid_panel_size = panel_size
                print(f"captured grid_panel size: {g.grid_panel_size}")
                get_panel_dimensions()

                highlight_gridsize_button()

        if event:
            if "Escape" in event or event == "exit":
                update_window_size_data()
                settings_saved = True
                fade_in_out(fade_in=False)
                window.close()
                return "Done"

            elif event.startswith("imgkey_"):
                selected_imgname = event.replace("imgkey_", "")
                move_to_grid(selected_imgname)

            elif event == "grid":
                x, y = values["grid"]

                row = int(x // g.cell_w)
                col = int(y // g.cell_h)

                if last_held_xy and (col, row) != last_held_xy:
                    update_clicked_square(last_held_xy[0], last_held_xy[1], click_off=True)

                last_held_xy = col, row

                update_clicked_square(col, row)
                update_clicks(newline=True)
                rotated_children = b.button_press(last_held_xy)
                rotate_children(rotated_children)
                check_if_completed()

            elif event.startswith("adv_"):
                if event == "adv_gridsize":
                    if window["gridsize_buttons"].visible:
                        window["gridsize_buttons"].update(visible=False)
                    else:
                        window["gridsize_buttons"].update(visible=True)

            elif event.startswith("gridsize_"):
                print(f"Event: gridsize_:  {event}")
                if set_gridsize(event):
                    if g.puzzle_img_filename and t.is_grid_screen:
                        set_during_buttons_enable(enable=False, include_scramble=False)
                        move_to_grid(g.puzzle_img_filename)

            elif event == "adv_rotations":
                set_rotations()

            elif event.startswith("set_"):
                if event == "set_gallery":
                    move_to_gallery()


                if event == "set_image":
                    window["set_gallery"].update(disabled = False)
                    new_img_name = change_image()
                    if new_img_name:
                        g.puzzle_img_filename = new_img_name
                        move_to_grid(new_img_name)

                if event == "set_scramble":
                    scramble_colours()
                    if not t.game_started:
                        set_during_buttons_enable(enable=True)

                elif event == "set_perfect":
                    set_solved()
                    set_during_buttons_enable(enable=False, include_scramble=False)

            elif event == "get_hint":
                show_incorrect()

            elif event == "__WINDOW CONFIG__" and size_got and window.size != t.window_size:
                if not t.allow_resize:
                    if not window.maximized or window.size != t.maximised_size:
                        window.maximize()
                        t.window_size = window.size
                        update_window_size_data()
                else:
                    t.window_size = window.size
                    get_panel_dimensions()
                    if window.size == t.maximised_size:
                        t.start_maximised = True
                        update_window_size(do_maximise=True)
                    else:
                        t.start_maximised = False
                        update_window_size()
                    update_window_size_data()

                    settings_saved = True

        if window.is_closed():
            if not settings_saved:
                t.save_settings()
            return "Done"

def main():

    outcome = None
    while True:
        start_hidden=True
        while True:
            outcome = main_window(start_hidden=start_hidden)
            start_hidden=False
            if outcome:
                break
        if outcome and outcome == "Done":
            exit()

if __name__ == "__main__":
    main()
