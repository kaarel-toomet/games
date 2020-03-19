### code for creating and operating with the world
import numpy as np
import noise
import pygame as pg
import random as r

import coordinates
import globals
import sprites
import blocks

def activeSprites(sprites):
   """
   extract the sprites from 'sprites' that are inside 'activeWindow'
   INPUTS:
   sprites: chunk-sprite groups like 'Minerals', or 'Monsters'
   RETURN:
   pg.sprites.Group of sprites inside of the window
   """
   activeSprites = pg.sprite.Group()
   chunkIDs = globals.activeWindow.getChunkIDs()
   for chunkID in chunkIDs:
      s = sprites.get(chunkID)
      # list of sprites for this chunk
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
   That initializes chunkWidth, chunkHeight and such
   """
   def __init__(self, altitudeParam):
      """
      read parameters and set up and empty world
      freqX, freqY: Perline noise frequency
      a,b,c,d,e,f: other noise params, please rename appropriately!
      """
      freqX, freqY, a, b, c, d, e, f = altitudeParam
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
      ## create a new chunk
      chunk = np.empty((coordinates.chunkHeight, coordinates.chunkWidth), 'int8')
      jc, ic = chunkID
      for cx in range(chunk.shape[1]):
          for cy in range(chunk.shape[0]):
              ## world coordinates for Perlin noise computation
              x = ic*coordinates.chunkWidth + cx
              y = jc*coordinates.chunkHeight + cy
              noiseval = noise.snoise2(x/self.freqX, y/self.freqY,
                                       self.a, self.b, self.c, self.d,
                                       self.e, self.f,) + 1*noise.snoise2(x/1500,y/1500,20,0.5,2,1024,1024,0)
              noiseval2 = 0.7*noise.snoise2(x/(self.freqX*2) + 10, y/(self.freqY*2) + 10,
                                       self.a, self.b, self.c, self.d,
                                       self.e, self.f,) + 0.7*noise.snoise2((x/3000)+10,(y/3000)+10,20,0.5,2,1024,1024,0)
              biome1 = r.uniform(-0.1,0.5)
              biome2 = r.uniform(-0.2,0)
              if noiseval < -0.3:
                 chunk[cy, cx] = blocks.SYGAVM
              elif noiseval < 0:
                 chunk[cy, cx] = blocks.SEA
              elif noiseval < 0.07:
                 chunk[cy, cx] = blocks.SAND
              elif noiseval < 0.3:
                  chunk[cy,cx] = blocks.MURU
                  if biome1 < noiseval2:
                      chunk[cy,cx] = blocks.PUU
                  elif biome2 > noiseval2:
                      chunk[cy,cx] = blocks.SAND
                      if r.randint(0,100) == 0:
                         chunk[cy,cx] = blocks.KAKTUS
              elif noiseval < 0.4:
                 chunk[cy, cx] = blocks.KIVI
              elif noiseval < 11:
                 chunk[cy, cx] = blocks.LUMI
      self.chunks[chunkID] = chunk
      ## create minerals: sprites that do not move
      for i in range(1):
          chunkx, chunky = (np.random.randint(0, chunk.shape[1]),
                            np.random.randint(0, chunk.shape[0])
          )
          x, y = coordinates.inchunkToWorld(chunkID, (chunkx, chunky))
          globals.mineralGold.add(sprites.Gold(x, y))
      globals.activeMineralGold = activeSprites(globals.mineralGold)
      # those mineral sprites that are in activeWindow
      return chunk

   def put(self, chunkID, data):
      self.chunks[chunkID] = data.copy()
