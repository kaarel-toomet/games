"""
Custom sprite classes
"""
import numpy as np
import pygame as pg
import random

import blocks
import coordinates
import world
import globals

crazyHatImage = None
kollImage = None
kuldImage = None

def setup(tileSize):
   global kuldImage, kollImage, crazyHatImage
   crazyHatImage = pg.transform.scale(pg.image.load("pic.png"),(tileSize, tileSize))
   kuldImage = pg.transform.scale(pg.image.load("kuld.png"),(tileSize, tileSize))
   kollImage = pg.transform.scale(pg.image.load("koll.png"),(tileSize, tileSize))
      

class ChunkSprites():
   """
   Group of sprites connected to chunks and will be loaded/saved
   when one updates chunk location.
   This is the base class w/o update, the actual classes have to
   implement update, including eventual movement

   central data structure is a dict
   { chunkID -> list of sprites }
   empty list: this has been initialized
   None: it has not been initialized
   
   If the sprite moves, one has to remove it from the previous chunkID
   and add it to the new chunkID in case of crossing chunk boundaries
   """
   def __init__(self):
      self.chunks = {}
      self.N = 0
      # total number of minerals across all chunks
   def add(self, sprite):
      """
      add new sprite at it's (world) coordinates
      """
      chunkID = coordinates.chunkID((sprite.x, sprite.y))
      ## add the sprite to the chunk-specific list
      chunkSprites = self.chunks.get(chunkID, [])
      # when adding a sprite, we do not care about initialization flag,
      # hence we only pull in the list
      chunkSprites.append(sprite)
      self.chunks[chunkID] = chunkSprites
      # adding even a single sprite marks this list as initialized
      self.N += 1

   def get(self, chunkID):
      """
      return the list of sprites at this chunkID
      None if not initialized
      empty list if initialized but everything removed
      """
      sprites = self.chunks.get(chunkID, None)
      return sprites

   def getN(self):
      """
      how many items in total across all chunks
      """
      return self.N

   def moveChunk(self, sprite, newChunkID):
      """
      remove the sprite from old chunkID and add it to newChunkID
      """
      chunkSprites = self.chunks.get(sprite.chunkID, [])
      try:
         chunkSprites.remove(sprite)
         self.chunks[sprite.chunkID] = chunkSprites
      except:
         print("cannot remove sprite", id(sprite), "from chunk", sprite.chunkID)
      chunkSprites = self.chunks.get(newChunkID, [])
      chunkSprites.append(sprite)
      self.chunks[newChunkID] = chunkSprites
   
   def remove(self, spriteList):
      """
      remove these sprites from ChunkSprites
      """
      for sprite in spriteList:
         chunkID = coordinates.chunkID((sprite.x, sprite.y))
         chunkSprites = self.chunks.get(chunkID, [])
         try:
            chunkSprites.remove(sprite)
            self.N -= 1
            self.chunks[chunkID] = chunkSprites
         except ValueError:
            print("sprite not in list", id(sprite))
            print(len(chunkSprites), "chunkSprites:", chunkSprites)
            for cm in chunkSprites:
               print("but there is chunk sprites id:", id(cm))


class CrazyHat(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = crazyHatImage
        self.rect = self.image.get_rect()
        ## location in world coordinates
        self.x=x
        self.y=y
        ## 'rect' will be drawn on screen buffer, hence must be in screenbuffer coords
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
    def update(self, mup, mdown, mleft, mright):
        """
        use relative movements (mup, mdown...) to update
        Crazy Hat's position
        This means screen position is changed too,
        potentially involving active window change and
        chunk update
        """
        y = self.y
        x = self.x
        if mup:
            y = self.y - 1
        if mdown:
            y = self.y + 1
        if mleft:
            x = self.x - 1
        if mright:
            x = self.x + 1
        winx, winy = coordinates.worldToWindow(x, y)
        if globals.activeWindow[(winy,winx)] in blocks.solid:
            return
        if globals.activeWindow[(winy,winx)] in blocks.breakable:
            globals.activeWindow[(winy,winx)] = blocks.breakto[globals.activeWindow[(winy,winx)]]
            globals.screenBuffer.blit( blocks.blocks[blocks.breakto[globals.activeWindow[(winy,winx)]]],
                                       coordinates.worldToScreenbuffer(x, y))
        self.x, self.y = x, y
        chunkID = globals.activeWindow.getChunkID()
        chunkID1 = coordinates.chunkID((self.x, self.y))
        if chunkID1 != chunkID:
            ## chunk changed: update activeWindow and sprites
            coordinates.moveWindow((x, y))
        coordinates.coordinateShifts(chunkID, self.x, self.y)
        # update the coordinate system at every move, not just for chunk update
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
    def getxy(self):
        """
        return world coordinates
        """
        return(self.x, self.y)

    def setxy(self,x,y):
        """
        use world coordinates to set Crazy Hat's position
        x, y: world coordinates
        """
        self.x, self.y = x, y
        chunkID = globals.activeWindow.getChunkID()
        chunkID1 = coordinates.chunkID((self.x, self.y))
        if chunkID1 != chunkID:
            ## chunk changed: update activeWindow and sprites
            coordinates.moveWindow((x, y))
        coordinates.coordinateShifts(chunkID, self.x, self.y)
        # update the coordinate system at every move, not just for chunk update
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)


class Gold(pg.sprite.Sprite):
    def __init__(self, x, y, n=100):
        """
        x, y: world coordinates
        """
        pg.sprite.Sprite.__init__(self)
        self.image = kuldImage
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
        self.n = n
    def update(self):
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)

class Koll(pg.sprite.Sprite):
    def __init__(self, x, y=None):
        """
        x, y: world coordinates
        if y is None, x must be a tuple of coordinates
        """
        pg.sprite.Sprite.__init__(self)
        self.image = kollImage
        self.rect = self.image.get_rect()
        if isinstance(x, tuple):
           self.x = x[0]
           self.y = x[1]
        else:
           self.x=x
           self.y=y
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
        self.chunkID = coordinates.chunkID((self.x, self.y))
        self.tick = 0
        self.delay = 30

    def getxy(self):
       """
       return world coordinates
       """
       return(self.x, self.y)
   
    def update(self, monsters): 
        """
        moves the koll toward the CrazyHat
        monsters: list of monsters (ChunkSprites), have to update monsters in this list
                  as self is 'activeKollid'
        """
        self.tick += 1
        if self.tick == self.delay:
            self.tick = 0
            xy = globals.hullmyts.getxy()
            # hullmyts: CrazyHat, needed for movement direction
            delta = np.sign([self.x - xy[0], self.y - xy[1]])
            winx, winy = coordinates.worldToWindow(self.x-delta[0],self.y-delta[1])
            if globals.activeWindow[(winy,winx)] in blocks.solid:
               return
            self.x -= delta[0]
            self.y -= delta[1]
            newChunkID = coordinates.chunkID((self.x, self.y))
            if newChunkID != self.chunkID:
               ## put it into the new chunk
               monsters.moveChunk(self, newChunkID)
               self.chunkID = newChunkID
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)


## Define globals
globals.mineralGold = ChunkSprites()
