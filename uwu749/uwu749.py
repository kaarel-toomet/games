#!/usr/bin/env python3
import argparse
import pygame as pg
import random as r
import numpy as np
import sys
import subprocess
import noise

import blocks1
import files1

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

## ---------- blocks ----------
tileSize = 32
# block size on screen
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
        screenw = int(wh[0])
        screenh = int(wh[1])
        screen = pg.display.set_mode((screenw, screenh), pg.RESIZABLE)
        xdotool = True
if not xdotool:
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    screenw, screenh = pg.display.get_surface().get_size()
pg.display.set_caption(str(r.randint(0,9000)))
pg.mixer.init()
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()

## load config and all that
blocks1.loadBlocks(tileSize)
pic = pg.transform.scale(pg.image.load("pic.png"),(tileSize, tileSize))
kutt = pg.transform.scale(pg.image.load("person.png"),(tileSize, tileSize))
home = pg.transform.scale(pg.image.load("home.png"),(tileSize, tileSize))
kuld = pg.transform.scale(pg.image.load("kuld.png"),(tileSize, tileSize))
koll = pg.transform.scale(pg.image.load("koll.png"),(tileSize, tileSize))
##
bgColor = (64,64,64)
# dark gray

## ---------- coordinate translation ----------
## the game contains 3 types of coordinates:
## * screen coordinates in pixels, (0,0) is top left
## * active window coordinates in tiles, (0,0) is top left (the same thing as screenBuffer)
## * world coordinates, in tiles, potentially unlimited, (0,0) is center (TBD)
##
## translation is mainly done using tuples (sx, sx) to shift to screen coords,
## and (wx, wx) to screenBuffer coords.

## Screen and active window
chunkSize = 32
# size of tiles chunks for loading/saving
windowWidth = 3*chunkSize  # how many tiles loaded into the active window
windowHeight = 3*chunkSize

def coordinateShifts(iChunk, jChunk, cx, cy):
    """
    compute the coordinate shifts b/w coordinates
    shifts should be added to the world coordinates to make the translation
    INPUTS: 
    iChunk, jChunk: central chunk of the active window
    cx, cy: screen center world coordinates 
            normally location of Crazy Hat
    RETURNS:
    (ssx, ssy, wsx, wsy)
    wx, wy: shift b/w world and window coordinates
    """
    wsx = (iChunk - 1)*chunkSize
    wsy = (jChunk - 1)*chunkSize
    ssx = screenw/2 - (cx + wsx)*tileSize
    ssy = screenh/2 - (cy + wsy)*tileSize
    return (ssx, ssy, wsx, wsy)

def windowCoords(x,y):
    """
    transform world coordinates to screenBuffer coordinates
    x, y: world coordinates
    returns:
    (bx, by): screen buffer coordinates
    """
    return(wsx + x*tileSize, wsy + y*tileSize)

def screenCoords(x, y):
    """
    transform world coordinates to screen coordinates
    x, y: world coordinates
    returns:
    (ex, ey): screen coordinates
    """
    return(ssx + x*tileSize, ssy + y*tileSize)
##

screenBuffer = pg.Surface(size=(4*screenw, 4*screenh))
screenBuffer.fill(bgColor)
m8Buffer = pg.Surface([4*screenw, 4*screenh], pg.SRCALPHA, 32)
# this is the buffer where movement-related drawing is done,
# afterwards it is copied to the screen
do = True
title = True
dist = 1
actuallyuselessvariable = 39
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
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
tfont = pg.font.SysFont("Times",100)
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
kraam = pg.sprite.Group()
kollid = pg.sprite.Group()

##
s = files1.loadWorld()
if s is not None:
    world = s['world']
    homeX = s['home'][0]
    homeY = s['home'][1]
    worldWidth = world.shape[1]
    worldHeight = world.shape[0]
    try:
        items = {x[0]:x[1] for x in s["stuff"]}
    except:
        items = {}
    if len(items.keys()) != blocks1.BLOCK_END:
        items = oitems
else:
    ## ---------- Build the world ----------
    ## variables
    worldWidth = 1024
    worldHeight = 1024
    #groundLevel = 0.5
    # in fraction, from bottom.  0.3 means bottom 30%
    ## sanity check
    print("creating the world..", end="")
    world = np.empty((worldHeight, worldWidth), 'int8')
    freq = 16.0
    for x in range(worldWidth):
        for y in range(worldHeight):
            noiseval = noise.snoise2(x/50, y/50, 20, 0.5, 2, 1024, 1024, 0,)
            if noiseval < -0.3:
                world[y,x] = 7
            elif noiseval < -0.05:
                world[y,x] = 0
            elif noiseval < 0:
                world[y,x] = 1
            elif noiseval < 0.3:
                world[y,x] = 2
            elif noiseval < 0.4:
                world[y,x] = 3
            elif noiseval < 11:
                world[y,x] = 4
    print("done")
    ## where Crazy Hat has her home:
    homeX = int(worldWidth/2)
    homeY = int(worldHeight/2)

## create the active window, centered on home:
worldWidthChunks = worldWidth/chunkSize
worldHeightChunks = worldHeight/chunkSize
iChunk = homeX % chunkSize
jChunk = homeY % chunkSize
activeWindow = np.empty((windowWidth, windowHeight), 'int8')
for i, ic in enumerate([iChunk-1, iChunk, iChunk+1]):
    for j, jc in enumerate([jChunk-1, jChunk, jChunk+1]):
        if 0 <= ic < worldWidthChunks and 0 <= jc < worldHeightChunks:
            # we are in the middle of the world
            activeWindow[j*chunkSize:(j+1)*chunkSize,i*chunkSize:(i+1)*chunkSize] =\
            world[iChunk*chunkSize:(iChunk+1)*chunkSize, jChunk*chunkSize:(jChunk+1)*chunkSize].copy()
        else:
            # this chunk is outside of the world
            activeWindow[j*chunkSize:(j+1)*chunkSize,i*chunkSize:(i+1)*chunkSize] = 0

## Draw the world
for x in range(activeWindow.shape[0]):
    for y in range(activeWindow.shape[1]):
        screenBuffer.blit( blocks1.blocks[ activeWindow[x,y] ], windowCoords(y, x))

class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x, self.rect.y = screenCoords(x, y)
    def update(self, mup, mdown, mleft, mright):
        global ssx, ssy, wsx, wsy
        global world, gmod, f
        y = self.y
        x = self.x
##        if world[y,x] == blocks1.SKY and gmod == 1:
##            mup = False
##            if world[y+1,x] == blocks1.SKY:
##                mdown = True
        if mup:
            y = max(self.y - 1, 0)
        if mdown:
            y = min(self.y + 1, worldHeight - 1)
        if mleft:
            x = max(self.x - 1, 0)
        if mright:
            x = min(self.x + 1, worldWidth - 1)
        if world[y,x] in blocks1.solid:
            return
        if world[y,x] in blocks1.breakable:
            world[y,x] = blocks1.breakto[world[y,x]]
            screenBuffer.blit( blocks1.blocks[blocks1.breakto[world[y,x]]], windowCoords(x, y))
        self.x = x
        self.y = y
        ssx, ssy, wsx, wsy = coordinateShifts(iChunk, jChunk, hullmyts.getxy()[0], hullmyts.getxy()[1])
        self.rect.x = tileSize*x
        self.rect.y = tileSize*y
    def getxy(self):
        return(self.x,self.y)
    def setxy(self,x,y):
        self.x = x
        self.y = y
        self.rect.x = x*tileSize
        self.rect.y = y*tileSize
class Tüüp(pg.sprite.Sprite):
    def __init__(self,x,y):
        global tileSize
        pg.sprite.Sprite.__init__(self)
        self.image = kutt
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x = x*tileSize
        self.rect.y = y*tileSize
    def update(self):
        global tileSize
        if r.randint(0,30) == 0:
            self.x += r.randint(-1,1)
            self.y += r.randint(-1,1)
        self.rect.x = self.x*tileSize
        self.rect.y = self.y*tileSize
class Koll(pg.sprite.Sprite):
    def __init__(self,x,y):
        global f
        pg.sprite.Sprite.__init__(self)
        self.image = koll
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x = x*tileSize
        self.rect.y = y*tileSize
    def update(self):
        global f, hullmyts
        if r.randint(0,30) == 0:
            xy = hullmyts.getxy()
            if xy[0] < self.x:
                self.x -= 1
            if xy[0] > self.x:
                self.x += 1
            if xy[1] < self.y:
                self.y -= 1
            if xy[1] > self.y:
                self.y += 1
        self.rect.x = self.x*tileSize
        self.rect.y = self.y*tileSize
    def lammutus(self,x,y):
        global punktid
        if self.x == x and self.y == y:
            kollid.remove(self)
            punktid += 100
class jura(pg.sprite.Sprite):
    def __init__(self,x,y, img=kuld, n=100):
        global tileSize
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x = x*tileSize
        self.rect.y = y*tileSize
        self.n = n
    def update(self):
        pass
for x in range(worldWidth):
        for y in range(worldHeight):
            if r.randint(0,400) == 0:
                kraam.add(jura(x,y))
##            if r.randint(0,400) == 0:
##                kollid.add(Koll(x,y))
def reset():
    global hullmyts, gameover, lifes, punktid
    punktid = 0
    gameover = False
    lifes = 5
    player.empty()
    hullmyts = Player(homeX, homeY)
    player.add(hullmyts)
def build(x,y):
    global bb
    if x>=0 and y>=0 and x<worldWidth and y<worldHeight:
        if world[y,x] in blocks1.breakable:
            return
        if gmod == 1:
            if items[bb] <= 0:
                return
            items[bb] -= 1
        world[y,x] = bb
        screenBuffer.blit( blocks1.blocks[bb], windowCoords(x, y)) 
def destroy(x,y):
    if x>=0 and y>=0 and x<worldWidth and y<worldHeight:
        if r.randint(0,200) == 0 and world[y,x] != blocks1.breakto[world[y,x]]:
            kraam.add(jura(x,y))
        items[world[y,x]] += 1
        screenBuffer.blit( blocks1.blocks[blocks1.breakto[world[y,x]]], windowCoords(x, y))
        world[y,x] = blocks1.breakto[world[y,x]]
    for k in kollid:
        k.lammutus(x,y)
# initialize player        
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
##        text_rect.y = screenh/2
##        screen.blit(text,text_rect)
##        screen.blit(uwu,(screenw/2-f*8,screenh/4-f*2))
##        pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                build(hullmyts.getxy()[0]-1,hullmyts.getxy()[1])
            elif event.key == pg.K_s:
                build(hullmyts.getxy()[0],hullmyts.getxy()[1]+1)
            elif event.key == pg.K_d:
                build(hullmyts.getxy()[0]+1,hullmyts.getxy()[1])
            elif event.key == pg.K_w:
                build(hullmyts.getxy()[0],hullmyts.getxy()[1]-1)
            elif event.key == pg.K_j:
                destroy(hullmyts.getxy()[0]-1,hullmyts.getxy()[1])
            elif event.key == pg.K_k:
                destroy(hullmyts.getxy()[0],hullmyts.getxy()[1]+1)
            elif event.key == pg.K_l:
                destroy(hullmyts.getxy()[0]+1,hullmyts.getxy()[1])
            elif event.key == pg.K_i:
                destroy(hullmyts.getxy()[0],hullmyts.getxy()[1]-1)
            elif event.key == pg.K_UP:
                mup = True  #useless comment
            elif event.key == pg.K_DOWN:
                mdown = True
            elif event.key == pg.K_LEFT:
                mleft = True
            elif event.key == pg.K_RIGHT:
                mright = True
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                hullmyts.setxy(homeX,homeY)
            elif event.key == pg.K_h:
                homeX = hullmyts.getxy()[0]
                homeY = hullmyts.getxy()[1]
            elif event.key == pg.K_RIGHTBRACKET and bb < blocks1.BLOCK_END:
                bb += 1
            elif event.key == pg.K_LEFTBRACKET and bb > 0:
                bb -= 1
            elif event.key == pg.K_x:
                seehome = 1-seehome
            elif event.key == pg.K_z:
                files1.saveWorld(world, (homeX, homeY), items)
            elif event.key == pg.K_c:
                destroy(hullmyts.getxy()[0],hullmyts.getxy()[1])
            elif event.key == pg.K_g:
                gmod = 1-gmod
            elif event.key == pg.K_t:
                title = True
            elif event.key == pg.K_o:
                kutid.add(Tüüp(hullmyts.getxy()[0],hullmyts.getxy()[1]))
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
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
    if r.randint(0,400) == 0:
        kollid.add(Koll(r.randint(0,worldWidth),r.randint(0,worldHeight)))
    col = pg.sprite.spritecollide(hullmyts,kraam,False)
    if len(col) > 0:
        kraam.remove(col)
        punktid += 100
    col = pg.sprite.spritecollide(hullmyts,kollid,False)
    if len(col) > 0 and aia == 0:
        lifes -= 1
        aia = 30
    if aia > 0:
        aia -= 1
    ## ---------- screen udpate ----------
    screen.fill(bgColor)
    screen.blit(screenBuffer, (ssx,ssy))
    screen.blit(m8Buffer, (ssx,ssy))
    m8Buffer.fill((0,0,0,0))
    if seehome == 1:
        screen.blit(home, screenCoords(homeX, homeY))
    pg.draw.rect(screen,(0,0,0),(0,10,screenw,30))
    score = ("plokk: " + blocks1.bn[bb] + "*" + str(items[bb]) +
             ", punktid: " + str(punktid) + " elud: " + str(lifes))
    if len(kraam) == 0:
        score += " (kõik maas kuld korjatud)"
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    ## ---------- player update ----------
    player.update(mup,mdown, mleft, mright)
    player.draw(m8Buffer)
    kutid.update()
    kutid.draw(m8Buffer)
    kollid.update()
    kollid.draw(m8Buffer)
    kraam.draw(m8Buffer)
    pg.display.update()
    ##
    mup = False
    mdown = False
    mleft = False
    mright = False
    timer.tick(60)

pg.quit()
