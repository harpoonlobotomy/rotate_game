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
