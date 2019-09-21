
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

def chunkID(worldLoc):
   """
   return chunkID based on worldLoc = (x,y)
   """
   return worldLoc[0] // chunkSize, worldLoc[1] // chunkSize
   
def coordinateShifts(chunkID, cx, cy):
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
    iChunk, jChunk = chunkID
    wsx = -(iChunk - 1)*chunkSize
    wsy = -(jChunk - 1)*chunkSize
    ssx = int(screenWidth/2) - cx*tileSize
    # note: we can directly translate b/w world and screen w/o need for window!
    ssy = int(screenHeight/2) - cy*tileSize
    blitShift = worldToScreen(-wsx, -wsy)

def updateWindow(activeWindow, world, chunkID1, chunkID=None):
   """
   load new chunks to the active window, store back the old chunks
   in case those have been changed
   inputs:
   activeWindow: window, will be changed by reference
   world: the World object
   chunkID1: new chunkID (iChunk, jChunk)
   chunkID: old chunkID, for storing stuff back to the world
   """
   ## read new chunks to the window
   print("new chunk", chunkID1)
   iChunk, jChunk = chunkID1
   for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
      for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
         activeWindow[i*chunkSize:(i+1)*chunkSize, j*chunkSize:(j+1)*chunkSize] = world.get((ic, jc))

    
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
