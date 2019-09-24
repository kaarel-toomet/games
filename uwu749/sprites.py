"""
Custom sprite classes
"""
import numpy as np
import pygame as pg
import random

import coordinates

koll = None
kuldImage = None

def setup(tileSize):
   global kuldImage, koll
   kuldImage = pg.transform.scale(pg.image.load("kuld.png"),(tileSize, tileSize))
   koll = pg.transform.scale(pg.image.load("koll.png"),(tileSize, tileSize))

class ChunkSprites():
   """
   Group of sprites connected to chunks and will be loaded/saved
   when one updates chunk location.
   This is the base class w/o update, the actual classes have to
   implement update, including eventual movement

   central data structure is a dict
   { chunkID -> list of minerals }
   empty list: this has been initialized
   None: it has not been initialized
   """
   def __init__(self):
      self.chunks = {}
      self.N = 0
      # total number of minerals across all chunks
   def add(self, mineral):
      """
      add new mineral at it's (world) coordinates
      """
      chunkID = coordinates.chunkID((mineral.x, mineral.y))
      ## add the mineral to the chunk-specific list
      chunkMinerals = self.chunks.get(chunkID, [])
      # when adding a mineral, we do not care about initialization flag,
      # hence we only pull in the list
      chunkMinerals.append(mineral)
      self.chunks[chunkID] = chunkMinerals
      # adding even a single mineral marks this list as initialized
      self.N += 1

   def get(self, chunkID):
      """
      return the list of minerals at this chunkID
      None if not initialized
      empty list if initialized but everything removed
      """
      minerals = self.chunks.get(chunkID, None)
      return minerals

   def getN(self):
      """
      how many items in total across all chunks
      """
      return self.N

   def remove(self, spriteList):
      for sprite in spriteList:
         chunkID = coordinates.chunkID((sprite.x, sprite.y))
         chunkMinerals = self.chunks.get(chunkID, [])
         try:
            chunkMinerals.remove(sprite)
            self.N -= 1
            self.chunks[chunkID] = chunkMinerals
         except ValueError:
            print("sprite not in list", id(sprite))
            print(len(chunkMinerals), "chunkMinerals:", chunkMinerals)
            for cm in chunkMinerals:
               print("but there is chunk minerals id:", id(cm))


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
    def __init__(self,x,y):
        """
        x, y: world coordinates
        """
        pg.sprite.Sprite.__init__(self)
        self.image = koll
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
    def update(self, hullmyts):
        """
        moves the koll at random toward the Crazy Hat
        """
        if np.random.randint(0,30) == 0:
            xy = hullmyts.getxy()
            delta = np.sign([self.x - xy[0], self.y - xy[1]])
            self.x -= delta[0]
            self.y -= delta[1]
            self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
    def lammutus(self,x,y):
        global punktid
        if self.x == x and self.y == y:
            kollid.remove(self)
            punktid += 100
