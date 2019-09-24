"""
Custom sprite classes
"""
import coordinates

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

class Minerals(ChunkSprites):
   """
   ChunkSprites that do not move: just a dummy update()
   """
   def update(self):
      pass
