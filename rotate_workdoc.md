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

Current bugs/errors:
 * since the recent change to how the grids are formed/squares are coloured, if reverting to a 5x5 grid, only the top left square is coloured. No apparent errors other than that obvious failure. Need to figure out why. But tbh that whole section is a mess of old and new parts, so should find the reason + solution in due course.
 * buttons need larger margins, can't see the background enough half the time.
