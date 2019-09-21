
## basic data (meant to be private)
screenWidth, screenHeight = None, None
chunkSize = None
tileSize = None
## shifts: 
winsx = None  # window
winsy = None
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
    COMPUTES:
    (ssx, ssy, winsx, winsy)
    wx, wy: shift b/w world and window coordinates
    """
    global winsx, winsy, sbsx, sbsy, ssx, ssy, blitShift
    iChunk, jChunk = chunkID
    winsx = -(iChunk - 1)*chunkSize
    winsy = -(jChunk - 1)*chunkSize
    ssx = int(screenWidth/2) - cx*tileSize
    # note: we can directly translate b/w world and screen w/o need for window!
    ssy = int(screenHeight/2) - cy*tileSize
    blitShift = worldToScreen(-winsx, -winsy)

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
   if not chunkID is None:
      ## put back modified chunks
      iChunk, jChunk = chunkID
      for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
         for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
            world.put((jc, ic), activeWindow[j*chunkSize:(j+1)*chunkSize, i*chunkSize:(i+1)*chunkSize])
   ## read new chunks to the window
   iChunk, jChunk = chunkID1
   for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
      for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
         activeWindow[j*chunkSize:(j+1)*chunkSize, i*chunkSize:(i+1)*chunkSize] = world.get((jc, ic))

    
def worldToWindow(x,y):
    """
    transform world coordinates to window coordinates
    x, y: world coordinates
    returns:
    (bx, by): screen buffer coordinates (in tiles)
    """
    return(winsx + x, winsy + y)

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
    return((winsx + x)*tileSize, (winsy + y)*tileSize)
 
def windowToScreenBuffer(wx, wy):
    """
    translate from window coordinates to screenBuffer coordinates
    """
    return wx*tileSize, wy*tileSize
