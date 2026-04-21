
import FreeSimpleGUI as sg

def col_print(string):
    print_col_prints = False
    if print_col_prints:
        print(string)

class theme_data():

    def __init__(self):
        pass

    theme_dict:dict = {
        "arcade": {'BACKGROUND': "#38354a",#31374e",
                    'TEXT': "#de4507",
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

    screen_x = 480
    screen_y = 640
    maximise_window=True
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

t = theme_data()

#sg.main_global_pysimplegui_settings()
def get_col_from_col_code(red, green, blue):
    """col_code is a tuple from pixel_dict, returns a "#FFFFFFF" style value."""
    return '#%02x%02x%02x' % (red, green, blue)

class buttonClass:

    def __init__(self):
        self.coord_to_colour:dict = {} # just a 'grid coordinate to current colour' shortcut.
        self.coord_to_pixel:dict = {}
        #self.pixel_to_coord:dict = {}
        #self.str_to_tuple:dict = {}
        self.row_dict:dict = {}
        self.row_column_dict:dict = {}
        self.buttons:set = set()
        self.by_coord:dict[tuple: self.buttonInstance] = {}
        #self.prepared_children:dict = {}
        self.clean_dict:dict = {} # for the post-converted '36,36' > '0,0' / '121,36' > '1, 0'
        """ self.clean_dict[coord] = {"pixel_coords": pix_coord, "children": {"top": (1,0)}, "target_colour": get_col_from_col_code(img_data.pixel_dict[(x_val, y_val)])} """


    def img_from_coords(button, row, column):
        """row_{row}_col_{column}.png"""

        if button and isinstance(button, buttonClass.buttonInstance):
            row, column = button.coords
        elif button and isinstance(button, tuple):
            row, column = button
        elif button and isinstance(button, str):
            row, column = eval(button)

        if row and column:
            img_filename = f"row_{row}_col_{column}.png"
            return img_filename
        else:
            print(f"No row/column found from `button` : {button} / `row` : {row} / `column` : {column}")
    def colour_from_coords(self, coords, is_base=False, img_data=None):

        if isinstance(coords, str):
            print(f"COORDS GIVEN AS STRING: {coords}")
            return

        if self.by_coord.get(coords):
            if not is_base:
                return self.by_coord[coords].current_colour
            else:
                return self.by_coord[coords].target_colour

        #elif self.clean_dict.get(coords) and self.clean_dict[coords].get("target_colour"):
            #return self.clean_dict[coords]["target_colour"]

        else:
            print(f"Failed to get colour from {coords}, type: {type(coords)}")

    class buttonInstance:

        def __init__(self, coords):
            if isinstance(coords, str):
                print("COORDS GIVEN AS A STRING")
                return#coords = b.pixel_to_coord[coords]
            self.target_image = b.clean_dict[coords]["target_image"]
            self.coords = coords
            self.str_coords = str(coords)
            self.current_image = self.target_image

        def __repr__(self):
            return f"self.coords: {self.coords}  self.current_image: {self.current_image}  self.target_image: {self.target_image}"

        def change_image(self, new_image):
            self.current_image = new_image
            pass

    def button_press(self, coord:buttonInstance, base_pos, img_data):

        print(f"BUTTON PRESS: {coord}")
        rotated_children = {}
        if isinstance(coord, str) or isinstance(coord, tuple):
            if isinstance(coord, str):
                coord = eval(coord)
            children = b.clean_dict[coord]["children"]
        else:
            children = coord.children
        reordered = base_pos.reindex_children(children)
        for child in children:
            orig_index = list(children).index(child)
            new_index = list(reordered).index(child)
            rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], b.by_coord[str(children[list(children)[new_index]])].current_image)#), img_data))

        return rotated_children

    """

OKAY. So I need to add row/col coordinates to the 'left/top/right', instead of hardcoding the pixel values. That's just a holdover.
So, setup stage for buttons:
- add button instances.
- assign those button instances their children, by position, not by instance. So, 'top' for (2, 2) is (2, 1)
- Then for rotating children, we take the (current) top's colour and apply it to (current) right. We already store the original(target) colour on the instance so that works fine.
"""

    def set_up_buttons(self, base_pos, img_data):
        #from rotate_01 import base_positions, image_data
        base_pos
        img_data
        """   ! button_key_dict == self.row_dict
        self.row_dict: {0: ['(36, 36)', '(121, 36)', '(206, 36)', '(291, 36)', '(376, 36)'], 1: ['(36, 121)', '(121, 121)', '(206, 121)', '(291, 121)', '(376, 121)'], 2: ['(36, 206)', '(121, 206)', '(206, 206)', '(291, 206)', '(376, 206)'], 3: ['(36, 291)', '(121, 291)', '(206, 291)', '(291, 291)', '(376, 291)'], 4: ['(36, 376)', '(121, 376)', '(206, 376)', '(291, 376)', '(376, 376)']}"""

        def get_children():

            cleaned_children = {}
            for entry in self.clean_dict:
                cleaned_children[entry] = {}
                for position, coord in self.clean_dict[entry]["children"].items():
                    cleaned_children[entry][position] = coord

            for entry in self.clean_dict:
                self.clean_dict[entry]["children"] = cleaned_children[entry]

        def make_row_column_dict():

            if not img_data.new_img_data:
                print(f"No new_img_data: {img_data.new_img_data}")
                return
            if img_data.new_img_data:
                print("new_img_data found")

                base_file, coord_to_img_files, coords_list, image_size = img_data.new_img_data
                img_data.base_file = base_file
                img_data.coords_list = coords_list
                img_data.coord_to_img_files = coord_to_img_files

                #self.filename_to_coords = {}
                #self.coords_to_filename = {}
                for row_no in coord_to_img_files:
                    self.row_column_dict[row_no] = dict()
                    for col_no in coord_to_img_files[row_no]:
                        filename = coord_to_img_files[row_no][col_no]
                        self.row_column_dict[row_no][col_no] = filename
                        #self.filename_to_coords[filename] = (row_no, col_no)
                        #self.coords_to_filename[row_no, col_no] = (filename)
                        #b.str_to_tuple[f"{row_no, col_no}"] = (row_no, col_no)
                    #for col_no, y_val in base_pos.coord_dict["columns"].items():#coord dict: {'rows': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}, 'columns': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}}
                        """
                        coord = (x_val, y_val)
                        pix_coord = f"{(x_val, y_val)}"
                        self.pixel_to_coord[pix_coord] = coord
                        self.coord_to_pixel[coord] = pix_coord"""
                        #print(f"img_data.pixel_dict[(x_val, y_val) for pix_coord: {pix_coord} (cord: {coord}): {img_data.pixel_dict[(x_val, y_val)]}")
                        #print(f"Base positions ordered children: {base_pos.ordered_children}")
                        coord = row_no, col_no
                        self.clean_dict[coord] = {"children": base_pos.ordered_children[(row_no, col_no)], "target_image": filename}

                #print(f"\n\nclean dict: \n\n{self.clean_dict}\n\n")

            """for row_no, x_val in base_pos.coord_dict["rows"].items():
                self.row_column_dict[x_val] = list()
                for col_no, y_val in base_pos.coord_dict["columns"].items():#coord dict: {'rows': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}, 'columns': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}}
                    self.row_column_dict[x_val].append(y_val)
                    coord = (x_val, y_val)
                    pix_coord = f"{(x_val, y_val)}"
                    self.pixel_to_coord[pix_coord] = coord
                    self.coord_to_pixel[coord] = pix_coord
                    #print(f"img_data.pixel_dict[(x_val, y_val) for pix_coord: {pix_coord} (cord: {coord}): {img_data.pixel_dict[(x_val, y_val)]}")
                    colour = img_data.pixel_dict[coord]
                    self.clean_dict[coord] = {"pixel_coords": pix_coord, "children": base_pos.ordered_children[(x_val, y_val)], "target_colour": colour}
                    self.coord_to_colour[coord] = colour
            print(f"\n\nclean dict: \n\n{self.clean_dict}\n\n")"""

        make_row_column_dict()
        get_children()

b = buttonClass()

def splash_window(img_data):
    """Using the splash screen to get the size of the maximised window"""

    splashscreen_panel = [
        [sg.Canvas(size=(500,2), pad=2)],
        [sg.Text(text="\n ***••.  SCRAMBLE  .••*** \n", expand_x=True, expand_y=True, text_color=theme_data().theme_dict[sg.theme()]["gold_text"], justification="center")]
        ]

    splashscreen_main = [
        [sg.Column(splashscreen_panel)]]

    splashscreen_layout = [
        [sg.Frame(title="", key="splashscreen_window", layout=splashscreen_main, font=("courier", 10, "bold"), relief="groove", pad=(5), border_width=5)]]

    splashscreen_window = sg.Window(' •• SCRAMBLE ••', splashscreen_layout, keep_on_top=True, finalize=True, margins=(10,10), no_titlebar=True, auto_close=True, auto_close_duration=1.5)

    sample_layout = [[sg.Canvas(expand_x=True, expand_y=True, visible=False, key="sample_canvas")]]
    sample_window = sg.Window('', sample_layout, keep_on_top=True, finalize=True, no_titlebar=False, auto_close=True, auto_close_duration=1.5, alpha_channel=0)

    while True:
        _, _ = sample_window.read(timeout=100)
        event, _ = splashscreen_window.read(timeout=100)
        if splashscreen_window.get_screen_dimensions() and splashscreen_window.get_screen_dimensions() != (None, None):   #fullscreen version"""
            t.screen_x, t.screen_y = splashscreen_window.get_screen_dimensions()
            sample_window.close()

        if splashscreen_window.is_closed():
            if not sample_window.is_closed():
                sample_window.close()
            break


def main_window(img_data, base_pos):
    from rotate_01 import base_pos, base_positions, img_data, image_data
    base_pos:base_positions
    img_data:image_data
    sg.theme(t.theme_name)

    gallery_list = ["testing/lex.png", "rave_shaman.png"]

    t.difficulty = img_data.difficulty

    font_size = 14

    show_stretchers = None#"yellow"
    debug_colours = False#True

    std_background_1 = "gray"
    std_background_2 = "#38354a"

    def change_image():
        file_selected = sg.popup_get_file(message="Select a .png file to use as the base image", title="Select a .PNG file", file_types=(("PNG Files", "*.png"),))
        if file_selected:
            return file_selected

    def update_clicks(reset=False):
        if reset and reset == "clicks":
            t.clicks = 0
            text = f"Clicks: {t.clicks}"
        elif not reset:
            t.clicks += 1
            text = f"Clicks: {t.clicks}"
        else:
            t.clicks = 0
            text = reset
        window["click_counter"].update(f"\n{text}")

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
            update_clicks(reset = f"\nCompleted with {t.clicks} clicks!\nScramble to play again.")


    def set_difficulty():
        t.difficulty += 1
        if t.difficulty >= 3:
            t.difficulty = 0
        window["set_difficulty"].update(f"Difficulty:\n{t.difficulty_legend[t.difficulty]}")
        update_clicks(f"Difficulty set to {t.difficulty}")


    def show_incorrect(fix_incorrect=False):
        incorrect_buttons = check_if_completed(record_incomplete=True)
        """incorrect_buttons == list of buttonInstances"""

        if not incorrect_buttons:
            print("No incorrect buttons to highlight.")
            return

        saved_colours = {}
        from time import sleep
        for button in incorrect_buttons:
            button:buttonClass.buttonInstance
            saved_colours[button] = button.current_image
            x, y = button.coords
            if not g.white_square:
                from img_manipulation import make_square
                g.white_square = make_square(g.cell_w, "white", g.padding)

            button_box = coord_dict[x][y]
            g.grid.draw_image(filename=g.white_square, location = (button_box[0][0]+(g.padding/2)+2, button_box[0][1]+(g.padding/2)+2))
            unpressed_button(button_box[0], button_box[1])
            #update_clicked_square(x, y, g.white_square, click_off=True)
            #window[str(button.coords)].update(button_color=("black", "white"))
            window.refresh()
            sleep(.05)

        #print(f"Saved colours: {saved_colours}")
        #window["button_grid"].update()
        window.refresh()
        sleep(.5)

        for button in incorrect_buttons:
            if fix_incorrect:
                new_image = button.target_image
            else:
                new_image = saved_colours[button]
            button:buttonClass.buttonInstance
            x, y = button.coords
            update_clicked_square(x, y, new_image, click_off=True)
            #window[str(button.coords)].update(button_color=("black", saved_colours[button]))
            window.refresh()
            sleep(.03)
        window.refresh()

            #restore_colour =
    def set_solved(img_data):
        show_incorrect(fix_incorrect=True)


    def rotate_children(rotated_children, update=False):

        for _, child_coords in rotated_children.items():
            child_coords, child_image = child_coords
            #print(f"[rotate_children]  child_coords: {child_coords} / child_colour: {child_image}")
            #pixel_value = img_data.pixel_dict[child_coords]
            #if img_data.pixel_dict[child_coords] == child_colour:
                #a, b, c = child_colour
                #child_colour = tuple((a+45, b+45, c+45))
            #if update:
                #window[str(child_coords)].update(image_source = child_colour)#get_col_from_col_code(child_colour)))
            b.by_coord[f"{child_coords}"].change_image(child_image)
            #print(f"b.by_coord[f'{child_coords}']: {b.by_coord[f'{child_coords}']}")
            row, column = child_coords
            update_clicked_square(row, column, child_image, click_off=True)

    def scramble_colours():

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

        number_of_clicks = random.randint(1,3)
        buttons_to_click = random.choices(population=list(b.by_coord), k=int(len(b.by_coord)/2))
        for button in buttons_to_click:
            rotated_children = b.button_press(button, base_pos, img_data)
            if number_of_clicks > 1:
                for _ in range(number_of_clicks-1):
                    rotate_children(rotated_children, update=False)
                    sleep(.02)
                    window.refresh()
                    #col_print(f"Children to rotate: {rotated_children}")
                    #update_clicked_square(row, column, click_off=False)
            rotate_children(rotated_children)
        t.clicks = 0


### GRID POINTS

    if not img_data.start_screen:

        def make_button(coord):
            button_inst = b.buttonInstance(coord)
            b.buttons.add(button_inst)
            b.by_coord[f"{coord}"] = button_inst

    #theme.background_colour = img_data.background_colour

############################ new img/grid setup ###################################
    class gridClass:

        def __init__(self, region_size, grid_size):

            #self.new_grid = True
            self.region_size = 600,600
            self.width, self.height = region_size
            self.grid_size = grid_size
            self.rows = grid_size
            self.cols = grid_size # separate in case I do rectangles later.
            self.cell_w = self.width / self.cols
            self.cell_h = self.height / self.rows

            self.padding = 6

            self.grid:sg.Graph = None
            self.full_img = None
            self.coord_to_img_files:dict = {}
            self.coords_list = []

            self.white_square:str = None # to use for flashing hints

        def new_image(self, full_img, coord_to_img_files=None, coords_list=None, size=None):#(g.width, g.height)):
            """To make sure these are properly reset when the image is selected/changed"""
            if not size:
                size = (self.width, self.height)

            self.width, self.height = size

            if img_data.grid_size:
                self.cols = self.rows = img_data.grid_size

            self.cell_w = self.width / self.cols
            self.cell_h = self.height / self.rows

            if self.width == self.height:
                self.cell_w, self.cell_h = int(self.cell_w), int(self.cell_w)

            self.full_img = full_img

            if not coord_to_img_files or not coords_list:
                print("No coord_to_img_files or not coords_list")
                return

            self.full_img, self.coord_to_img_files, self.coords_list, (self.width, self.height) = full_img, coord_to_img_files, coords_list, size

            from rotate_01 import generate_children
            self.child_dict = generate_children(self.coords_list)
            base_pos.child_dict = self.child_dict
            from rotate_01 import base_positions, image_data
            b.set_up_buttons(base_pos, img_data)


    g = gridClass(region_size=img_data.region_size, grid_size=img_data.grid_size)

    def set_up_grid(img_file, img_size):

        padding = 5
        if padding % 2 != 0:
            padding += 1
        g.padding=int(padding)

        g.new_image(img_file, size=img_size)

        grid = sg.Graph(
            canvas_size=(g.width, g.height),
            graph_bottom_left=(0, g.height),
            graph_top_right=(g.width, 0),
            enable_events=True,
            key="grid", pad=16,
        )

        g.grid=grid

        g.full_img, g.coord_to_img_files, g.coords_list, (g.width, g.height) = img_data.new_img_data

        g.new_image(g.full_img, g.coord_to_img_files, g.coords_list, (g.width, g.height)) # just run it again in case anything was resized here? Need to cull so much of this.
        return grid

    def unpressed_button(top_left, bottom_right):
        g.grid.draw_rectangle(top_left=top_left, bottom_right=bottom_right, line_color="black", line_width=2)
        g.grid.draw_rectangle(top_left=(top_left[0]+1, top_left[1]+1), bottom_right=(bottom_right[0]-1, bottom_right[1]-1), line_color="white", line_width=1)


    def initial_grid_drawing():

        if not g.grid:
            g.grid = set_up_grid(g.full_img, g.region_size)
        coord_dict = {}
        g.grid.draw_image(filename=g.full_img, location=(0, 0))

        add_button_gap = True

        for row in range(0, int(g.width/g.cell_w)):
            coord_dict[row] = {}
            for column in range(0, int(g.height/g.cell_h)):
                if add_button_gap:
                    top_left = g.cell_w*column + (g.padding/2), g.cell_h*row + (g.padding/2)
                    bottom_right = g.cell_w*(column+1) - (g.padding/2), g.cell_h * (row+1) - (g.padding/2)
                #print(f"i in range: {column} // j in range: {column}")
                else:
                    top_left = g.cell_w*column, g.cell_h*row
                    bottom_right = g.cell_w*(column+1), g.cell_h * (row+1)
                button_box = top_left, bottom_right
                coord_dict[row][column] = button_box
                make_button((row, column))
            #print(f"top left: {top_left} // bottom right: {bottom_right}")
                unpressed_button(top_left, bottom_right)
        return coord_dict


    def update_clicked_square(row, column, new_image=None, click_off=False):
        #print("COORD DICT: {coord_dict}")
        #print(f"coord_to_img_files DICT:\n\n{g.coord_to_img_files}\n\n")
        if row > g.grid_size -1 or column > g.grid_size-1:
            #print(f"Clicked a grid reference that shouldn't exist: {row},{column}. The grid size is {g.grid_size}")
            return
        button_box = coord_dict[row][column]
        #print(f"ROW: {row} COLUMN: {column} // button box: {button_box}")
        if not new_image:
            if not hasattr(img_data, "coord_to_img_files") or not img_data.coord_to_img_files:
                filename = g.coord_to_img_files[row][column]
            else:
                filename = img_data.coord_to_img_files[row][column]
        else:
            filename = new_image
        # so we make the filename the grid ref image, and it should work, I think.
        #print(f"FILENAME FOR CLICKED SQUARE [{row}][{column}]: {filename}")
        #g.grid.draw_image(filename=filename, location = button_box[0])##(button_box[0][0]+2, button_box[0][1]+2))
        #g.grid.draw_image(filename=filename, location = (button_box[0][0]+(g.padding/2)+1, button_box[0][1]+(g.padding/2)+1))

        #print(f"click_off: {click_off}")
        if click_off:
            g.grid.draw_image(filename=filename, location = (button_box[0][0]+(g.padding/2)+2, button_box[0][1]+(g.padding/2)+2))
            unpressed_button(button_box[0], button_box[1])
        else:
            g.grid.draw_rectangle(top_left=button_box[0], bottom_right=button_box[1], line_color="white", line_width=2)
        window["grid"].update()


    def set_buttons_enable(enable=True):

        window["set_scramble"].update(disabled = not enable)
        window["get_hint"].update(disabled = not enable)
        window["set_perfect"].update(disabled = not enable)
        window["set_gallery"].update(disabled = not enable)

###################################################################################


    #gallery_source = "manip_testing_2.png" # make a list/dict later and generate from that. this'll do for now.

    def setup_button(text, key=None, size=None, font="courier 12", start_disabled=False, colour=t.button_colour):
        if not key:
            if text:
                key = f"{text}_key"

        if size:
            return sg.Button(button_text=text, size=size, key=key, use_ttk_buttons=True, auto_size_button=True, font=font, disabled_button_color="gray", disabled=start_disabled, button_color=colour)

        return sg.Button(button_text=text, key=key, use_ttk_buttons=True, auto_size_button=True, font=font, disabled_button_color="gray", disabled=start_disabled)

    def setup_text(text, key=None, size=None, font="courier 16"):
        colour = "white"
        if not key:
            if text:
                key = f"{text}_key"
        if size:
            return sg.Text(text=text, key=key, size=size, justification="center", text_color=colour, font=font)
        else:
            return sg.Text(text=text, key=key, justification="center", text_color=colour, font=font)

    if img_data.start_screen:

        def button_yielder():
            #buttons = list((sg.Canvas(pad=0, background_color="yellow"), sg.Text("Click an image to use it as the base for the puzzle.")))
            buttons = list()
            buttons.append(sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour))
            add_buttons = list(sg.Button(button_text="", image_filename=i, image_source=i, image_subsample=2, key=f"imgkey_{i}", image_size=(200,200)) for i in gallery_list)
            for b in add_buttons:
                buttons.append(b)
            buttons.append(sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour))
            return buttons

        grid_panel = [
            #[sg.Canvas(size=(int(theme.screen_x*.66), 0), pad=0)],
            [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
            [(setup_text("\n - choose an image -\n"))],
            [sg.Canvas(size=(t.screen_x*.66, 20), background_color="black" if debug_colours else t.background_colour)],
            button_yielder(),
            #[sg.Canvas(size=(1, theme.screen_y), pad=0, background_color="yellow"), sg.Text("Click an image to use it as the base for the puzzle."),
                #button_yielder()],
                #(sg.Button(button_text=i, image_filename=i, image_source=i, image_subsample=2, key=f"imgkey_{i}") for i in gallery_list)],
                #sg.Button(button_text=gallery_source, image_filename=gallery_source, image_source=gallery_source, image_subsample=2, key="imgkey_manip_testing_2.png")],
                #sg.Image(source="manip_testing_2.png", subsample=2, key="imgkey_manip_testing_2.png")],
            [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
            ]

    else:
        grid_panel = [
            [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
            [sg.Canvas(size=(int(t.screen_x*.66), 0), pad=0)],
            [sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour),
                set_up_grid(img_data.new_img_data, img_data.new_img_data[3]),
                sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour)],
            [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
            ]


#### Side panel ###
    difficulty_text = "Easy: 4x4 grid\nStandard: 6x6 grid\nHard: 9x9 grid."

    all_settings = [
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [setup_button("\n - scramble - \n", key="set_scramble", start_disabled=True, colour=t.highlight_button_colour, font="Courier 16 bold")],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [sg.HorizontalSeparator()],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
        [setup_button(text=f"Custom image", key="set_image")],
        #[sg.Button(button_text=f"Custom image", key="set_image", use_ttk_buttons=True, button_color=t.button_colour)],
        [setup_button(text=f"Difficulty:\n{t.difficulty_legend[t.difficulty]}", key="set_difficulty")],
        [setup_button(text="Show incorrect", key="get_hint", start_disabled=True)],
        [setup_button(text="Start over", key="set_perfect", start_disabled=True)],
        [setup_button(text=f"Return to Gallery", key="set_gallery", start_disabled=True)],
        [setup_button(text="Exit", key="exit")],
        [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
    ]

    text_layout = [
                [setup_text(text=f"\nWaiting to scramble...\n", key="click_counter")]#, size=(20,4))]
    ]

    side_layout = [
                  [sg.Column(layout=all_settings, element_justification="center", justification="right", vertical_alignment="center", expand_y=False, background_color="red" if debug_colours else t.background_colour)]
                  ]

    side_panel = [
                    [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                    [sg.Frame(title="", layout=[[sg.Frame(title="", layout=side_layout, relief="ridge", border_width=7, pad=50)]], relief="groove", border_width=5, pad=40)],
                  [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                  [sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour),
                    sg.Frame(title="", layout=text_layout, element_justification="center"),
                    sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                  [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)],
                  [sg.VStretch(background_color=show_stretchers if debug_colours else t.background_colour)]
                  ]

    inside_between = [[sg.Canvas(size=(5, None), expand_y=True, background_color="#0E1B25"),
                        sg.VerticalSeparator(color="black"),
                        sg.Stretch(background_color="#00345B"),
                        sg.VerticalSeparator(color="black"),
                        sg.Stretch(background_color="#00345B"),
                        sg.VerticalSeparator(color="black"),
                        sg.Canvas(size=(5, None), expand_y=True, background_color="#0E1B25")
                    ]]
    pillar = [
        [sg.Frame(title="", layout=[[sg.Canvas()]], element_justification="center", size=(140,25), pad=((0,0), (10,0)), relief="raised")],
        [sg.Frame(title="", layout=[[sg.Column(layout = inside_between, background_color="#00345B", expand_y=True, vertical_alignment="center")]], relief="sunken", pad=(10, 0), background_color="gray", expand_y=True, border_width=2)],
        [sg.Frame(title="", layout=[[sg.Canvas()]], element_justification="center", size=(140,25), pad=((0,0), (0,10)), relief="raised")]
    ]

    layout = [[sg.Frame(title="", key="main_window",
                            layout=[[
                                    sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour),
                                    sg.Column(layout=grid_panel, key="central",
                                                background_color="magenta" if debug_colours else t.background_colour, pad=(5,5), element_justification='center', vertical_alignment='center', expand_x=True, expand_y=True),
                                    sg.Stretch(background_color=show_stretchers if debug_colours else t.background_colour),
                                    sg.Column(layout=pillar, expand_y=True, background_color="orange" if debug_colours else t.background_colour, element_justification="center", pad=((20,0),(20,20))),#sg.VerticalSeparator(pad=5),
                                    sg.Column(side_panel, key="side", element_justification="right", vertical_alignment="center",
                                                background_color="dark blue" if debug_colours else t.background_colour, pad=((0,5),(5,5)), expand_x=False, expand_y=True)]],
                            font=("courier", 10, "bold"), relief="groove", pad=(5), border_width=5, expand_x=True, expand_y=True,
                            background_color="green" if debug_colours else t.background_colour, element_justification="right")]
                        ]

    window = sg.Window(' •• SCRAMBLE •• ', layout, keep_on_top=False, finalize=True, margins=(3,3), no_titlebar=False, resizable=True, size=(t.screen_x, t.screen_y), return_keyboard_events=True, enable_window_config_events=True, element_justification="center")

    last_held_xy = None
    if t.maximise_window:
        window.Maximize()
        t.maximised_size = tuple(window.size)

    start_screen_checked = False
    t.game_started = False
    while True:
        event, values = window.read(timeout=1000)
        """

DEFAULT_PIXELS_TO_CHARS_SCALING = (10,26)

The conversion simply takes your size[0] and multiplies by 10 and your size[1] and multiplies it by 26.

        """
        if img_data.start_screen:
            if event and event.startswith("imgkey_"):
                selected_imgname = event.replace("imgkey_", "")
                window["side"].set_size((100, None))
                region_size = window["central"].get_size()
                img_data.region_size = region_size
                g.full_img = selected_imgname
                g.region_size = region_size
                g.new_grid = True
                #img_data.new_img_data = new_image, coord_to_img_files, coord_list, image_size
                img_data.start_screen=False
                window.close()
                print(f"Returning `restart_{selected_imgname}`")
                return f"restart_{selected_imgname}"

        elif not start_screen_checked:

            g.region_size = g.width, g.height
            coord_dict = initial_grid_drawing()
            window["set_scramble"].update(disabled=False, button_color=t.highlight_button_colour)
            window["grid"].set_size(size=(g.width, g.height))
            #window["side"].set_size((200, None))
            window.refresh()
            start_screen_checked=True

        if event:
            if event == "grid":
                x, y = values["grid"]

                row = int(x // g.cell_w)
                col = int(y // g.cell_h)

                #print(f"last_held_xy: {last_held_xy} // current xy: {(col, row)}")
                if last_held_xy and (col, row) != last_held_xy:
                    update_clicked_square(last_held_xy[0], last_held_xy[1], click_off=True)

                last_held_xy = col, row

                update_clicked_square(col, row)
                update_clicks()
                #event = b.by_coord[event]
                #event = b.str_to_tuple[last_held_xy]
                rotated_children = b.button_press(last_held_xy, base_pos, img_data)
                #print(f"Children to rotate: {rotated_children}")
                rotate_children(rotated_children)
                #print(f"Button pressed: {last_held_xy}")
                check_if_completed()

            if "Escape" in event or event == "exit":
                window.close()
                return "Done"

            elif event.startswith("set_"):
                if event == "set_gallery":
                    window.close()
                    img_data.start_screen=True
                    return f"restart"

                if event == "set_image":
                    new_img_name = change_image()
                    if new_img_name:
                        print(f"new_img_name: {new_img_name}")
                        region_size = window["central"].get_size()
                        g.full_img = selected_imgname
                        g.region_size = region_size
                        g.new_grid = True
                        img_data.region_size = region_size
                        """from img_manipulation import generate_img_grid
                        print("Going to generate_img_grid from ln 722")
                        new_image, coord_to_img_files, coord_list, new_image_size = generate_img_grid(new_img_name, region_size)
                        img_data.new_img_data = new_image, coord_to_img_files, coord_list, image_size
                        img_data.region_size = new_image_size
"""
                        window.close()
                        img_data.start_screen=False
                        return f"restart_{new_img_name}"

                if event == "set_scramble":
                    scramble_colours()
                    if not t.game_started:
                        set_buttons_enable(enable=True)

                elif event == "set_difficulty":
                    set_difficulty()
                elif event == "set_perfect":
                    set_solved(img_data)
                elif event == "set_use_images_checkbox":
                    if hasattr(values, event):
                        img_data.use_images_not_colours = values.get(event)


            elif event == "get_hint":
                show_incorrect()


            elif event != "__TIMEOUT__":
                if event == "__WINDOW CONFIG__":
                    #print(f"original screen_x, original screen_y: {theme.screen_x}, {theme.screen_y}")
                    if window.size == t.maximised_size:
                        t.maximise_window = True
                    else:
                        t.maximise_window = False
                    new_screen_x, new_screen_y = window.size

                    if new_screen_x == t.screen_x and new_screen_y == t.screen_y:
                        continue
                    else:
                        reset = False
                        #print(f"new_screen_x, new_screen_y: {new_screen_x}, {new_screen_y}")
                        max_x = max(new_screen_x - t.screen_x, t.screen_x - new_screen_x)
                        #print(f"MAX X DIFF: {max_x}")
                        max_y = max(new_screen_y - t.screen_y, t.screen_y - new_screen_y)
                        #print(f"MAX Y DIFF: {max_y}")
                        if max_x > 100 or max_y > 100:
                            reset = True

                        if reset:
                            t.screen_x = new_screen_x
                            t.screen_y = new_screen_y
                            window.close()
                            break

        if window.is_closed():
            #print("window is closed.")
            return "Done"

if __name__ == "__main__":
    from rotate_01 import main
    main()
