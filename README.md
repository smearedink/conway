conway
======

Conway's Game of Life... everybody has to make this at some point, right?

Each time step the following things happen to each cell:
1. If a cell is alive and exactly TWO or THREE of its eight neighbours are alive, it remains alive
2. If a cell is alive and the above condition does not hold, it dies
3. If a cell is dead and exactly THREE of its eight neighbours are alive, it becomes alive
That is all!

This includes a really really kludgey RLE file reader I wrote that seems to work, so hey, good enough.  People seem to post Game of Life starting conditions online in RLE format.  If they've done that, you can include the filename on the command line and if you're lucky, it will be loaded.  This is not the most efficiently written Game of Life ever, so don't be surprised if enormous initial conditions run horribly.

+/-: zoom in/out
click: switch cells between dead (black) and alive (white)
space: start/stop time
arrows: pan around
q/esc: quit
