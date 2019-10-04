import numpy as np

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

class activeWindow():
   """
   data related to the activeWindow: a square of the 9 cunks, centered at Crazy Hat
   """
   def __init__(self, width, height):
      self.matrix = np.empty((width, height), 'int8')
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
      return self.matrix.shape[0]
   def getHeight(self):
      return self.matrix.shape[1]
   
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
               world.put((jc, ic), self.matrix[j*chunkSize:(j+1)*chunkSize, i*chunkSize:(i+1)*chunkSize])
      ## read new chunks to the window
      iChunk, jChunk = chunkID
      for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
         for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
            self.matrix[j*chunkSize:(j+1)*chunkSize, i*chunkSize:(i+1)*chunkSize] = world.get((jc, ic))
      self.chunkID = chunkID

    
def setup(screenw, screenh, chunksize, tilesize):
   global screenWidth, screenHeight, chunkSize, tileSize
   screenWidth, screenHeight = screenw, screenh
   chunkSize = chunksize
   tileSize = tilesize

def chunkID(worldLoc):
   """
   return chunkID based on worldLoc = (x,y)
   inputs:
   worldLoc: tuple (x, y), world coordinates
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
