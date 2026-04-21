rotate_workdoc.md

Bit late to start this bit might as well.

The basic game works; you click a square, and the 4 adjacent squares rotate clockwise; the goal is to get all the colours back to their correct places.

Currently implemented:
 * custom image selection (without any image manipulation other than scale)
 * basic 'scramble' (randomly rotates random points a number of times depending on difficulty)
 * win condition
 * consistent square colour (so a moved colour can be moved again, etc.)
 * click counts

To do:
 * hint button to flash incorrect squares (potentially useful for large grids with lots of similar colours) ## basic version done, just turns them briefly white and restores.
 * image cleaning (simplify colour palette, maybe increase contrast if low, same for saturation, etc)
 * non-square images
 * zoom? Is that even possible? Probably extremely messy with how it redraws the window already.
 * fix the 'scramble' fn
 * obvs much nicer UI
 * 'gallery' of sample images for now. Later maybe levels? idk. Need to sort the difficulty curve first.
 * Re: above, start with gallery selection, use that window to get grid region size for button size/img manipulation. [note: an event in the column (eg clicking button) updates the region size to print accurately.]
 * Render a PNG of the modified image and use that as the background, instead of having each button have its own coloured background. Loading one img vs colouring all those backgrounds has to be a slight improvement, right? Still store the target_colour data the exact same way, just don't represent it via button backgrounds.
 * For tiles with virtually no difference, make them identical and interchangable. I don't want 5 identical black squares failing the challenge because technically one has a few pixels of extremely dark blue while another has extremely dark brown. Not implemented at all yet. Almost need to hash the avg colour val of the square and compare that, comparing actual filenames is really silly. Maybe I need to rework the button class so the buttons actually move and carry their images with them, instead of the button being the stationary point waiting for its colour to return. Conceptually, anyway. Hm.

Current bugs/errors:
 * since the recent change to how the grids are formed/squares are coloured, if reverting to a 5x5 grid, only the top left square is coloured. No apparent errors other than that obvious failure. Need to figure out why. But tbh that whole section is a mess of old and new parts, so should find the reason + solution in due course.
 * buttons need larger margins, can't see the background enough half the time.

1.42pm
So, figured out how to split images, give them transparent padding etc.The idea is to have the buttons be fullsize with no padding (though I'll likely have to add a minimum of padding for things to work) and for the 'padding' to actually be a transparent area of the button, which the background (the same original image/colour) will show through. Not sure if that's how it'll work but that's what I'm going to try. That or we just leave off the transparent padding and do regular padding, not sure which I want yet.

Need to totally rejig the button building. And honestly the dicts overall.

Might just run two entirely separate paths for this afternoon, one that uses image-buttons, the other what I already have. Instead of trying to blend them together. Just redo a bunch of it with images instead. Eh.

4.17pm
Getting there.
Have the data now  to set the grid size by available space, and to make image-buttons. Just need to do it now. But a rest first, exhausted.

9:24am 20/4/26
Notes:
- turn image effects on/off
- set grid size within game
- 'set image' should set start_screen=False, not just gallery selection
- 'add to gallery' button for images set
- need background image behind buttons

I can't see how to add a background image to the button grid. Might have to go back to my original idea of using button backgrounds, though I'm not sure if those can be images. Goddamn.

10.59pm
Have to shift to a sg.Graph version, I just don't think I can get it to work with the current columns/buttons. Doesn't seem to a functioning background option, and the only other way is to add the inbetween slivers as separate canvases, and that feels like a godawful 'solution'. So, graph it is. Have a working test graph in a separate script with faux buttons so the concept is sound enough.

3.54pm
Decent progress made, the grid is now in place and is clickable but the children aren't implemented yet.
Also there seems to be a sub-pixel misalignment; the lower buttons seem to move down extremely slightly and the very top ones seem to move the other way.  Need to make sure I'm storing position boxes as cleaned values so that's minimised.

5.07pm
Graph is basically working now. Rotation works as before, but now the 'buttons' have proper surrounds. There's no darkening when it's clicked which is unfortunate, but overall it works.

Currently no resolution for images with extremely similar image-tiles (eg an image with a uniform background), it currently requires the current image to be the target image.

7.41pm
scramble works again, as do hints.

7.54pm
The rotation is going the wrong way. No wonder I was struggling.

10.03pm
improved the ui some.

0.19am
exit button doesn't work during gameplay
sometimes (for reasons I don't understand yet) the tiles shown aren't correct. They appear correct but the accuracy check shows them as wrong and when you rotate it they seemingly appear out of nowhere, potentially appearing as duplicates, that then disappear when rotated. Can't see a common thread/cause yet. Will test more tomorrow.

0:54am
Now the splash screen is showing twice. I removed a bunch of extraneous code from the original version but now this is happening. Will figure it out tomorrow. Should already be in bed.

Should add a transparent square in the white square so you can still see the image underneath. Make it like a glowing border. Would help with identifying the above problem and be prettier.

11.20am 21/4/26
re splash screen showing twice:
"in align_children
in align_children"
plays twice.

So, it does this:

    ABOUT TO GENERATE `rave_shaman_temp.png` from `rave_shaman.png`

    Base image saved at: rave_shaman_temp.png
    child_dict: {full dict here}
    in align_children
    No coord_to_img_files or not coords_list
    child_dict: {full dict here}
    new_img_data found
    Base positions ordered children:

It's because setup needs the image data first to make the grid, but then the grid makes the image again.

Still not sure why the splash screen runs twice.
But for now -
going to isolate the 'new image' process, so all the data is in one place to be used by whatever needs it.

Oh - the splashscreen was running twice because I imported
#from rotate_01 import base_positions, image_data
to get the data typing for set_up_buttons. As soon as I removed that it stopped. Good to know.

Hm. Had this cause a crash:

*  File "d:\Git_Repos\rotate_game\rotate_gui_01.py", line 378, in show_incorrect
*    update_clicked_square(x, y, new_image, click_off=True)

Need to make the text output box bigger and more appealing.

Need to figure out why it's sometimes showing the wrong tile.
It seems to only come about from scrambling, I've not seen it happen in user clicking.
(Though it does rotate the wrong way, I really need to fix that.)
Maybe this?
            if not hasattr(img_data, "coord_to_img_files") or not img_data.coord_to_img_files:
                filename = g.coord_to_img_files[row][column]
            else:
                filename = img_data.coord_to_img_files[row][column]
