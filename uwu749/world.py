### code for creating and operating with the world
import numpy as np
import noise
import pygame as pg

import coordinates


def activeSprites(sprites, activeWindow):
   """
   extract the sprites from 'sprites' that are inside 'activeWindow'
   INPUTS:
   sprites:
   chunk-sprite groups like 'Minerals'
   RETURN:
   pg.sprits.Group of sprites inside of the window
   """
   activeSprites = pg.sprite.Group()
   chunkIDs = activeWindow.getChunkIDs()
   for chunkID in chunkIDs:
      s = sprites.get(chunkID)
      if s is not None:
         activeSprites.add(s)
   return(activeSprites)


class World:
   """
   Define the world
   The main component of it is a dict (chunk id) -> chunk of tiles
   the main functions:
   __init__: set up parameters and empty data

   You have to set up coordinates before you set up the world
   That initializes chunkSize and such
   """
   def __init__(self, freqX, freqY, a, b, c, d, e, f):
      """
      read parameters and set up and empty world
      freqX, freqY: Perline noise frequency
      a,b,c,d,e,f: other noise params, please rename appropriately!
      """
      self.chunks = {}
      self.freqX, self.freqY = freqX, freqY
      self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f
   def get(self, chunkID):
      """
      return the chunk data
      if chunk does not exist, create it, store it, and return so
      next time it already exists
      chunkID: tuple (ic, jc) of chunk column, row
      """
      if chunkID in self.chunks:
         return self.chunks[chunkID]
      chunk = np.empty((coordinates.chunkSize, coordinates.chunkSize), 'int8')
      jc, ic = chunkID
      for cx in range(chunk.shape[0]):
          for cy in range(chunk.shape[1]):
              ## world coordinates for Perlin noise computation
              x = ic*coordinates.chunkSize + cx
              y = jc*coordinates.chunkSize + cy
              noiseval = noise.snoise2(x/self.freqX, y/self.freqY,
                                       self.a, self.b, self.c, self.d, self.e, self.f,)
              if noiseval < -0.3:
                  chunk[cy,cx] = 7
              elif noiseval < -0.05:
                  chunk[cy,cx] = 0
              elif noiseval < 0:
                  chunk[cy,cx] = 1
              elif noiseval < 0.3:
                  chunk[cy,cx] = 2
              elif noiseval < 0.4:
                  chunk[cy,cx] = 3
              elif noiseval < 11:
                  chunk[cy,cx] = 4
      self.chunks[chunkID] = chunk
      return chunk

   def put(self, chunkID, data):
      self.chunks[chunkID] = data.copy()
