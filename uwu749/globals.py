#!/usr/bin/env python3
"""
global variables that need to be accessed in different modules
these are just variable declarations, these must
be initialized in uwu, or in the corresponding module
"""
import pygame as pg

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
# Berlin noise data for ground
groundNoiseParams = (50, 50, 10, 0.5, 2, 1024, 1024, 0)

# memory are where drawing is done, and part of which is showed on monitor
screenBuffer = None
