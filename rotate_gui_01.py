from ast import literal_eval

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

theme = theme_data()

def get_col_from_col_code(col_code):
    """col_code is a tuple from pixel_dict, returns a "#FFFFFFF" style value."""
    red, green, blue = col_code
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
            print(f"Children: {children}")
            reordered = base_pos.reindex_children(children)
            #print(f"CHILDREN: {children} // REORDERED: {reordered}")
            for child in children:
                orig_index = list(children).index(child)
                new_index = list(reordered).index(child)
                print(f"list(children)[new_index]: {list(children)[new_index]}")
                print(f"children[list(children)[new_index]: {children[list(children)[new_index]]}")
                rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], b.colour_from_coords(children[list(children)[new_index]]))

            #self.prepared_children[str(coord)] = rotated_children
            print(f"coord: {str(coord)}")
            #print(f"self.prepared_children[coord]: {self.prepared_children[coord]}")

        else:
            children = self.prepared_children[coord]
            print(f"CHildren from prepared_children: {children}")
            reordered = base_pos.reindex_children(children)
            for child in children:
                orig_index = list(children).index(child)
                new_index = list(reordered).index(child)
                print(f"list(children)[new_index]: {list(children)[new_index]}")
                rotated_children[list(children)[new_index]] = (children[list(children)[orig_index]], self.by_coord[coord].current_colour)
                print(f"rotated_children[list(children)[new_index]: {rotated_children[list(children)[new_index]]}")

            self.prepared_children[coord] = rotated_children

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
            self.coord_list = []
            #print(f"ORDERED CHILDREN: {base_pos.ordered_children}")

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
        #print(f"SELF.CLEAN_DICT: {self.clean_dict}")

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

    #coord_dict == ["rows"] / ["columns"]
    #colours = ['Black2', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue18', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 'DarkGrey15', 'DarkGrey16', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeonBlue1', 'NeonGreen1', 'NeonYellow1', 'NeutralBlue', 'Purple']
    #colours = ["Blue", "Brown", "Grey", "Green", "Purple", "Red", "Teal", "Yellow", "Black"]
    print(f"coord dict: {base_pos.coord_dict}")

    def rotate_children(rotated_children):

        for _, child_coords in rotated_children.items():
            child_coords, child_colour = child_coords
            #print(f"child_coords: {child_coords} / child_colour: {child_colour}")
            #pixel_value = pixel_dict[child_coords]
            #if img_data.pixel_dict[child_coords] == child_colour:
                #a, b, c = child_colour
                #child_colour = tuple((a+45, b+45, c+45))
            print(f"Child colour: {child_colour}")
            window[str(child_coords)].update(button_color=("black", child_colour))#get_col_from_col_code(child_colour)))
            b.by_coord[child_coords].change_colour(child_colour)
            print(window[str(child_coords)].ButtonColor)
### GRID POINTS

    """def make_all_buttons():
        radios = []

        radios.append(list(sg.Button(button_text="", button_color=get_col_from_col_code(val), font="courier 12", size=(8,4), key=str(i)) for i, val in pixel_dict.items()))

        #radios.append(list(sg.Radio(text="", group_id="01", circle_color=get_col_from_col_code(val), font="arial 6", key=str(i)) for i, val in pixel_dict.items()))
        #radio_inner = [sg.Text(""), sg.Radio(text="", group_id="01", circle_color="yellow", font="arial 6")]
        #radio = [radio_inner, val for i, val in pixel_dict.items()]
        print(f"RADIOS: {radios}")
        return radios

    sg.Column(layout=make_all_buttons())"""

    #grid_panel = [[sg.Column(layout=make_all_buttons())]]#sg.Multiline(default_text = sg.list_of_look_and_feel_values(), size=(int((theme.screen_x*.66)/8), 20))]]

    button_size = (16, 8)

    font_size = 12

    def get_button_size():
        no_of_rows = len(base_pos.coord_dict["rows"])
        no_of_cols = len(base_pos.coord_dict["columns"])
        if no_of_rows != no_of_cols:
            if no_of_cols < no_of_rows:
                no_of_rows = no_of_cols ## just need whichever is smaller to use for button size. with this, no_of_rows is always smallest.

        #if theme.maximise_window:
            #max_x, max_y = theme.maximised_size
        #else:
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
            #button_list.append(sg.Button(button_text="", button_color=get_col_from_col_code(pixel_dict[coord]), font=f"courier {font_size}", size=button_size, key=str(coord), pad=7))
            button_list.append(make_button(coord))

            #button_dict[col_no][row_no] =
        button_dict[column] = button_list
        #button_key_dict[row] = list(i.key.replace("_base", "") for i in button_list)
    #print(f"BUTTON KEY DICT: {button_key_dict}")
    #print(f"\nBUTTON DICT [ by row_number[coord]]:\n{button_key_dict}\n\n")

    #b.row_dict = button_key_dict



    """
    BUTTON DICT [ by row_number[coord]]:
        {0: ['(36, 36)', '(36, 121)', '(36, 206)', '(36, 291)', '(36, 376)'], 1: ['(121, 36)', '(121, 121)', '(121, 206)', '(121, 291)', '(121, 376)'], 2: ['(206, 36)', '(206, 121)', '(206, 206)', '(206, 291)', '(206, 376)'], 3: ['(291, 36)', '(291, 121)', '(291,
        206)', '(291, 291)', '(291, 376)'], 4: ['(376, 36)', '(376, 121)', '(376, 206)', '(376, 291)', '(376, 376)']}
    """

    grid_region = "maroon"

    #grid = sg.Column(button_list for button_list in button_dict.values())
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
    side_panel_size = (5,5)#((int(theme.screen_x*.33)-55), int((theme.screen_y*.33)-35))
    side_panel_col = "pink"
    #temp_side_panel = [[sg.Canvas(size=((int(theme.screen_x*.33)-55), int((theme.screen_y*.33)-35)))]]
    #temp_side_panel_2 = [[sg.Stretch(), sg.Canvas(size=((int(theme.screen_x*.33)-55), int((theme.screen_y*.33)-35))), sg.Stretch()]]
    #temp_side_panel_3 = [[sg.Canvas(size=((int(theme.screen_x*.33)-55), int((theme.screen_y*.33)-35)))]]
    temp_side_panel = [[sg.Canvas(expand_x=False, expand_y=True, background_color=side_panel_col, size=side_panel_size)]]
    temp_side_panel_2 = [[sg.Canvas(expand_x=False, expand_y=True, size=side_panel_size, background_color=side_panel_col)]]
    temp_side_panel_3 = [[sg.Canvas(expand_x=False, expand_y=True, size=side_panel_size, background_color=side_panel_col)]]
    side_panel = [[sg.Canvas(size=(int(theme.screen_x*.33), 0))], [sg.Column(layout=temp_side_panel)], [sg.VStretch()], [sg.Column(layout=temp_side_panel_2)], [sg.VStretch()], [sg.Column(layout=temp_side_panel_3)]]

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
        if event and "Escape" in event:
            return "Done"

        if event in b.by_coord:
            rotated_children = b.button_press(event, base_pos, img_data)
            rotate_children(rotated_children)
            print(f"Button pressed: {event}")

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
