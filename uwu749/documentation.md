# UWU749: Help

## How to play

TBD

## How to code: technical background

### Coordinates: code to handle coordinate systems and translations

#### Related Concepts

* **chunk**: a square of tiles of size `chunkSize`.  This is used to copy
   tiles data from world to _active window_.
   Each chunk is identified by
   `(iChunk, jChunk) = (x // chunkSize, y // chunkSize)`.
   If Crazy Hat is located at `(x, y)`, this corresponds to the chunks
   `(x // chunkSize, y // chunkSize)`.
   This chunk, and all it's 8 neighbors are copied into _active window_.
* **world**: this is a collection of all tiles of the world.  It
   contain the world properties (type of tile as 'int8') for every possible location.
   Technically, world is stored as a dict of of chunks where _chunk
   id_-s (see below) are used as keys.
 * **active window** (or just window):  an area of the world near the Crazy Hat that is 
   stored as a matrix and where all the immediate movements and
   screen drawings are done.  The main motivation for this structure
   is to simplify these operations.  It is made of tile codes like
   _world_ and unlike _screenbuffer_,
   and hence cannot be directly drawn.
 * **screenbuffer** is a mirror of active window, just made of pixels
   (tile images), not tile id-s.
   Hence one can copy _screenbuffer_ directly to the graphical memory.
   All the drawing is initially done in _screenbuffer_ and when a frame
   is ready, this is copied
   (blitted) to the screen memory.
 * **screen**: the physical screen and the associated graphical screen,
   normally visible to the user.
   This is pretty similar thing to a monitor.
 
#### Coordinate systems
 
the game uses 4 types of coordinates:
* **world coordinates**.  These are in tiles and of unlimited size.
  Normally the center is at `(0,0)`.  The numbers grow right and
  down.  Typically denoted as `x`, `y`.
* **active window coordinates** in tiles, `(0,0)` is top left.  It's
  size is `3*chunkSize`.  Normally denoted `winx`, `winy`.
* **screenBuffer coordinates**, in pixels, `(0,0)`, is top left.
  Pretty much the same thing as _active window coordinated_, just in
  pixels.  It is a square with side length `3*chunkSize*tileSize`.
* **screen coordinates** in pixels, (0,0) is top left
   these measure pixel locations on current screen.  Size is stored in
   `screenWidth`, `screenHeight`, and depends on your monitor.


#### Coordinate translations

translation is mainly done using tuples (sx, sx) to shift to screen coords,
and (wx, wx) to screenBuffer coords.


#### Code
