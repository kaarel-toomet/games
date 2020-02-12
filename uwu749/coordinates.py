import numpy as np

## basic data (meant to be private)
screenWidth, screenHeight = None, None
chunkWidth = None
chunkHeight = None
tileSize = None
## shifts: 
winsx = None  # window
winsy = None
sbsx = None  # screenBuffer
sbsy = None
ssx = None  # screen
ssy = None
blitShift = None, None  # blit whole screen

class activeWindow():
   """
   data related to the activeWindow: a square of the 9 cunks, centered at Crazy Hat
   """
   def __init__(self, width, height):
      self.matrix = np.empty((height, width), 'int8')
      self.chunkID = None
      # contains no chunks so far...
   def __getitem__(self, key):
      """
      return the tile code in window
      None if out of range
      """
      try:
         return self.matrix[key[0], key[1]]
      except:
         return None
   def __setitem__(self, key, value):
      self.matrix[key[0], key[1]] = value
   def draw(self, screenBuffer, blocks):
       """
       draws the activeWindow on screenBuffer
       screenBuffer:
       blocks: the block images corresponding to the activeWindow codes
       """
       for wx in range(self.getWidth()):
          # note: we run over window coordinates
          for wy in range(self.getHeight()):
             sbLoc = windowToScreenBuffer(wx, wy)
             screenBuffer.blit(blocks[ self.matrix[wy,wx] ], sbLoc)

   def getChunkID(self):
      """
      get the chunkID for the central chunk
      """
      return self.chunkID
   
   def getChunkIDs(self):
      """
      get a list of all chunkID-s in this window
      """
      chunkIDs = [(self.chunkID[0]-1, self.chunkID[1]-1), (self.chunkID[0], self.chunkID[1]-1), (self.chunkID[0]+1, self.chunkID[1]-1),
                  (self.chunkID[0]-1, self.chunkID[1]), (self.chunkID[0], self.chunkID[1]), (self.chunkID[0]+1, self.chunkID[1]),
                  (self.chunkID[0]-1, self.chunkID[1]+1), (self.chunkID[0], self.chunkID[1]+1), (self.chunkID[0]+1, self.chunkID[1]+1)]
      return chunkIDs
   
   def getWidth(self):
      return self.matrix.shape[1]
   def getHeight(self):
      return self.matrix.shape[0]
   
   def update(self, world, chunkID):
      """
      load new chunks to the active window, store back the old chunks
      in case those have been changed
      inputs:
      world: the World object
      chunkID: chunkID for the new center
      """
      if not self.chunkID is None:
         ## put back modified chunks
         iChunk, jChunk = self.chunkID
         for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
            for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
               world.put((jc, ic), self.matrix[j*chunkHeight:(j+1)*chunkHeight, i*chunkWidth:(i+1)*chunkWidth])
      else:
         self.chunkID = chunkID
         # set chunkID here if it is None at initialization
      ## read new chunks to the window
      iChunk, jChunk = chunkID
      for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
         for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
            self.matrix[j*chunkHeight:(j+1)*chunkHeight, i*chunkWidth:(i+1)*chunkWidth] = world.get((jc, ic))
      self.chunkID = chunkID
      # set new chunkid after doing all updates
    
def setup(screenw, screenh, chunkwidth, chunkheight, tilesize):
   global screenWidth, screenHeight, chunkWidth, chunkHeight, tileSize
   screenWidth, screenHeight = screenw, screenh
   chunkWidth = chunkwidth
   chunkHeight = chunkheight
   tileSize = tilesize

def chunkID(worldLoc):
   """
   return chunkID based on worldLoc = (x,y)
   inputs:
   worldLoc: tuple (x, y), world coordinates
   """
   return worldLoc[0] // chunkWidth, worldLoc[1] // chunkHeight

def inchunkToWorld(chunkID, inchunkLoc):
    """
    transform in-chunk coordinates to world coordinates
    chunkID: chunk id (i, j)
    inchunkLoc = (chunkx, chunky): window coordinates (in tiles)
    returns:
    (x, y): world coordinates (in tiles)
    """
    chunkx, chunky = inchunkLoc
    return (chunkID[1]*chunkWidth + chunkx, chunkID[0]*chunkHeight + chunky)
   
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
    winsx = -(iChunk - 1)*chunkWidth
    winsy = -(jChunk - 1)*chunkHeight
    ssx = int(screenWidth/2) - cx*tileSize
    # note: we can directly translate b/w world and screen w/o need for window!
    ssy = int(screenHeight/2) - cy*tileSize
    blitShift = worldToScreen(-winsx, -winsy)


def moveWindow(loc):
    """
    move the active window into the new position centered on world coordinates
    loc = (x, y)
    """
    chunkID = chunkID(loc)
    globals.activeWindow.update(globals.ground, chunkID)
    globals.activeWindow.draw(globals.screenBuffer, blocks1.blocks)
    globals.activeMineralGold.empty()
    # have to empty the group here to tell sprites they do not belong to that group
    globals.activeMineralGold = world.activeSprites(globals.mineralGold)
    globals.activeKollid.empty()
    # have to empty the group here to tell sprites they do not belong to that group
    globals.activeKollid = world.activeSprites(globals.kollid)
    coordinates.coordinateShifts(chunkID, loc[0], loc[1])


def screenToWorld(screenx, screeny):
    """
    transform world coordinates to screen coordinates
    screenx, screeny: screen coordinates (pixels), horizontal, vertical
    returns:
    (x, y): world coordinates
    """
    return ((screenx - ssx) // tileSize, (screeny - ssy) // tileSize)

 
def windowToWorld(winx, winy):
    """
    transform window coordinates to world coordinates
    winx, winy: window coordinates (in tiles)
    returns:
    (x, y): world coordinates (in tiles)
    """
    return(winx - winsx, winy - winsy)
   
    
def worldToWindow(x,y):
    """
    transform world coordinates to window coordinates
    x, y: world coordinates (in tiles)
    returns:
    (winx, winy): window coordinates (in tiles)
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
