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
   def __init__(self, dimension, altitudeParam, materials, thresholds):
      """
      read parameters and set up and empty world
      inputs:
      dimension: name of the layer, such as "ground"
      altitudeParam: Perline noise parameters for
         biome altitude (freqX, freqY, a,b,c,d,e,f)
      """
      self.dimension = dimension
      freqX, freqY, a, b, c, d, e, f = altitudeParam
      self.chunks = {}
      self.freqX, self.freqY = freqX, freqY
      self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f
      self.materials = materials
      self.thresholds = thresholds
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
               r.seed(1000*cx+cy)
               n = 0
               holegen = r.randint(0,100)
               noiseval = noise.snoise2(x/self.freqX, y/self.freqY,
                                       self.a, self.b, self.c, self.d,
                                       self.e, self.f,) + 1*noise.snoise2(x/1500,y/1500,20,0.5,2,1024,1024,0)
               noiseval2 = 0.7*noise.snoise2(x/(self.freqX*2) + 10, y/(self.freqY*2) + 10,
                                       self.a, self.b, self.c, self.d,
                                       self.e, self.f,) + 0.7*noise.snoise2((x/3000)+10,(y/3000)+10,20,0.5,2,1024,1024,0)
               
               while noiseval > self.thresholds[n]:
                  n += 1
               chunk[cy,cx] = self.materials[n]
               n=0
      self.chunks[chunkID] = chunk
      ## create minerals: sprites that do not move
      for i in range(1):
          chunkx, chunky = (np.random.randint(0, chunk.shape[1]),
                            np.random.randint(0, chunk.shape[0]))
          x, y = coordinates.inchunkToWorld(chunkID, (chunkx, chunky))
          globals.mineralGold.add(sprites.Gold((x, y)))
      globals.activeMineralGold = activeSprites(globals.mineralGold)
      # those mineral sprites that are in activeWindow
      return chunk

   def put(self, chunkID, data):
      self.chunks[chunkID] = data.copy()
