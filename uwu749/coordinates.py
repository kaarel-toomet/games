import numpy as np
import globals
import blocks
import world
import pygame as pg

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
    def draw(self, dx, dy, blocks):
       """
       draws the activeWindow on screenBuffer
       tries to speed up stuff by scrolling the visible parts
         inputs:
       dx: chunk id difference (old - new) for horizontal
           if None, draw everything
       dy: same for vertical
       blocks: the block images corresponding to the activeWindow codes
       """
       ## we move all blocks we can by scrolling.
       ## but these tiles on screen we have to update:
       ## wxRange: which horizontal range (in tiles) to update
       ## wyRange: vertical
       if dx == 1:
           # moving left -> redraw left edge
           wxRange = range(0, chunkWidth)
       elif dx == -1:
           wxRange = range(2*chunkWidth, 3*chunkWidth)
       else:
           ## None or 0: no horizontal movement,
           ## update everything here
           wxRange = range(0, 3*chunkWidth)
       if dy == 1:
           # moving up -> redraw upper edge
           wyRange = range(0, chunkHeight)
       elif dy == -1:
           wyRange = range(2*chunkHeight, 3*chunkHeight)
       else:
           ## None or 0: no vertical movement,
           ## update everything here
           wyRange = range(0, 3*chunkHeight)
       w = ((blocks[ self.matrix[wy,wx] ], windowToScreenBuffer(wx, wy))
            for wy in wyRange for wx in wxRange)
       globals.screenBuffer.blits(w)

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


def moveWindow(worldLoc):
    """
    move the active window into the new chunk position
    centered on world coordinates worldLoc = (x, y)
    """
    newChunk = chunkID(worldLoc)
    ## scroll the old part of screen accordingly
    oldChunk = globals.activeWindow.getChunkID()
    dx = (oldChunk[0] - newChunk[0])*chunkWidth*tileSize
    dy = (oldChunk[1] - newChunk[1])*chunkHeight*tileSize
    globals.screenBuffer.scroll(dx, dy)
    ## draw the new missing pieces
    globals.activeWindow.update(globals.ground, newChunk)
    globals.activeWindow.draw(oldChunk[0] - newChunk[0],
                              oldChunk[1] - newChunk[1],
                              blocks.blocks)
    globals.activeMineralGold.empty()
    # have to empty the group here to tell sprites they
    # do not belong to that group.  Otherwise will belong
    # to both to the old and new group
    globals.activeMineralGold = world.activeSprites(globals.mineralGold)
    globals.activeKollid.empty()
    # have to empty the group here to tell sprites they do not belong to that group
    globals.activeKollid = world.activeSprites(globals.kollid)
    coordinateShifts(newChunk, worldLoc[0], worldLoc[1])


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
