"""thinking of just having a separate script for this, because the original is just so damn messy."""

# for now just going to copy the vital bits here for planning.

from PIL import Image, ImageEnhance, ImageDraw, ImageOps

### from https://codedrome.substack.com/p/image-histograms-with-python-and-pillow ###

def histograms(filename):

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

class image_manip_data: # at some point combine this with img_data but for now they're separate because I'm tired

    base_image:str=None
    filename:str=None

    base_img_width:int=None
    base_img_height:int=None

    pixel_dict:dict={}

    str_to_coord:dict = {}

    image_dict = {} # dict to send back with all relevant data in it
    """[x, y coordinates] = (r, g, b values)"""

    def __init__(self):
        pass

    def quantise_img(self, Imageimage=None, combine=False, strength=2, save_file=False, is_tile=False):

        from PIL import ImageFilter as filt
        if Imageimage:
            im= Imageimage
        else:
            im = Image.open(self.filename)

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

                new_image.save(f"{self.filename.replace('.png', '')}_horizontal_concatenated_image.png")
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

    def set_file_data(self, base_file=None, filename=None, region_size=None, padding=9):

        import json
        settings = "rotate_settings.json"
        with open(settings, "r") as settings:
            settings_data = json.load(settings)

        self.grid_size = settings_data["grid_size"]
        self.difficulty = settings_data["difficulty"]
        self.background_colour = settings_data["background_colour"]
        self.default_screen_size = settings_data["screen_size"]
        self.is_fullscreen = settings_data["fullscreen"]

        self.filename = filename

        if region_size:
            self.img_region_width, self.img_region_height = region_size
        else:
            self.img_region_width, self.img_region_height = 400, 400

        self.padding=padding

        self.base_image = base_file

        with Image.open(base_file) as im:
            width, height = im.size
        self.base_img_width = im.size[0]
        self.base_img_height = im.size[1]#height

        if self.img_region_height != self.base_img_height:
            print(f"Image region is {self.img_region_height} but the image is {self.base_img_height}")
        if not self.base_img_width or not self.base_img_height:
            print(f"Not self.width or self.height: {self.base_img_width} / {self.base_img_height}/ exiting, can't handle this yet.")
            exit()

        """
        So instead of the below, maybe I check to see whether w or h is closer to region dimensions (or which exceeds by more) and scale by that. Would make more sense. Currently the whole grid setup is expecting strictly squares, but I think it should be pretty straightforward to change it? I think....
        """
        #target_x = int(target_x/2)
        #target_y = int(target_y/2) # arbitrarily, img is half the screen size. Will figure a better way of doing it. Maybe an interim screen for image selection before the grid is generated, and the region area is defined then?
        if abs(self.img_region_width - width) > 100 or abs(self.img_region_height - height) > 100:
            #print("IMAGE IS THE WRONG SIZE.")
            width_diff = abs(self.img_region_width - width)
            #print(f"Width diff: {width_diff}")
            height_diff = abs(self.img_region_height - height)
            #print(f"Height diff: {height_diff}")
            #if width_diff > height_diff:
                #print("Is more wrong in width than height. How/why does this matte? No idea.")
        with Image.open(base_file) as im:
            im = im.resize(size=(int(self.img_region_height*.8), int(self.img_region_height*.8)))
            with Image.new("RGBA", size=(int(self.img_region_height*.8), int(self.img_region_height*.8))) as new_im:
                new_im.paste(im)
                new_im.save(self.filename, format="png")
                img_manip_data.base_image = self.filename
                print(f"Base image saved at: {self.filename}")

        self.base_img_width = new_im.size[0]
        self.base_img_height = new_im.size[1]
        self.spacing = int(self.base_img_width / self.grid_size)
        #self.dot_radius = int((self.spacing-5)/2) ## want to remove the 'radius' here entirely. If we're going to be outputting dot representations of the img, it should be defined by the dimensions, not hardcoded like this. This was just because I had a starting image to figure out how it'd work, not because it was a good idea.
        #self.spacing_between_edges = int(self.spacing - self.dot_radius)
        print(f"width at end: {self.base_img_width}")
        print(f"height at end: {self.base_img_height}")

    def _get_pixel_data(self, im):
        """Pixel data as a sequence of (r,g,b,a) tuples. Works on Pillow < 12.1 (getdata) and >= 12.1 (get_flattened_data)."""
        if hasattr(im, "get_flattened_data"):
            return im.get_flattened_data()
        return im.getdata()

    def determine_bg_color(self, im, border_percentage: int = 5):
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

    def square_image(self, im: Image):
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
        return im_r

    """def reverse_split(self, paths_to_merge, rows, cols, image_path, should_cleanup=False, should_quiet=False):
        if len(paths_to_merge) == 0:
            print("No images to merge!")
            return
        for index, path in enumerate(paths_to_merge):
            path_number = int(path.split("_")[-1].split(".")[0])
            if path_number != index:
                print("Warning: Image " + path +
                    " has a number that does not match its index!")
                print("Please rename it first to match the rest of the images.")
                return

        images_to_merge = [Image.open(p) for p in paths_to_merge]
        image1 = images_to_merge[0]
        new_width = image1.size[0] * cols
        new_height = image1.size[1] * rows
        new_image = Image.new(image1.mode, (new_width, new_height))
        for path in paths_to_merge:
            print("Path: ", path)
        print("Merging image tiles with the following layout:", end=" ")
        for i in range(0, rows):
            print("\n")
            for j in range(0, cols):
                print(paths_to_merge[i * cols + j], end=" ")
        print("\n")
        for i in range(0, rows):
            for j in range(0, cols):
                image = images_to_merge[i * cols + j]
                new_image.paste(image, (j * image.size[0], i * image.size[1]))
        print("Saving merged image: " + image_path)
        new_image.save(image_path)
        if should_cleanup:
            import os
            for p in paths_to_merge:
                print("Cleaning up: " + p)
                os.remove(p)"""

    def extract_tiles(self, im: Image, col_width: int, row_height: int, padding: int):
        im_width, im_height = im.size
        print(f"im.size in extract: {im.size}")
        cols = int(im_width / col_width)
        rows = int(im_height / row_height)
        if not cols.is_integer(): raise ValueError("column width must be a factor of the total image width")
        if not rows.is_integer(): raise ValueError("row height must be a factor of the total image height")
        rows, cols = int(rows), int(cols)
        print(f"[in extract_tiles]  cols: {cols} // rows: {rows}")
        outputs = []
        output_dict = {}
        for i in range(0, rows):
            output_dict[i] = {}
            for j in range(0, cols):
                box = ((j * col_width)+(padding/2), (i * row_height)+(padding/2), (j * col_width +
                    col_width)-(padding/2), (i * row_height + row_height)-(padding/2))
                outputs.append(im.crop(box))
                output_dict[i][j] = im.crop(box)

        #return outputs
        return output_dict

    def merge_tiles(self, output_path, outputs, image_size=None, manipulate=True, subtlety=2, save_single=True, save_result=False, save_base=True, col_width=5, row_height=5):

        import os
        #output_path = r"tile_recombined_2.png"
        overlay_img = None
        make_overlay = False

        coord_to_img_dict = {}

        if make_overlay:
            overlay_img = Image.new("RGBA", image_size, color="#458976")

        coords = []
        if save_result:
            new_image = Image.new("RGB", image_size)
        output_dir = f"{os.getcwd()}" + r"\tiles"
        for row in outputs:
            coord_to_img_dict[row] = {}
            for column in outputs[row]:
                tile = outputs[row][column]
                coords.append((row, column))

                if manipulate:
                    tile = img_manip_data.quantise_img(tile, combine=False, strength=subtlety, save_file=output_path, is_tile=True)
                if save_single:
                    with Image.new(mode="RGBA", size=tile.size, color=(255, 0, 0, 0)) as button_cropped:
                        crop_value = self.padding / 2
                        box = (crop_value, crop_value, tile.size[0]-crop_value, tile.size[0]-crop_value)
                        button = tile.crop(box=box)
                        #button_cropped.paste(im=button, box=box)
                        outp_path = os.path.join(output_dir, f"row_{row}_col_{column}.png")
                        coord_to_img_dict[row][column] = outp_path
                        button.save(outp_path) # final file outputs

                        """if overlay_img:
                            paste_box = (column * col_width, row * row_height, column * col_width +
                                col_width, row * row_height + row_height)
                            overlay_img.paste(im=button_cropped, box=paste_box)
"""
                if save_result:
                    new_image.paste(tile, (column * tile.size[0], row * tile.size[1]))

        if overlay_img:
            #overlay_img.show()
            overlay_img.save("overlay_img.png")
            overlay_img.close()

        if save_result:
            new_image.save(output_path)
            new_image.close()

        return output_path, coord_to_img_dict, coords
        return new_image, coord_to_img_dict # sends the actual image instance

        """im.crop(box)"""

        """box = (j * col_width, i * row_height, j * col_width +
            col_width, i * row_height + row_height)
        outputs.append(im.crop(box))
        output_dict[i][j] = im.crop(box)"""

img_manip_data = image_manip_data()

def split_img(image_path, cols, rows, should_square=False, save_tiles_alone = False, padding=8, effects=True):

    # adapted from https://github.com/whiplashoo/split-image/blob/main/src/split_image/split.py


    import os
    im = Image.open(image_path)
    print(f"im.size on opening for `{image_path}`: `{im.size}` f")
    img_manip_data.img_size = im.size
    name, ext = os.path.splitext(image_path)
    name = os.path.basename(name)
    output_dir = "./"

    if should_square:
        im_r = img_manip_data.square_image(im)
        outp_path = name + "_squared" + ext
        outp_path = os.path.join(output_dir, outp_path)
        im_r.save(outp_path) # intermediary file output
        im = im_r

    img_manip_data.img_size = im.size
    col_width = int(im.size[0] / cols)
    row_height = int(im.size[1] / rows)
    print(f"col w and h just before extract_tiles: {col_width} / {row_height}")
    print(f" cols: {cols} // rows: {rows}")
    image_dict = {"incoming_filename": image_path, "image_size": im.size, "col_width": col_width, "row_height": row_height, "padding": padding}
    outputs = img_manip_data.extract_tiles(im, col_width, row_height, padding)
    #print(f"OUTPUTS: {outputs}")

    """if save_tiles_alone:
        for n, item in enumerate(outputs):
            outp_path = name + "_" + str(n) + ext
            outp_path = os.path.join(output_dir, outp_path)
            print("Exporting image tile: " + outp_path)
            item.save(outp_path) # final file outputs

    else: # assume we manipulate the image and reassemble"""
    print(f"Image size before sending to merge_tiles: `{im.size}`")
    new_image, coord_to_img_files, coords_list = img_manip_data.merge_tiles(output_path=image_path, outputs=outputs, image_size=im.size, manipulate=effects, subtlety = 1, save_single=True, col_width=col_width, row_height=row_height)
    return new_image, coord_to_img_files, coords_list, im.size
    """  coord_to_img_files: [row_no][column_no]["tile_filename.png"]  """

#base_file = r"Screenshot 2026-04-18 233936_output.png"

def generate_img_grid(base_file, region_size=None, effects=False, padding=8, grid_size = 4, grid_data=None):

    if grid_data:
        padding = grid_data.gap
        grid_size = grid_data.grid_size
        region_size = grid_data.width, grid_data.height # here, 'region' is actually the full size of the image.
    #input_filename = "image_name_for_testing.png" # r"Screenshot 2026-04-18 233936_output.png"

    temp_file_filename = f"{base_file.replace('.png', '')}_temp.png"
    print(f"\nABOUT TO GENERATE `{temp_file_filename}` from `{base_file}`\n")
    img_manip_data.set_file_data(base_file = base_file, filename=temp_file_filename, region_size=region_size)
    #input_filename = "manip_testing_2.png"
    if effects:
        img_manip_data.quantise_img(save_file = temp_file_filename, strength=1)

    new_image, coord_to_img_files, coords_list, img_size = split_img(temp_file_filename, grid_size, grid_size, should_square=True, save_tiles_alone = False, padding=padding, effects=effects)
    return new_image, coord_to_img_files, coords_list, img_size

#generate_img_grid(base_file = "image_name_for_testing.png", effects=False)
