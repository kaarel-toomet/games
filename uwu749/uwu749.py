#!/usr/bin/env python3
import argparse
import pygame as pg
import numpy as np
import sys
import subprocess
import time

import blocks
import coordinates
import files1
import sprites
import world
import globals

## Command line arguments
parser = argparse.ArgumentParser(description='uwu749: Crazy Hat builds another world!')
parser.add_argument('-v', type=int, default=0,
                    help='verbosity level')
parser.add_argument('-x', '--width', type=int, default=64,
                    dest='width',        ##other useless comment
                    help='window width (tiles)')
parser.add_argument('-y', '--height', type=int, default=64,
                    dest='height',
                    help='window height (tiles)')
args = parser.parse_args()

## ---------- params ----------
kollProbability = 0.04

## ---------- blocks ----------
tileSize = 32
tileScale = int(tileSize/16)
# block size on screen, should depend on the screen resolution

pg.init()

## figure out the screen size
## The standard get_size() gives wrong results on multi-monitor setup
## use xrandr instead (only on linux)
xdotool = False
# did we get the data through xdotool?
if sys.platform == 'linux':
    res = subprocess.run("./activescreen", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(res.returncode == 0):
        # success
        wh = res.stdout.split(b' ')
        screenWidth = int(wh[0])
        screenHeight = int(wh[1])
        screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
        xdotool = True
if not xdotool:
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    screenWidth, screenHeight = pg.display.get_surface().get_size()
    pg.display.set_caption(str(np.random.randint(0,9000)))
    pg.mixer.init()
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()

## load config and all that
blocks.loadBlocks(tileSize)
kutt = pg.transform.scale(pg.image.load("person.png"),(tileSize, tileSize))
home = pg.transform.scale(pg.image.load("home.png"),(tileSize, tileSize))
hotbar = pg.transform.scale(pg.image.load("hotbar.png"),(180*tileScale, 18*tileScale))
selslot = pg.transform.scale(pg.image.load("selslot.png"),(18*tileScale, 18*tileScale))
##
bgColor = (64,64,64)
# dark gray

font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
tfont = pg.font.SysFont("Times",100)

def textrender(text,x,y,font=font):
    text = font.render(text, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text,text_rect)

def drawSprites(sprites, spriteBuffer):
    """
    Just draw the sprites listed in the group on screen
    ensure correct coordinates
    """
    sprites.draw(spriteBuffer)

def updateScreen():
    """
    update various sprites.
    these must be done here as these need access various global variables
    """
    globals.activeMineralGold.update()
    globals.activeKollid.update(globals.kollid)
    
## Screen and active window
chunkWidth = int(np.ceil(screenWidth/2/tileSize))
chunkHeight = int(np.ceil(screenHeight/2/tileSize))
chunkWidth = 32
chunkHeight = 32

# size of tile chunks for loading/saving
windowWidth = 3*chunkWidth  # how many tiles loaded into the active window
windowHeight = 3*chunkHeight

coordinates.setup(screenWidth, screenHeight, chunkWidth, chunkHeight, tileSize)
globals.screenBuffer = pg.Surface(size=(windowWidth*tileSize, windowHeight*tileSize))
globals.screenBuffer.fill(bgColor)
spriteBuffer = pg.Surface([windowWidth*tileSize, windowHeight*tileSize], pg.SRCALPHA, 32)
# this is the buffer where movement-related drawing is done,
# afterwards it is copied to the screen
do = True
title = True
dist = 1
up = True
down = True
left = True
right = True
mup = False
mdown = False
mleft = False
mright = False
timer = pg.time.Clock()
lifes = 5
punktid = 0
pause = False
gameover = False
bb = 1
seehome = 1
gmod = 0
gmods = {0:"creative",1:"survival"}
items = {0:0, 1:5, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}
oitems = items
aia = 0
player = pg.sprite.Group()
kutid = pg.sprite.Group()
sprites.setup(tileSize)
globals.kollid = sprites.ChunkSprites()
speed = False
## inventory stuff
inventory = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, -1]
amounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
empty = 0
select = 0
##
s = None
if s is not None:
    world = s['world']
    homeX = s['home'][0]
    homeY = s['home'][1]
    try:
        items = {x[0]:x[1] for x in s["stuff"]}
    except:
        items = {}
    if len(items.keys()) != blocks.BLOCK_END:
        items = oitems
else:
    ## ---------- Build a new world ----------
    ## variables
    globals.ground = world.World(50, 50, 20, 0.5, 2, 1024, 1024, 0)
    ## where Crazy Hat has her home:
    homeX, homeY = 0, 0

## create the active window, centered on home:
chunkID = coordinates.chunkID((homeX, homeY))
globals.mineralGold = sprites.ChunkSprites()
globals.activeWindow = coordinates.activeWindow(windowWidth, windowHeight)
coordinates.coordinateShifts(chunkID, homeX, homeY)
globals.activeWindow.update(globals.ground, chunkID)
# load the world chunks into activeWindow
globals.activeKollid = world.activeSprites(globals.kollid)
# have to initialize this, in principle we may have a few kolls pre-created
globals.activeWindow.draw(None, None, blocks.blocks)
drawSprites(globals.activeMineralGold, spriteBuffer)

class Tüüp(pg.sprite.Sprite):
    def __init__(self,x,y):
        global tileSize
        pg.sprite.Sprite.__init__(self)
        self.image = kutt
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)
    def update(self):
        global tileSize
        if np.random.randint(0,30) == 0:
            self.x += np.random.randint(-1,1)
            self.y += np.random.randint(-1,1)
            self.rect.x, self.rect.y = coordinates.worldToScreenbuffer(self.x, self.y)


def reset():
    """
    reset lifes and score
    """
    global gameover, lifes, punktid, player
    punktid = 0
    gameover = False
    lifes = 5
    player.empty()
    globals.hullmyts = sprites.CrazyHat(homeX, homeY)
    player.add(globals.hullmyts)
    globals.hullmyts.setxy(homeX, homeY)
    
def build(x,y):
    """
    add blocks to the position
    """
    global inventory, select
    winx, winy = coordinates.worldToWindow(x, y)
    if inventory[select] == -1:
        return
    if globals.activeWindow[(winy,winx)] in blocks.breakable:
        return
    globals.activeWindow[(winy,winx)] = inventory[select]
    globals.screenBuffer.blit( blocks.blocks[inventory[select]], coordinates.worldToScreenbuffer(x, y)) 
    amounts[select] -= 1

def destroy(x,y):
    """
    destroy a block and replace it with 'breakto'
    if there is a koll at (x, y), kill it and give 100 points
    x, y: world coordinates
    """
    winx, winy = coordinates.worldToWindow(x, y)
    material = globals.activeWindow[(winy,winx)]
    breakto = blocks.breakto[ material]
    ## if gold and destroyable material
    if np.random.randint(0,200) == 0 and material != breakto:
        globals.mineralGold.add(sprites.Gold(x,y))
    try:
        items[inventory.index(material)] = material
        amounts[inventory.index(material)] += 1
    except:
        items[empty] = material
        amounts[empty] += 1
    inventory[empty] = material
    globals.screenBuffer.blit( blocks.blocks[breakto], coordinates.worldToScreenbuffer(x, y))
    globals.activeWindow[(winy, winx)] = breakto
    killKolls((x, y))

def killKolls(location):
    """
    kill all kolls at (x, y).
    if there is no koll at (x, y), do nothing
    
    location = (x, y), world coordinates
    """
    global punktid
    # punktid: (global) score
    for activeKoll in globals.activeKollid:
        if(activeKoll.getxy() == location):
            globals.kollid.remove([activeKoll])
            globals.activeKollid.remove(activeKoll)
            punktid += 100
            

## initialize player        
reset()

while do:
    ##    while title:
    ##        for event in pg.event.get():
    ##            if event.type == pg.QUIT:
    ##                title = False
    ##                do = False
    ##            elif event.type == pg.KEYDOWN:
    ##                if event.key == pg.K_s:
    ##                    gmod = 1
    ##                    title = False
    ##                elif event.key == pg.K_c:
    ##                    gmod = 0
    ##                    title = False
    ##        score = ("press C for creative mode, press S for survival(WIP)")
    ##        text = tfont.render(score, True, (0,255,0))
    ##        text_rect = text.get_rect()
    ##        text_rect.centerx = screen.get_rect().centerx
    ##        text_rect.y = screenHeight/2
    ##        screen.blit(text,text_rect)
    ##        screen.blit(uwu,(screenWidth/2-f*8,screenHeight/4-f*2))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            ## start with movements: these are by far most common
            if event.key == pg.K_UP:
                mup = True
            elif event.key == pg.K_DOWN:
                mdown = True
            elif event.key == pg.K_LEFT:
                mleft = True
            elif event.key == pg.K_RIGHT:
                mright = True
                ##
            elif event.key == pg.K_a:
                build(globals.hullmyts.getxy()[0]-1, globals.hullmyts.getxy()[1])
            elif event.key == pg.K_s:
                build(globals.hullmyts.getxy()[0], globals.hullmyts.getxy()[1]+1)
            elif event.key == pg.K_d:
                build(globals.hullmyts.getxy()[0]+1, globals.hullmyts.getxy()[1])
            elif event.key == pg.K_w:
                build(globals.hullmyts.getxy()[0], globals.hullmyts.getxy()[1]-1)
            elif event.key == pg.K_j:
                destroy(globals.hullmyts.getxy()[0]-1,globals.hullmyts.getxy()[1])
            elif event.key == pg.K_k:
                destroy(globals.hullmyts.getxy()[0],globals.hullmyts.getxy()[1]+1)
            elif event.key == pg.K_l:
                destroy(globals.hullmyts.getxy()[0]+1,globals.hullmyts.getxy()[1])
            elif event.key == pg.K_i:
                destroy(globals.hullmyts.getxy()[0],globals.hullmyts.getxy()[1]-1)
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                ## go home
                globals.hullmyts.setxy(homeX, homeY)
            elif event.key == pg.K_h:
                homeX = globals.hullmyts.getxy()[0]
                homeY = globals.hullmyts.getxy()[1]
            elif event.key == pg.K_RIGHTBRACKET and bb < blocks.BLOCK_END:
                bb += 1
            elif event.key == pg.K_LEFTBRACKET and bb > 0:
                bb -= 1
            elif event.key == pg.K_x:
                seehome = 1-seehome
            elif event.key == pg.K_z:
                files1.saveWorld(world, (homeX, homeY), items)
            elif event.key == pg.K_c:
                destroy(globals.hullmyts.getxy()[0],globals.hullmyts.getxy()[1])
            elif event.key == pg.K_g:
                gmod = 1-gmod
            elif event.key == pg.K_t:
                title = True
            elif event.key == pg.K_o:
                kutid.add(Tüüp(globals.hullmyts.getxy()[0], globals.hullmyts.getxy()[1]))
            elif event.key == pg.K_LSHIFT:
                speed = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
            elif event.key == pg.K_LSHIFT:
                speed = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mxy = pg.mouse.get_pos()
            tol = tileSize*6
            if event.button == 1 and mxy[0]>screenWidth/2-tol and mxy[0]<screenWidth/2+tol and mxy[1]>screenHeight/2-tol and mxy[1]<screenHeight/2+tol:
                destroy(coordinates.screenToWorld(mxy[0],mxy[1])[0],
                coordinates.screenToWorld(mxy[0],mxy[1])[1])
            elif event.button == 3 and mxy[0]>screenWidth/2-tol and mxy[0]<screenWidth/2+tol and mxy[1]>screenHeight/2-tol and mxy[1]<screenHeight/2+tol:
                build(coordinates.screenToWorld(mxy[0],mxy[1])[0],
                coordinates.screenToWorld(mxy[0],mxy[1])[1])
            elif event.button == 4:
                select -= 1
            elif event.button == 5:
                select += 1
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
                elif event.key == pg.K_r:
                    reset()
        pd = "PAUSIL"
        ptext = dfont.render(pd, True, (127,127,127))
        ptext_rect = ptext.get_rect()
        ptext_rect.centerx = screen.get_rect().centerx
        ptext_rect.y = 50
        screen.blit(ptext,ptext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
    if lifes == 0:
        uded = "SA SURID ÄRA"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
        gameover = True
    while gameover:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    gameover = False
                    reset()
    if np.random.uniform() < kollProbability:
        # create a new monster at a random location inside activeWindow
        winx = np.random.randint(0, globals.activeWindow.getWidth())
        winy = np.random.randint(0, globals.activeWindow.getHeight())
        # add it to the overall monster list
        globals.kollid.add(sprites.Koll(coordinates.windowToWorld(winx, winy)))
        # .. and update the active monsters' list
        globals.activeKollid.empty()
        # have to empty the activeGollid group here to remove the sprites from previous window group
        globals.activeKollid = world.activeSprites(globals.kollid)
    col = pg.sprite.spritecollide(globals.hullmyts, globals.activeMineralGold, False)
    if len(col) > 0:
        globals.activeMineralGold.remove(col)
        globals.mineralGold.remove(col)
        punktid += 100
    col = pg.sprite.spritecollide(globals.hullmyts, globals.activeKollid, False)
    if len(col) > 0 and aia == 0:
        lifes -= 1
        aia = 30
    if aia > 0:
        aia -= 1
    if select < 0:
        select = 9
    if select > 9:
        select = 0
    for s in range(0,10):
        if amounts[s] <= 0:
            inventory[s] = -1
    try:
        empty = inventory.index(-1)
    except:
        empty = 10
    ## ---------- screen udpate ----------
    screen.fill(bgColor)
    screen.blit(globals.screenBuffer, coordinates.blitShift)
    screen.blit(spriteBuffer, coordinates.blitShift)
    ## add score and other info
    pg.draw.rect(screen,(0,0,0),(0,18*tileScale,screenWidth,30))
    score = ("plokk: " + blocks.bn[bb] + "*" + str(items[bb]) +
             ", punktid: " + str(punktid) + " elud: " + str(lifes) +
             "  [x,y: " + str((globals.hullmyts.x, globals.hullmyts.y)) +
             ", chunk: " + str(coordinates.chunkID((globals.hullmyts.x, globals.hullmyts.y))) + "]")
    
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 18*tileScale
    screen.blit(text,text_rect)
    screen.blit(hotbar,(0,0))
    screen.blit(selslot,(select*18*tileScale,0))
    for s in range(0,10):
        screen.blit(blocks.blocks[inventory[s]],(18*tileScale*s+tileScale,tileScale))
        textrender(str(amounts[s]),18*tileScale*s+tileScale, tileScale)
    ## sprite update
    spriteBuffer.fill((0,0,0,0))
    if seehome == 1:
        screen.blit(home, coordinates.worldToScreen(homeX, homeY))
    ## draw sprites: static: no update need, dynamic: update
    drawSprites(globals.activeMineralGold, spriteBuffer)
    kutid.update()
    kutid.draw(spriteBuffer)
    updateScreen()
    drawSprites(globals.activeKollid, spriteBuffer)
    player.update(mup, mdown, mleft, mright)
    player.draw(spriteBuffer)
    ## if you are not speeding
    if not speed:
        mup = False
        mdown = False
        mleft = False
        mright = False
    pg.display.update()
    ##
    timer.tick(60)

pg.quit()
