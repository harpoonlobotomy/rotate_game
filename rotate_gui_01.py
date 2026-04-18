from ast import literal_eval
from re import M

import FreeSimpleGUI as sg
class theme_data():

    def __init__(self):
        pass

    theme_dict:dict = {
        "arcade": {'BACKGROUND': "#38354a",#31374e",
                    'TEXT': "#de4507",
                    'INPUT': "#45523F",
                    'TEXT_INPUT': "#f5db74",
                    'SCROLL': "#003e9b",
                    'BUTTON': ('black', "#ffda57"),##ffd657"),
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

theme = theme_data()

def get_col_from_col_code(col_code):
    """col_code is a tuple from pixel_dict, returns a "#FFFFFFF" style value."""
    print(f"COL CODE: {col_code}")
    if len(col_code) == 3:
        red, green, blue = col_code
    if len(col_code) == 4:
        red, green, blue, _ = col_code
    return '#%02x%02x%02x' % (red, green, blue)

class buttonClass:

    def __init__(self):
        self.coord_to_colour:dict = {} # just a 'grid coordinate to current colour' shortcut.
        self.coord_to_pixel:dict = {}
        self.pixel_to_coord:dict = {}
        self.row_dict:dict = {}
        self.row_column_dict:dict = {}
        self.buttons:set = set()
        self.by_coord:dict = {}
        self.prepared_children:dict = {}
        self.clean_dict:dict = {} # for the post-converted '36,36' > '0,0' / '121,36' > '1, 0'
        """ self.clean_dict[coord] = {"pixel_coords": pix_coord, "children": {"top": (1,0)}, "target_colour": get_col_from_col_code(img_data.pixel_dict[(x_val, y_val)])} """


    def colour_from_coords(self, coords, is_base=False):
        if self.by_coord.get(coords):
            if not is_base:
                return self.by_coord[coords].current_colour
            else:
                return self.by_coord[coords].target_colour
        else:
            return self.clean_dict[coords]["target_colour"]

    class buttonInstance:
        def __init__(self, coords):
            self.target_colour = b.coord_to_colour[coords]
            self.coords = str(coords)
            self.current_colour = self.target_colour

        def change_colour(self, new_colour):
            self.current_colour = new_colour
            pass

    def button_press(self, coord, base_pos, img_data):

        print("BUTTON PRESS")
        rotated_children = {}
        if not self.prepared_children.get(coord):
            children = b.clean_dict[coord]["children"]
            reordered = base_pos.reindex_children(children)
            #print(f"CHILDREN: {children} // REORDERED: {reordered}")
            for child in children:
                orig_index = list(children).index(child)
                new_index = list(reordered).index(child)
                rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], b.colour_from_coords(children[list(children)[new_index]]))


        else:
            children = self.prepared_children[coord]
            reordered = base_pos.reindex_children(children)
            for child in children:
                orig_index = list(children).index(child)
                new_index = list(reordered).index(child)
                rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], self.by_coord[coord].current_colour)

            self.prepared_children[coord] = rotated_children
        print(f"Rotated children: {rotated_children}")
        return rotated_children
        """

OKAY. So I need to add row/col coordinates to the 'left/top/right', instead of hardcoding the pixel values. That's just a holdover.
So, setup stage for buttons:
- add button instances.
- assign those button instances their children, by position, not by instance. So, 'top' for (2, 2) is (2, 1)
- Then for rotating children, we take the (current) top's colour and apply it to (current) right. We already store the original(target) colour on the instance so that works fine.
"""

    def set_up_buttons(self, base_pos, img_data):

        """   ! button_key_dict == self.row_dict
        self.row_dict: {0: ['(36, 36)', '(121, 36)', '(206, 36)', '(291, 36)', '(376, 36)'], 1: ['(36, 121)', '(121, 121)', '(206, 121)', '(291, 121)', '(376, 121)'], 2: ['(36, 206)', '(121, 206)', '(206, 206)', '(291, 206)', '(376, 206)'], 3: ['(36, 291)', '(121, 291)', '(206, 291)', '(291, 291)', '(376, 291)'], 4: ['(36, 376)', '(121, 376)', '(206, 376)', '(291, 376)', '(376, 376)']}"""

        def get_children():

            cleaned_children = {}
            for entry in self.clean_dict:
                cleaned_children[entry] = {}
                for position, pixel_coord in self.clean_dict[entry]["children"].items():
                    coord = self.pixel_to_coord[str(pixel_coord)]
                    cleaned_children[entry][position] = coord

            for entry in self.clean_dict:
                self.clean_dict[entry]["children"] = cleaned_children[entry]

        def make_row_column_dict():

            for row_no, x_val in base_pos.coord_dict["rows"].items():
                self.row_column_dict[row_no] = list()
                for col_no, y_val in base_pos.coord_dict["columns"].items():#coord dict: {'rows': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}, 'columns': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}}
                    self.row_column_dict[row_no].append(col_no)
                    coord = f"{(row_no, col_no)}"
                    pix_coord = f"{(x_val, y_val)}"
                    self.pixel_to_coord[pix_coord] = coord
                    self.coord_to_pixel[coord] = pix_coord
                    self.clean_dict[coord] = {"pixel_coords": pix_coord, "children": base_pos.ordered_children[(x_val, y_val)], "target_colour": get_col_from_col_code(img_data.pixel_dict[(x_val, y_val)])}
                    self.coord_to_colour[coord] = get_col_from_col_code(img_data.pixel_dict[(x_val, y_val)])

        make_row_column_dict()
        get_children()

b = buttonClass()

def splash_window(): #separate window so it can be left open during play if desired
    splashscreen_panel = [
        [sg.Canvas(size=(500,2), pad=2)],
        [sg.Text(text="\n***** UNNAMED ROTATE GAME *****\n", expand_x=True, expand_y=True, text_color=theme_data().theme_dict[sg.theme()]["gold_text"], justification="center")]
        ]

    splashscreen_main = [
        [sg.Column(splashscreen_panel)]]

    splashscreen_layout = [
        [sg.Frame(title="", key="splashscreen_window", layout=splashscreen_main, font=("courier", 10, "bold"), relief="groove", pad=(5), border_width=5)]]

    splashscreen_window = sg.Window(' ROTATE GAME ••', splashscreen_layout, keep_on_top=True, finalize=True, margins=(10,10), no_titlebar=True, auto_close=True, auto_close_duration=2.2)

    while True:
        event, _ = splashscreen_window.read(timeout=100)
        if splashscreen_window.get_screen_dimensions() and splashscreen_window.get_screen_dimensions() != (None, None):   #fullscreen version"""
            theme.screen_x, theme.screen_y = splashscreen_window.get_screen_dimensions()

        if event != "__TIMEOUT__":
            print(event)
        if splashscreen_window.is_closed():
            print("window is closed.")
            break


def main_window(img_data, base_pos):

    def change_image():
        file_selected = sg.popup_get_file(message="Select a .png file to use as the base image", title="Select a .PNG file", file_types=(("PNG Files", "*.png"),))
        if file_selected:
            return file_selected
            print(file_selected)
            print(img_data.base_image)
            img_data.base_image = file_selected
            print(img_data.base_image)

    def check_if_completed():
        not_complete = False
        for button in b.by_coord.values():
            if button.current_colour != button.target_colour:
                not_complete = True

        if not not_complete:
            print("All correct!")
            window["click_counter"].update(f"Completed with {theme.clicks} clicks!")
            theme.clicks = 0


    def update_clicks(reset=False):
        if reset:
            theme.clicks = 0
        else:
            theme.clicks += 1
        window["click_counter"].update(f"Clicks: {theme.clicks}")

    def set_difficulty():
        theme.difficulty += 1
        if theme.difficulty >= 3:
            theme.difficulty = 0
        window["set_difficulty"].update(f"Difficulty: {theme.difficulty_legend[theme.difficulty]}")

        update_clicks(reset=True)

    def set_solved():
        for button in b.by_coord:
            colour = b.colour_from_coords(button, is_base=True)
            window[button].update(button_color=("black", colour))
            b.by_coord[button].change_colour(colour)

        update_clicks(reset=True)

    def rotate_children(rotated_children, update=True):

        for _, child_coords in rotated_children.items():
            child_coords, child_colour = child_coords
            #print(f"child_coords: {child_coords} / child_colour: {child_colour}")
            #pixel_value = pixel_dict[child_coords]
            #if img_data.pixel_dict[child_coords] == child_colour:
                #a, b, c = child_colour
                #child_colour = tuple((a+45, b+45, c+45))
            if update:
                window[str(child_coords)].update(button_color=("black", child_colour))#get_col_from_col_code(child_colour)))
            b.by_coord[child_coords].change_colour(child_colour)

    def scramble_colours():

        points_to_rotate = {
            "0": 6,
            "1": 12,
            "2": 20
        }

        no_of_rotations = points_to_rotate[str(theme.difficulty)]

        import random

        buttons_to_click = random.choices(population=list(b.by_coord), k=no_of_rotations)
        for button in buttons_to_click:
            rotated_children = b.button_press(button, base_pos, img_data)
            number_of_clicks = random.randint(1,3)
            if number_of_clicks > 1:
                for _ in range(number_of_clicks-1):
                    rotate_children(rotated_children, update=False)
            rotate_children(rotated_children)
        update_clicks(reset=True)


### GRID POINTS

    button_size = (16, 8)
    font_size = 12

    def get_button_size():
        no_of_rows = len(base_pos.coord_dict["rows"])
        no_of_cols = len(base_pos.coord_dict["columns"])
        if no_of_rows != no_of_cols:
            if no_of_cols < no_of_rows:
                no_of_rows = no_of_cols ## just need whichever is smaller to use for button size. with this, no_of_rows is always smallest.

        max_y = theme.screen_y
        max_y = max_y*.8
        max_y_each = int((max_y/font_size)/no_of_rows)
        if max_y_each % 2 != 0:
            max_y_each += 1

        if max_y_each <= 6:
            max_y_each = 6
        button_size = (max_y_each-4, int(max_y_each/2)-2)#

        return button_size

    button_size = get_button_size()

    b.set_up_buttons(base_pos, img_data)

    def make_button(coord):

        button = sg.Button(button_text="", button_color=b.coord_to_colour[coord], font=f"courier {font_size}", size=button_size, key=str(coord), pad=15, border_width=3)
        button_inst = b.buttonInstance(str(coord))
        b.buttons.add(button_inst)
        b.by_coord[str(coord)] = button_inst

        return sg.Column(layout=[[button]], background_color=b.coord_to_colour[coord], key=f"{coord}_base", pad=0)


    button_dict = {}

    for column in b.row_column_dict:
        button_list = []
        for row in b.row_column_dict[column]:
            coord = f"{(row, column)}"
            button_list.append(make_button(coord))
        button_dict[column] = button_list


    """
    BUTTON DICT [ by row_number[coord]]:
        {0: ['(36, 36)', '(36, 121)', '(36, 206)', '(36, 291)', '(36, 376)'], 1: ['(121, 36)', '(121, 121)', '(121, 206)', '(121, 291)', '(121, 376)'], 2: ['(206, 36)', '(206, 121)', '(206, 206)', '(206, 291)', '(206, 376)'], 3: ['(291, 36)', '(291, 121)', '(291,
        206)', '(291, 291)', '(291, 376)'], 4: ['(376, 36)', '(376, 121)', '(376, 206)', '(376, 291)', '(376, 376)']}
    """

    grid_region = "maroon"

    grid = sg.Column(
            [button_list for button_list in button_dict.values()],
            pad=(0, 0),
            element_justification='center', background_color="blue", key="button_grid"
        )

    grid_panel = [
        [sg.Canvas(size=(int(theme.screen_x*.66), 0), pad=0)],
        [sg.VStretch(background_color=grid_region)],
        [sg.Canvas(size=(1, theme.screen_y), pad=0, background_color="yellow"), sg.Stretch(background_color=grid_region), grid, sg.Stretch(background_color=grid_region)],
        [sg.VStretch(background_color=grid_region)]
        ]


#### Side panel ###

    settings_panel = [
        [sg.Button(button_text=f"Set image", key="set_image")],
        [sg.Button(button_text=f"Difficulty: {theme.difficulty_legend[theme.difficulty]}", key="set_difficulty")]
        ]

    scramble_panel = [
        [sg.Button(button_text="Scramble", key="set_scramble")]
        ]

    reset_panel = [
        [sg.Button(button_text="Perfect Solve", key="set_perfect")]
        ]

    clicks_panel = [
        [sg.Text(text=f"Clicks: {theme.clicks}", key="click_counter")]
    ]

    exit_panel = [
        [sg.Button(button_text="Exit", key="exit")]
        ]

    side_panel = [[sg.Canvas(size=(int(theme.screen_x*.33), 0))],
                  [sg.Column(layout=settings_panel)], [sg.VStretch()],
                  [sg.Column(layout=scramble_panel)], [sg.VStretch()],
                  [sg.Column(layout=reset_panel)], [sg.VStretch()],
                  [sg.Column(layout=clicks_panel)], [sg.VStretch()],
                  [sg.Column(layout=exit_panel)]]

    layout = [[sg.Frame(title="~~ rotate game ~~", key="main_window",
                            layout=[[
                                    sg.Column(layout=grid_panel, key="central",
                                                background_color=grid_region, pad=(5,5), element_justification='center', justification="center", vertical_alignment='center', expand_x=True, expand_y=True),
                                    sg.Stretch(),
                                    sg.Column(side_panel, key="side", justification = "center", element_justification="center", vertical_alignment="center",
                                                background_color="dark blue", pad=(5,5))]],
                            font=("courier", 10, "bold"), relief="groove", pad=(5), border_width=5, expand_x=True, expand_y=True)]]

    window = sg.Window(' •• ROTATE •• ', layout, keep_on_top=False, finalize=True, margins=(3,3), no_titlebar=False, resizable=True, size=(theme.screen_x, theme.screen_y), return_keyboard_events=True, enable_window_config_events=True, element_justification="center")

    if theme.maximise_window:
        window.Maximize()
        theme.maximised_size = tuple(window.size)
    button_size = get_button_size()

    while True:
        event, _ = window.read(timeout=1000)
        if event and "Escape" in event or event == "exit":
            window.close()
            return "Done"

        if event.startswith("set_"):
            if event == "set_image":
                new_img_name = change_image()
                window.close()
                return f"restart_{new_img_name}"

            if event == "set_scramble":
                scramble_colours()
            elif event == "set_difficulty":
                set_difficulty()
                pass
            elif event == "set_perfect":
                set_solved()
                pass

        if event in b.by_coord:
            update_clicks()
            rotated_children = b.button_press(event, base_pos, img_data)
            rotate_children(rotated_children)
            print(f"Button pressed: {event}")
            check_if_completed()

        elif event != "__TIMEOUT__":
            print(f"EVENT: {event}")
            if event == "__WINDOW CONFIG__":
                #print(f"original screen_x, original screen_y: {theme.screen_x}, {theme.screen_y}")
                if window.size == theme.maximised_size:
                    theme.maximise_window = True
                else:
                    theme.maximise_window = False
                new_screen_x, new_screen_y = window.size

                if new_screen_x == theme.screen_x and new_screen_y == theme.screen_y:
                    continue
                else:
                    reset = False
                    #print(f"new_screen_x, new_screen_y: {new_screen_x}, {new_screen_y}")
                    max_x = max(new_screen_x - theme.screen_x, theme.screen_x - new_screen_x)
                    #print(f"MAX X DIFF: {max_x}")
                    max_y = max(new_screen_y - theme.screen_y, theme.screen_y - new_screen_y)
                    #print(f"MAX Y DIFF: {max_y}")
                    if max_x > 100 or max_y > 100:
                        reset = True

                    if reset:
                        theme.screen_x = new_screen_x
                        theme.screen_y = new_screen_y
                        button_size = get_button_size()
                        #window["central"].update(size=(int(theme.screen_x*.66), int(theme.screen_y*.95)))
                        #window["side"].update(size=(int(theme.screen_x*.33), int(theme.screen_y*.95)))
                        window.close()
                        break

        if window.is_closed():
            #print("window is closed.")
            return "Done"

if __name__ == "__main__":
    from rotate_01 import main
    main()
