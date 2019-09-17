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
                    help='world width (tiles)')
parser.add_argument('-y', '--height', type=int, default=64,
                    dest='height',
                    help='world height (tiles)')
args = parser.parse_args()

## ---------- blocks ----------
f=32
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
blocks1.loadBlocks(f)
pic = pg.transform.scale(pg.image.load("pic.png"),(f,f))
kutt = pg.transform.scale(pg.image.load("person.png"),(f,f))
home = pg.transform.scale(pg.image.load("home.png"),(f,f))
kuld = pg.transform.scale(pg.image.load("kuld.png"),(f,f))
koll = pg.transform.scale(pg.image.load("koll.png"),(f,f))
##
bgColor = (64,64,64)
# dark gray
## coordinate transformation for the buffer
def tc(x,y):
    return(x*f, y*f)
## coordnate transformation for the actual screen
def screenCoords(x, y):
    return(sx + x*f, sy + y*f)
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
player = pg.sprite.Group()
kutid = pg.sprite.Group()
kraam = pg.sprite.Group()
##
s = files1.loadWorld()
if s is not None:
    world = s['world']
    homeX = s['home'][0]
    homeY = s['home'][1]
    worldWidth = world.shape[1]
    worldHeight = world.shape[0]
    try:
        print("dfkglaj")
        items = {x[0]:x[1] for x in s["stuff"]}
    except:
        tiems = {}
    if len(items.keys()) != blocks1.BLOCK_END:
        items = oitems
else:
    ## ---------- Build the world ----------
    ## variables
    worldWidth = args.width
    worldHeight = args.height
    #groundLevel = 0.5
    # in fraction, from bottom.  0.3 means bottom 30%
    ## sanity check
##    worldHeight = min(max(worldHeight, 2), 400)
##    worldWidth = min(max(worldWidth, 2), 2000)
##    groundLevel = min(max(groundLevel, 0.0), 1.0)
    world = np.zeros((worldHeight, worldWidth), 'int8')
    noisemap = np.zeros((worldHeight, worldWidth))
    for x in range(worldWidth):
        for y in range(worldHeight):
            noisemap[y,x] = noise.snoise2(x/50, y/50, 20, 0.5, 2, 1024, 1024, 0,)
##    iGround = int((1 - groundLevel)*worldHeight)
##    world[iGround] = 1
##    world[iGround+1:] = 1
    for x in range(worldWidth):
        for y in range(worldHeight):
            if noisemap[y,x] < -0.3:
                world[y,x] = 7
            elif noisemap[y,x] < -0.05:
                world[y,x] = 0
            elif noisemap[y,x] < 0:
                world[y,x] = 1
            elif noisemap[y,x] < 0.3:
                world[y,x] = 2
            elif noisemap[y,x] < 0.4:
                world[y,x] = 3
            elif noisemap[y,x] < 11:
                world[y,x] = 4
    ## where crzy hat has her home:
    homeX = int(worldWidth/2)
    homeY = int(worldHeight/2)
## Draw the world
for x in range(world.shape[0]):
    for y in range(world.shape[1]):
        screenBuffer.blit( blocks1.blocks[ world[x,y] ], tc(y, x))
## ---------- world-screen coordinate translation ----------
## upper left corner of the world will be drawn at (sx, sy) on screen.
## This will be done when copying the screen buffer on screen
sx = screenw/2 - worldWidth*f/2
sy = screenh/2 - worldHeight*f/2
## ---------- world done ----------

class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x, self.rect.y = screenCoords(x, y)
    def update(self, mup, mdown, mleft, mright):
        global sx, sy, world, gmod, f
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
            screenBuffer.blit( blocks1.blocks[blocks1.breakto[world[y,x]]], tc(x, y))
        self.x = x
        self.y = y
        sx = screenw/2-hullmyts.getxy()[0]*f
        sy = screenh/2-hullmyts.getxy()[1]*f
##        self.rect.x, self.rect.y = screenCoords(self.x, self.y)
        self.rect.x = f*x
        self.rect.y = f*y
    def getxy(self):
        return(self.x,self.y)
class Tüüp(pg.sprite.Sprite):
    def __init__(self,x,y):
        global f
        pg.sprite.Sprite.__init__(self)
        self.image = kutt
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x = x*f
        self.rect.y = y*f
    def update(self):
        global f
        if r.randint(0,30) == 0:
            self.x += r.randint(-1,1)
            self.y += r.randint(-1,1)
        self.rect.x = self.x*f
        self.rect.y = self.y*f
class jura(pg.sprite.Sprite):
    def __init__(self,x,y, img=kuld, n=100):
        global f
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x = x*f
        self.rect.y = y*f
        self.n = n
    def update(self):
        pass
for x in range(worldWidth):
        for y in range(worldHeight):
            if r.randint(0,400) == 0:
                kraam.add(jura(x,y))
def reset():
    global hullmyts
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
        screenBuffer.blit( blocks1.blocks[bb], tc(x, y)) 
def destroy(x,y):
    if x>=0 and y>=0 and x<worldWidth and y<worldHeight:
        if r.randint(0,200) == 0 and world[y,x] != blocks1.breakto[world[y,x]]:
            kraam.add(jura(x,y))
        items[world[y,x]] += 1
        screenBuffer.blit( blocks1.blocks[blocks1.breakto[world[y,x]]], tc(x, y))
        world[y,x] = blocks1.breakto[world[y,x]]
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
                reset()
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
                    pd = "PAUSED"
                    ptext = dfont.render(pd, True, (127,127,127))
                    ptext_rect = ptext.get_rect()
                    ptext_rect.centerx = screen.get_rect().centerx
                    ptext_rect.y = 50
                    screen.blit(ptext,ptext_rect)
                    screen.blit(text,text_rect)
                    pg.display.update()
    if lifes == 0:
        uded = "GAME OVER"
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
    col = pg.sprite.spritecollide(hullmyts,kraam,False)
    if len(col) > 0:
        kraam.remove(col)
        punktid += 100
                    ## ---------- screen udpate ----------
    screen.fill(bgColor)
    screen.blit(screenBuffer, (sx,sy))
    screen.blit(m8Buffer, (sx,sy))
    m8Buffer.fill((0,0,0,0))
    if seehome == 1:
        screen.blit(home, screenCoords(homeX,homeY))
    pg.draw.rect(screen,(0,0,0),(0,10,screenw,30))
    score = ("plokk: " + blocks1.bn[bb] + "*" + str(items[bb]) +
             ", punktid: " + str(punktid))
    if len(kraam) == 0:
        score += " (kõik)"
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(m8Buffer)
    kutid.update()
    kutid.draw(m8Buffer)
    kraam.draw(m8Buffer)
    pg.display.update()
    ##
    mup = False
    mdown = False
    mleft = False
    mright = False
    timer.tick(60)

pg.quit()
