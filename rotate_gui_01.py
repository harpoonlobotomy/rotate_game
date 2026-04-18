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

class buttonClass():

    def __init__(self):
        self.row_dict:dict = {}
        self.row_column_dict:dict = {}

    def make_row_col_dict(self):
        self.coord_list = []
        for row, _ in self.row_dict.items():
            self.row_column_dict[row] = {}
            for column, entry in enumerate(self.row_dict[row]):
                #print(f"ROW: {row} // column : {column} // entry: {entry}")
                self.row_column_dict[row][column] = entry
                self.coord_list.append(entry)

        print(self.row_column_dict)

buttons = buttonClass()

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

def main_window(pixel_dict, coord_dict):
    #coord_dict == ["rows"] / ["columns"]
    #colours = ['Black2', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue18', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 'DarkGrey15', 'DarkGrey16', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeonBlue1', 'NeonGreen1', 'NeonYellow1', 'NeutralBlue', 'Purple']
    #colours = ["Blue", "Brown", "Grey", "Green", "Purple", "Red", "Teal", "Yellow", "Black"]
    print(f"coord dict: {coord_dict}")
    def get_col_from_col_code(col_code):
        """col_code is a tuple from pixel_dict, returns a "#FFFFFFF" style value."""
        red, green, blue = col_code
        return '#%02x%02x%02x' % (red, green, blue)

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

    button_dict = {}
    button_key_dict = {}
    button_size = (16, 8)

    font_size = 12

    def get_button_size():
        no_of_rows = len(coord_dict["rows"])
        no_of_cols = len(coord_dict["columns"])
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

        if max_y_each == 2:
            max_y_each = 4
        print(f"Max y each: {max_y_each}")
        button_size = (max_y_each-2, int(max_y_each/2)-1)#

        return button_size

    button_size = get_button_size()

    for row_no, x_val in coord_dict["rows"].items():#coord dict: {'rows': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}, 'columns': {0: 36, 1: 121, 2: 206, 3: 291, 4: 376}}
        button_list = []
        for col_no, y_val in coord_dict["columns"].items():
            coord = (x_val, y_val)
            button_list.append(sg.Button(button_text="", button_color=get_col_from_col_code(pixel_dict[coord]), font=f"courier {font_size}", size=button_size, key=str(coord), pad=7))
        button_dict[row_no] = button_list
        button_key_dict[row_no] = list(i.key for i in button_list)

    #print(f"\nBUTTON DICT [ by row_number[coord]]:\n{button_key_dict}\n\n")
    buttons.row_dict = button_key_dict
    buttons.make_row_col_dict()

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

        if event in buttons.coord_list:
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
