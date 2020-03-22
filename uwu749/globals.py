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

screenWidth = None
screenHeight = None
screen = None

# tiles for the ground
ground = None
underground = None
activelayer = None
# Perlin noise data for ground
groundNoiseParams = (50, 50, 20, 0.5, 2, 1024, 1024, 0)
undergroundNoiseParams = (50, 50, 20, 0.5, 2, 1024, 1024, 0)
# memory are where drawing is done, and part of which is showed on monitor
screenBuffer = None

pg.font.init()
def textrender(text, x, y, font=pg.font.SysFont("Times",24)):
    text = font.render(text, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text,text_rect)

class GameState():
    """
    contains information on the current state of the game,
    including lives, points, inventory, current location,
    home, etc
    """
    def __init__(self):
        self.punktid = 0
        self.home = (0, 0)  # where Crazy Hat has her home
        ## inventory stuff
        self.inventory = [blocks.MQQK,blocks.KIRKA,-1,-1,-1,-1,-1,-1,-1,-1, -1]
        self.amounts = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0,  0]
        self.lifes = 10
        self.kuld = 0
        self.kollivaremed = 0
        self.dimension = "ground"  # start on ground

    def dictify(self):
        d = {
            "punktid" : self.punktid,
            "home" : self.home,
            "inventory" : self.inventory,
            "amounts" : self.amounts,
            "lifes" : self.lifes,
            "kuld" : self.kuld,
            "kollivaremed" : self.kollivaremed,
            "dimension" : self.dimension
        }
        return d
        
    def __str__(self):
        s = "GameState object:\n" +\
        " punktid: " + str(self.punktid) + "\n" +\
        " home: " + str(self.home) +\
        " inventory: " + str(zip(self.inventory, self.amounts))
        return s

    def undictify(self, d):
        if "punktid" in d:
            self.punktid = d["punktid"]
        if "home" in d:
            self.home = d["home"]
        if "inventory" in d:
            self.inventory = d["inventory"]
        if "amounts" in d:
            self.amounts = d["amounts"]
        if "lifes" in d:
            self.lifes = d["lifes"]
        if "kuld" in d:
            self.kuld = d["kuld"]
        if "kollivaremed" in d:
            self.kollivaremed = d["kollivaremed"]
        if "dimension" in d:
            self.dimension = d["dimension"]
