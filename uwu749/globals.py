#!/usr/bin/env python3
"""
global variables that need to be accessed in different modules
these are just variable declarations, these must
be initialized in uwu, or in the corresponding module
"""
import pygame as pg
import blocks

## CrazyHat: the player
hullmyts = None
## sprite group for crazy hat
player = pg.sprite.Group()

# the window that contains active chunks
activeWindow = None
# mineral gold: mineral means it is not movin
mineralGold = None
# mineral gold in active window
activeMineralGold = None
# monsters that want to eat you.  Technically, unlike minerals, these move
kollid = None
# monsters in the active window
activeKollid = None

# tiles for the ground
ground = None
# Perlin noise data for ground
groundNoiseParams = (50, 50, 20, 0.5, 2, 1024, 1024, 0)

# memory are where drawing is done, and part of which is showed on monitor
screenBuffer = None

class GameState():
    """
    contains information on the current state of the game,
    including lives, points, inventory, current location,
    home, etc
    """
    def __init__(self):
        self.punktid = 0
        self.homeX = 0  # where Crazy Hat has her home
        self.homeY = 0
        ## inventory stuff
        self.inventory = [blocks.MQQK,blocks.KIRKA,-1,-1,-1,-1,-1,-1,-1,-1, -1]
        self.amounts = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0,  0]
        self.lifes = 10
        self.kuld = 0
        self.kollivaremed = 0
    def __str__(self):
        s = "GameState object:\n" +\
        " punktid: " + str(self.punktid) + "\n" +\
        " homeX, homeY: " + str((self.homeX, self.homeY))
        return s
