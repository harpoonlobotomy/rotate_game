"""thinking of just having a separate script for this, because the original is just so damn messy."""

# for now just going to copy the vital bits here for planning.

from PIL import Image, ImageEnhance, ImageDraw, ImageOps
import os

def logger(string):
    logging = False#True
    if logging:
        print(string)

def histograms(filename):
    ### from https://codedrome.substack.com/p/image-histograms-with-python-and-pillow ###

    def create_histograms(image):

        """
        Takes a Pillow image.
        Returns a dictionary of Pillow images of colour
        histograms.
        For colour (mode "RGB") images there are 3 with
        keys "red", "green" and "blue".
        For greyscale (mode "L") images there is one with key "greyscale".
        Raises ValueError if mode is not "RGB" or "L"
        """

        if image.mode == "RGB":

            normalized_frequencies = _create_normalized_frequencies_rgb(image)

            return {"red": _create_histogram((0,), normalized_frequencies["red"]),
                    "green": _create_histogram((1,), normalized_frequencies["green"]),
                    "blue": _create_histogram((2,), normalized_frequencies["blue"])}

        elif image.mode == "L":

            normalized_frequencies = _create_normalized_frequencies_greyscale(image)

            return {"greyscale": _create_histogram((0,1,2), normalized_frequencies)}

        else:

            raise ValueError("Image must have mode of RGB or L")


    def _create_normalized_frequencies_rgb(image):

        """
        Create a dictionary of 3 sets of frequencies
        as fractions of the highest frequency.
        Keys are "red", "green" and "blue".
        Frequencies are lists.
        """

        # get the flat frequencies data using the Pillow histogram method
        frequencies = image.histogram()

        # find the highest of the 3 frequencies
        max_freq = max(frequencies)

        # Create the dictionary using list comprehensions.
        normalized_frequencies = {"red": [f / max_freq for f in frequencies[0:256]],
                                "green": [f / max_freq for f in frequencies[256:512]],
                                "blue": [f / max_freq for f in frequencies[512:768]]}

        return normalized_frequencies


    def _create_normalized_frequencies_greyscale(image):

        """
        Create a list of of frequencies as
        fractions of the highest frequency.
        """

        # get the flat frequencies data using the Pillow histogram method
        frequencies = image.histogram()

        # get the highest frequency
        max_freq = max(frequencies)

        # calculate frequencies using list comprehension
        normalized_frequencies = [f / max_freq for f in frequencies]

        return normalized_frequencies


    def _create_histogram(channels, frequencies):

        """
        Create a histogram from frequency
        data as a Pillow image.
        """

        width = 256
        height = 158
        column_width = 1

        im = Image.new("RGB", (width, height), (255,255,255))

        draw = ImageDraw.Draw(im)

        col = [0,0,0]

        for v in range(0, 256):

            # set the value of the particular RGB channel
            # to values between 0 and 255
            for channel in channels:
                col[channel] = v

            # draw the individual histogram column
            draw.line(xy=[(v, height),(v, height - (height * frequencies[v]))],
                    fill=tuple(col),
                    width=column_width)

        return im

    image = Image.open(filename)
    if image.mode == "RGBA":
        image = image.convert("RGB")

    histograms = create_histograms(image)
    if image.mode == "RGB":

        histograms["red"].save("histogram_red.png", "PNG")
        histograms["green"].save("histogram_green.png", "PNG")
        histograms["blue"].save("histogram_blue.png", "PNG")

def make_square(cell_w, colour, padding, transparent_centre=True):
    logger("make_square")
    output_name =  f"{colour}_square.png" if not transparent_centre else  f"{colour}_square_trans.png"
    outer_width = int(cell_w-(padding*2))
    #outer_height = cell_w-(padding*2)-4
    new_image = Image.new("RGBA", (outer_width-4, outer_width-4), colour) # is -4 here to compensate for the -2 of placement. But it shouldn't be an int like this, it should be defined by padding. Hm. #TODO

    if transparent_centre:
        inner_square_width = int((cell_w*.66))
        print(f"inner square width: {inner_square_width}")
        inner_square = Image.new("RGBA", (inner_square_width, inner_square_width), color=(0,0,0,0))
        #print(f"inner_square: {inner_square.getbbox(alpha_only=False)}") # inner_square: (0, 0, 68, 68

        gap = int((outer_width - inner_square_width)/2)

        if colour == "white":
            semitrans_width = inner_square_width + gap
            semitrans_gap = int((outer_width - semitrans_width)/2)
            semitrans = Image.new("RGBA", (semitrans_width, semitrans_width), (255,255,255,125)) # is -4 here to compensate for the -2 of placement. But it shouldn't be an int like this, it should be defined by padding. Hm. #TODO
            new_image.paste(semitrans, box=(semitrans_gap, semitrans_gap, semitrans_width + semitrans_gap, semitrans_width + semitrans_gap))


        new_image.paste(inner_square, box=(gap, gap, inner_square_width + gap, inner_square_width + gap))

    new_image.save(output_name, "PNG")
    return output_name

class image_manip_data: # at some point combine this with img_data but for now they're separate because I'm tired

    #image_dict = {} # dict to send back with all relevant data in it
    """[x, y coordinates] = (r, g, b values)"""

    def __init__(self):
        logger("init image_manip_data")
        self.output_filename = None
        self.img_width = None
        pass

    def quantise_img(self, Imageimage=None, combine=False, strength=2, save_file=False, is_tile=False):
        logger("quantise_img")
        from PIL import ImageFilter as filt
        if Imageimage:
            im= Imageimage
        else:
            im = Image.open(self.output_filename)

        width, height = im.size
        im = im.convert("RGB")
        with Image.new("RGB", size=(width*2, height*2)) as new_image:

            #im.show()
            im = ImageOps.posterize(im, 6)
            cutoff_val = (.5 if strength == 3 else .25 if strength == 2 else 5)
            #im_1 = ImageOps.autocontrast(im, cutoff = .5, preserve_tone=True)
            im_1 = im.quantize(method=1, colors=46, dither=False)#, dither=False)
            im_1 = im_1.convert("RGB")
            if strength == 1:
                if not is_tile:
                    im_1 = ImageOps.autocontrast(im_1, cutoff = .4, preserve_tone=True)
                im_1 = im_1.filter(filter=filt.ModeFilter(size=3))
                if save_file:
                    im_1.save(save_file)
                return im_1
            im_2 = ImageOps.autocontrast(im_1, cutoff = .6, preserve_tone=True)
            #im_1.show()
            #contrast = ImageEnhance.Contrast(im)
            #contrast.enhance(1.5).show()
            #im_2.show()
            #sleep(.5)
            #new_image.save(f"{self.filename.replace('.png', '')}_horizontal_concatenated_image.png")

            #exit()
            if strength == 2:
                if save_file:
                    im_2.save(save_file)
                return im_2
            im_3 = im_2.filter(filter=filt.ModeFilter(size=5))
            #im_3.show()
            #m = im.filter(filter=filt.DETAIL())
            #im.show()
            #sleep(.5)
            if combine:
                new_image.paste(im, (0, 0))
                new_image.paste(im_1, (im.width, 0))
                new_image.paste(im_2, (0, im_1.height))
                new_image.paste(im_3, (im.width, im_1.height))

                new_image.save(f"{self.output_filename.replace('.png', '')}_horizontal_concatenated_image.png")
            """im_4 = im_3.filter(filter=filt.ModeFilter(size=10))
            im_sharpen = im.filter(filter=filt.SHARPEN())
            im_sharpen = im_detail.filter(filter=filt.SHARPEN())
            im_sharpen.show()
            sleep(.5)
            new_image.paste(im_4, (im_4.width, im_1.height))
            #im_4.show()
            #sleep(.5)"""

            #im_filt_then_quan = im_filtered.quantize(20, dither=False)
            #im_filt_then_quan.show()
            #sleep(.5)
            if save_file:
                im_3.save(save_file)
            return im_3
            """histo_after = im.histogram()
            print(f"Histo: {histo_before}")
            print(f"Histo: {histo_after}")
            im.show()
"""

    def set_file_data(self, base_file, filename, region_size=None, padding=9, grid_size=4):
        logger("set_file_data")

        self.output_filename = filename
        if region_size:
            if region_size[0] < region_size[1]:
                target_width = region_size[0]
            else:
                target_width =  region_size[1]
        else:
            target_width = 400

        self.padding=padding

        with Image.open(base_file) as im:
            if im.height != int(target_width) or im.width != int(target_width):
            #im = im.resize(size=(int(target_width*.8), int(target_width*.8))) # 80% of the available height. currently assuming landscape, will adapt later.
                im = im.resize(size=(int(target_width), int(target_width))) # 80% of the available height. currently assuming landscape, will adapt later.

            #with Image.new("RGBA", size=(int(target_width*.8), int(target_width*.8))) as new_im:
                with Image.new("RGBA", size=(int(target_width), int(target_width))) as new_im:
                    new_im.paste(im)
                    new_im.save(self.output_filename, format="png")

                    print(f"Base image saved at: {self.output_filename}")

        self.region_height = target_width
        self.img_width = new_im.size[0]
        self.col_width = int(self.img_width / grid_size)
        self.row_width = int(self.img_width / grid_size)
        #self.spacing = int(self.img_width / grid_size)

    def _get_pixel_data(self, im):
        """Pixel data as a sequence of (r,g,b,a) tuples. Works on Pillow < 12.1 (getdata) and >= 12.1 (get_flattened_data)."""
        logger("_get_pixel_data")
        if hasattr(im, "get_flattened_data"):
            return im.get_flattened_data()
        return im.getdata()

    def determine_bg_color(self, im, border_percentage: int = 5):
        logger("determine_bg_color")
        from collections import Counter
        if not (0 <= border_percentage <= 100): raise ValueError("border_percentage must be between 0 and 100")
        rgb_im = im.convert('RGBA')
        width, height = im.size
        border_px_width = int(width * border_percentage / 100)
        border_px_height = int(height * border_percentage / 100)
        edges = []
        for crop_box in [
            (0, 0, width, border_px_height),
            (0, 0, border_px_width, height),
            (width - border_px_width, 0, width, height),
            (0, height - border_px_height, width, height),
        ]:
            edges.extend(self._get_pixel_data(rgb_im.crop(crop_box)))

        return Counter(edges).most_common(1)[0][0]

        """def square_image(self, im: Image):
        logger("square_image")
        im_width, im_height = im.size
        mode = im.mode
        min_dimension = min(im_width, im_height)
        max_dimension = max(im_width, im_height)
        #print("Resizing image to a square...")
        #print("Determining background color...")
        bg_color = self.determine_bg_color(im)
        #print("Background color is... " + str(bg_color))
        im_r = Image.new(
            mode = mode,
            size = (max_dimension, max_dimension),
            color = bg_color
            )
        offset = int((max_dimension - min_dimension) / 2)
        if im_width > im_height:
            im_r.paste(im, (0, offset))
        else:
            im_r.paste(im, (offset, 0))
        return im_r"""

    def extract_tiles(self, image_path, col_width: int, row_height: int, padding: int, effect=False):

        logger("extract_tiles")
        im = Image.open(image_path)
        #print(f"im.size in extract: {im.size}")
        cols = int(self.img_width / col_width)
        rows = int(self.img_width / row_height)

        if not effect:
            import os
            output_dir = f"{os.getcwd()}" + r"\tiles"

        coords = []
        tile_filenames = {}
        bbox_dict = {}
        for row in range(0, rows):
            tile_filenames[row] = {}
            bbox_dict[row] = {}
            for column in range(0, cols):
                box = ((column * col_width)+(padding/2), (row * row_height)+(padding/2), (column * col_width +
                    col_width)-(padding/2), (row * row_height + row_height)-(padding/2))
                #outputs.append(im.crop(box))
                tile = im.crop(box)
                bbox_dict[row][column] = box
                coords.append((row, column))
                if not effect: # just save here immediately instead of going through merge
                    with Image.new(mode="RGBA", size=tile.size, color=(255, 0, 0, 0)):
                        crop_value = self.padding / 2
                        box = (crop_value, crop_value, tile.size[0]-crop_value, tile.size[0]-crop_value)
                        button = tile.crop(box=box)
                        #button_cropped.paste(im=button, box=box)
                        outp_path = os.path.join(output_dir, f"row_{row}_col_{column}.png")
                        button.save(outp_path) # final file outputs
                        tile_filenames[row][column] = outp_path

        return image_path, coords, tile_filenames, bbox_dict

    def merge_tiles(self, output_path, img_tiles, manipulate=True, subtlety=2, save_single=True, save_result=False, save_base=True):
        logger("merge_tiles")
        import os

        coord_to_img_dict = {}

        coords = []
        if save_result:
            new_image = Image.new("RGB", (self.img_width, self.img_width))

        output_dir = f"{os.getcwd()}" + r"\tiles"
        for row in img_tiles:
            coord_to_img_dict[row] = {}
            for column in img_tiles[row]:
                tile = img_tiles[row][column]
                coords.append((row, column))

                if manipulate:
                    tile = raw_img_data.quantise_img(tile, combine=False, strength=subtlety, save_file=output_path, is_tile=True)
                if save_single:
                    with Image.new(mode="RGBA", size=tile.size, color=(255, 0, 0, 0)) as button_cropped:
                        crop_value = self.padding / 2
                        box = (crop_value, crop_value, tile.size[0]-crop_value, tile.size[0]-crop_value)
                        button = tile.crop(box=box)
                        #button_cropped.paste(im=button, box=box)
                        outp_path = os.path.join(output_dir, f"row_{row}_col_{column}.png")
                        coord_to_img_dict[row][column] = outp_path
                        button.save(outp_path) # final file outputs

                if save_result:
                    new_image.paste(tile, (column * tile.size[0], row * tile.size[1]))

        if save_result:
            new_image.save(output_path)
            new_image.close()

        return output_path, coord_to_img_dict, coords

    def split_img(self, image_path, grid_size, padding=8, effects=True):
        logger("split_img")
        # adapted from https://github.com/whiplashoo/split-image/blob/main/src/split_image/split.py

        #import os
        #print(f"im.size on opening for `{image_path}`: `{im.size}` f")

        #name, ext = os.path.splitext(image_path)
       # name = os.path.basename(name)
        #output_dir = "./"

        self.img_width
        col_width = int(self.img_width / grid_size) # currently all squares. Once I've got that working will play with rectangles but this is it for now.
        row_height = int(self.img_width / grid_size)
        #print(f"col w and h just before extract_tiles: {col_width} / {row_height}")
        #print(f" cols: {cols} // rows: {rows}")
        #image_dict = {"incoming_filename": image_path, "image_size": self.img_width, "col_width": col_width, "row_height": row_height, "padding": padding}
        new_image, coords, img_tile_dict, bbox_dict = raw_img_data.extract_tiles(image_path, col_width, row_height, padding) # don't actually need to output new_image here as it's just image_path, but makes it easier to blend w/ merge_tiles output if needed later.
        """if save_tiles_alone:
            for n, item in enumerate(outputs):
                outp_path = name + "_" + str(n) + ext
                outp_path = os.path.join(output_dir, outp_path)
                print("Exporting image tile: " + outp_path)
                item.save(outp_path) # final file outputs

        else: # assume we manipulate the image and reassemble"""
        #print(f"Image size before sending to merge_tiles: `{im.size}`")
        if effects:
            new_image, coord_to_img_files, coords_list = raw_img_data.merge_tiles(output_path=image_path, img_tiles=img_tile_dict, manipulate=effects, subtlety = 1, save_single=True)

        return new_image, coords, img_tile_dict, bbox_dict
        # note: tile_img_dict is now [row][column]["tile_path"] and [bbox]. if effect==True, then ["tile_path" will not be added yet but in merge_tiles, which will become effects.]

    #base_file = r"Screenshot 2026-04-18 233936_output.png"

    def generate_img_grid(self, base_file, region_size=None, effects=False, padding=8, grid_size = 4, grid_data=None):
        logger(f"Generate image grid for {base_file}")
        if grid_data:
            print("\nimg_manip got grid_data data\n\n")
            padding = grid_data.gap
            grid_size = grid_data.grid_size
            region_size = grid_data.width, grid_data.height # here, 'region' is actually the full size of the image.
        #input_filename = "image_name_for_testing.png" # r"Screenshot 2026-04-18 233936_output.png"

        temp_file_filename = f"{base_file.replace('.png', '').replace("gallery", "temp")}_temp.png"
        print(f"\nABOUT TO GENERATE `{temp_file_filename}` from `{base_file}`\n")
        raw_img_data.set_file_data(base_file = base_file, filename=temp_file_filename, region_size=region_size, padding=padding, grid_size=grid_size)
        #input_filename = "manip_testing_2.png"
        if effects:
            raw_img_data.quantise_img(save_file = temp_file_filename, strength=1)

        output_filename, coords_list, tiles_dict, bbox_dict = self.split_img(temp_file_filename, grid_size, padding=padding, effects=effects)

        logger(f"Returning `{output_filename}` from generate_img_grid")
        return output_filename, tiles_dict, bbox_dict, coords_list, self.img_width


raw_img_data = image_manip_data()

def move_focus(shift, image, x_gap, y_gap, x, y, box, strength=0, specify=False):
    print(f"starting_box = {box}")
    new_box = None

    if specify:
        new_box = (x_gap, y_gap, x_gap + x, y_gap + y)

    elif shift.lower() == "l":
        x_gap = x_gap/(2 + strength)
        new_box = (x_gap, y_gap, x_gap + x, y_gap + y)
    elif shift.lower() == "r":
        x_gap = x_gap*(2 + strength)
        new_box = (x_gap, y_gap, x_gap + x, y_gap + y)
    else:
        print(f"{shift} is not understood. Returning unchanged.")
        cropped = image

    if new_box:
        print(f"NEW BOX: {new_box}")
        cropped = image.crop(new_box)

        a, b, c, d = box
        e, f, g, h = new_box
        left = a-e
        right = c-g
        print(f"diff: left: {left}, right: {right}")

        if new_box:
            box = new_box
        return cropped, box

def make_square_png(orig_dir = None, make_thumbnails=False, new_length = 200, force_make=False, thumbnail_dir=rf"{os.getcwd()}\\gallery_thumbnails\\"):

    #print(f"directory : {listdir(f'{getcwd()}\\init_gallery\\')}\n")
    gallery_dir = f'{os.getcwd()}\\gallery\\' # < - the images already squared. Should also set a max pixel size at some point.

    if not orig_dir:
        orig_dir = f'{os.getcwd()}\\init_gallery\\'

    gallery_list = [f for f in os.listdir(orig_dir)]
    print(f"Gallery list: {gallery_list}")
    if make_thumbnails:
        gallery_list =  [f for f in os.listdir(f'{gallery_dir}')]

    gallery_list = list(i for i in gallery_list if ".png" in i.lower())
#generate_img_grid(base_file = "image_name_for_testing.png", effects=False)
    for i in gallery_list:

        if make_thumbnails:
            path = f"{gallery_dir}{i}"
        else:
            path = f"{orig_dir}{i}"

        with Image.open(path) as im:
            if make_thumbnails:
                path = f"{thumbnail_dir}{i}"
            #print(f"Path: {path}")
            else:
                path = path.replace("init_gallery", "gallery")
            #print(f"Path: {path}")
            if ("_squared.png" in i.lower() and not make_thumbnails) or ("_thumbnail.png" in i.lower() and make_thumbnails):
                filename = i
            else:
                filename = i.replace(" ", "_").replace(".png", "")
                if len(filename) > 10:
                    filename = filename[:10]

                if make_thumbnails:
                    filename = path.replace(i, filename)
                    filename = filename + "_thumbnail.png"
                else:
                    if "_squared" not in filename:
                        filename = path.replace(i, filename) + "_squared.png"

            if os.path.isfile(filename) and not force_make:
                print(f"{filename} already exists, skipping.")
                continue
            #print(f"Filename: {filename}")
            starting_size = im.size
            #im.show()
            print(f"Starting size for {filename}: {starting_size}")
            x, y = starting_size
            if x != y:

                if x < y:
                    new_x = x
                    new_y = x
                else:
                    new_x = y
                    new_y = y

                print(f"new_x: {new_x}")
                print(f"new_y: {new_y}")
                x_diff = x - new_x
                y_diff = y - new_y
                x_diff = abs(x_diff)
                y_diff = abs(y_diff)
                print(f"x_diff: {x_diff} / y_diff: {y_diff}")

                x_gap = x_diff / 2
                y_gap = y_diff / 2

                print(f"x_gap = {x_gap} / y_gap: {y_gap}")
                """
    left: The x-coordinate of the leftmost edge.
    upper: The y-coordinate of the top edge.
    right: The x-coordinate of the rightmost edge.
    lower: The y-coordinate of the bottom edge.
                """
            #im = im.resize(size=(int(target_width*.8), int(target_width*.8))) # 80% of the available height. currently assuming landscape, will adapt later.
                box = (x_gap, y_gap, x_gap + new_x, y_gap + new_y)
                cropped = im.crop(box = box)
                cropped.show()
                test = input("Is this correct? enter `r` or `l` to move the focus, 'undo' to terminate, or nothing to continue as is.")
                if test:
                    strength = 0
                    while test:
                        if test.lower() == "undo":
                            print(f"Terminating, please make required alterations. {i} has not been altered.")
                            break
                        cropped, box = move_focus(test, im, x_gap, y_gap, new_x, new_y, box, strength)
                        cropped.show()
                        test = input("Is this correct? enter `r` or `l` to move the focus, `undo` to go back to the original, or nothing to continue as is.")
                        strength += 1

                if test and test.lower() == "undo":
                    test = input("Do you want to give more specific instruction, or just cancel?")
                    if not test:
                        break
                    while test:
                        if test.lower() == "undo":
                            print(f"Terminating, please make required alterations. {i} has not been altered.")
                            break
                        test = input(f"Current x_gap is {x_gap}. Please enter the new x_gap you wish to use, as an integer.")
                        try:
                            x_gap = int(test.strip())
                            cropped, box = move_focus(test, im, x_gap, y_gap, new_x, new_y, box, specify=True)
                            cropped.show()
                            test = input("Is this correct? If not, enter the new value you wish to use, or `undo` to go back to the original. Otherwise, just hit enter to save.")
                        except:
                            print(f"Could not recognise `{test}` as an integer.")


                #break
                    #im = im.resize(size=(int(target_width), int(target_width))) # 80% of the available height. currently assuming landscape, will adapt later.

            #im.paste(im, )
                with Image.new("RGB", (cropped.width, cropped.height)) as new_image:
                    new_image.paste(cropped)

            else:
                with Image.new("RGB", (x, y)) as new_image:
                    new_image.paste(im)

            if make_thumbnails:
                new_image = new_image.resize(size=(new_length, new_length))

                print(f"make_thumbnails new size: {new_image.size}")

            new_image.save(filename, "PNG")
            break
        #raw_img_data.set_file_data(i, filename, region_size=None, padding=9, grid_size=4)
make_square_png()
