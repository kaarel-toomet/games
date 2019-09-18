## ---------- coordinate translation ----------
## the game needs 4 types of coordinates:
## * screen coordinates in pixels, (0,0) is top left
## * screenBuffer coordinates, in pixels, (0,0), is top left
## * active window coordinates in tiles, (0,0) is top left.  The
##   same as screenBuffer, except in tiles instead of pixels
## * world coordinates, in tiles, potentially unlimited, (0,0) is center (TBD)
##
## translation is mainly done using tuples (sx, sx) to shift to screen coords,
## and (wx, wx) to screenBuffer coords.

## basic data (meant to be private)
screenWidth, screenHeight = None, None
chunkSize = None
tileSize = None
## shifts: 
wsx = None  # window
wsy = None
sbsx = None  # screenBuffer
sbsy = None
ssx = None  # screen
ssy = None
blitShift = None, None  # blit whole screen

def setup(screenw, screenh, chunksize, tilesize):
   global screenWidth, screenHeight, chunkSize, tileSize
   screenWidth, screenHeight = screenw, screenh
   chunkSize = chunksize
   tileSize = tilesize

def coordinateShifts(iChunk, jChunk, cx, cy):
    """
    compute the coordinate shifts b/w coordinates
    shifts should be _added_ to the world coordinates to make the translation,
    not substracted
    INPUTS: 
    iChunk, jChunk: central chunk of the active window
    cx, cy: screen center world coordinates 
            normally location of Crazy Hat
    RETURNS:
    (ssx, ssy, wsx, wsy)
    wx, wy: shift b/w world and window coordinates
    """
    global wsx, wsy, sbsx, sbsy, ssx, ssy, blitShift
    wsx = -(iChunk - 1)*chunkSize
    wsy = -(jChunk - 1)*chunkSize
    ssx = int(screenWidth/2) - cx*tileSize
    # note: we can directly translate b/w world and screen w/o need for window!
    ssy = int(screenHeight/2) - cy*tileSize
    blitShift = worldToScreen(-wsx, -wsy)

def worldToWindow(x,y):
    """
    transform world coordinates to window coordinates
    x, y: world coordinates
    returns:
    (bx, by): screen buffer coordinates (in tiles)
    """
    return(wsx + x, wsy + y)

def worldToScreen(x, y):
    """
    transform world coordinates to screen coordinates
    x, y: world coordinates
    returns:
    (ex, ey): screen coordinates
    """
    return(ssx + x*tileSize, ssy + y*tileSize)

def worldToScreenbuffer(x, y):
    """
    transform world coordinates to screenbuffer coordinates
    x, y: world coordinates
    returns:
    (ex, ey): screenbuffer coordinates (in pixels)
    """
    return((wsx + x)*tileSize, (wsy + y)*tileSize)
 
def windowToScreenBuffer(wx, wy):
    """
    translate from window coordinates to screenBuffer coordinates
    """
    return wx*tileSize, wy*tileSize
