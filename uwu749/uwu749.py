#!/usr/bin/env python3
import argparse
import pygame as pg
import numpy as np
import sys
import subprocess
import time
import noise

import blocks
import coordinates
import files
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
kollProbability = 0.005   #default is 0.005
#kollProbability = 0.0

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

def textrender(text, x, y, font=font):
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
title = True  # start with main menu?
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
punktid = 0
pause = False
gameover = False
bb = 1
seehome = 1
gmod = 0
gmods = {0:"creative",1:"survival"}
gameState = globals.GameState()  # current running game data

def newGame(terrain=None, state=None):
    """
    Re-create everything, including terrain, monsters
    reset lives, score, inventory
    """
    global gameState
    ## global params
    if terrain is None:
        globals.ground = world.World(globals.groundNoiseParams)
    else:
        globals.ground = terrain
    globals.activeWindow = coordinates.activeWindow(windowWidth, windowHeight)
    ## create the active window, centered at 0,0 as we don't
    ## have the CH coordinates yet:
    chunkID = coordinates.chunkID((0, 0))
    globals.mineralGold = sprites.ChunkSprites()
    coordinates.coordinateShifts(chunkID, gameState.homeX, gameState.homeY)
    globals.activeWindow.update(globals.ground, chunkID)
    # load the world chunks into activeWindow
    globals.activeKollid = world.activeSprites(globals.kollid)
    # have to initialize this, in principle we may have a few kolls pre-created
    globals.activeWindow.draw(None, None, blocks.blocks)
    drawSprites(globals.activeMineralGold, spriteBuffer)
    ## set the game state first: we have to know the initial location
    reset()
    if state is not None:
        gameState = state

def reset():
    """
    reset lives, score etc to the original state
    leave the world geography untouched
    """
    global gameState, gameover, aia
    gameState = globals.GameState()
    gameover = False
    aia = 0
    # counter for immunity: after a monster hits you, you will be immune
    # agains new hits for this many ticks.
    globals.player.empty()
    globals.hullmyts = sprites.CrazyHat(gameState.homeX, gameState.homeY)
    globals.player.add(globals.hullmyts)
    globals.hullmyts.setxy(gameState.homeX, gameState.homeY)

kollin = 0  # how many mosters
kutid = pg.sprite.Group()
sprites.setup(tileSize)
globals.kollid = sprites.ChunkSprites()
speed = False
empty = 0
select = 0
##

newGame()


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
    
def build(x,y):
    """
    add blocks to the position
    """
    winx, winy = coordinates.worldToWindow(x, y)
    if gameState.inventory[select] == -1:
        return
    if blocks.breakto[gameState.inventory[select]] != globals.activeWindow[(winy,winx)]:
        return
    globals.activeWindow[(winy,winx)] = gameState.inventory[select]
    globals.screenBuffer.blit( blocks.blocks[gameState.inventory[select]], coordinates.worldToScreenbuffer(x, y)) 
    gameState.amounts[select] -= 1

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
    killKolls((x, y))
    if globals.activeWindow[(winy,winx)] in blocks.unbreakable:
        return
    try:
        gameState.amounts[gameState.inventory.index(material)] += 0
    except:
        if empty == 10:
            return
    if np.random.randint(0,200) == 0 and material != breakto:
        globals.mineralGold.add(sprites.Gold(x,y))
        globals.activeMineralGold = world.activeSprites(globals.mineralGold)
    get(blocks.drops[material])
    globals.screenBuffer.blit( blocks.blocks[breakto], coordinates.worldToScreenbuffer(x, y))
    globals.activeWindow[(winy, winx)] = breakto
    

def killKolls(location):
    """
    kill all kolls at (x, y).
    if there is no koll at (x, y), do nothing
    
    location = (x, y), world coordinates
    """
    global gameState, kollin
    for activeKoll in globals.activeKollid:
        if(activeKoll.getxy() == location):
            globals.kollid.remove([activeKoll])
            globals.activeKollid.remove(activeKoll)
            gameState.punktid += 100
            kollin -= 1
            gameState.kollivaremed += 1

def get(item, cost=blocks.NONE):
    try:
        gameState.amounts[gameState.inventory.index(cost)] -= 1
        if cost == blocks.NONE:
            gameState.amounts[gameState.inventory.index(cost)] += 1
    except:
        if empty == 10:
            return
    try:
        gameState.inventory[gameState.inventory.index(item)] = item
        gameState.amounts[gameState.inventory.index(item)] += 1
    except:
        gameState.inventory[empty] = item
        gameState.amounts[empty] += 1
## initialize player        
reset()

while do:
    while title:
        ## main menu
        for event in pg.event.get():
            if event.type == pg.QUIT:
                title = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_l:
                    terrain, gameState = files.loadWorld()
                    newGame(terrain, gameState)
                    title = False
                elif event.key == pg.K_s:
                    globals.activeWindow.update(globals.ground,
                                                (coordinates.chunkID(globals.hullmyts.getxy())))
                    # sync data
                    files.saveWorld(globals.ground, gameState)
                    title = False
                elif event.key == pg.K_c:
                    newGame()
                    title = False
        textrender("press C to create new world, L to load world from file, S to save",
                   screenWidth/2, screenHeight/2)
        pg.display.update()
        timer.tick(5)  # low fps enough for the main menu
    for event in pg.event.get():
        ## main game loop
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
                globals.hullmyts.setxy(gameState.homeX, gameState.homeY)
            elif event.key == pg.K_h:
                gameState.homeX = globals.hullmyts.getxy()[0]
                gameState.homeY = globals.hullmyts.getxy()[1]
            elif event.key == pg.K_RIGHTBRACKET and bb < blocks.BLOCK_END:
                bb += 1
            elif event.key == pg.K_LEFTBRACKET and bb > 0:
                bb -= 1
            elif event.key == pg.K_x:
                seehome = 1-seehome
            elif event.key == pg.K_c:
                destroy(globals.hullmyts.getxy()[0],globals.hullmyts.getxy()[1])
            elif event.key == pg.K_g:
                gmod = 1-gmod
            elif event.key == pg.K_t:
                title = True
            elif event.key == pg.K_o:
                kutid.add(Tüüp(globals.hullmyts.getxy()[0], globals.hullmyts.getxy()[1]))
            elif event.key == pg.K_RSHIFT:
                speed = True
            elif event.key == pg.K_y:
                # go to the main menu
                title = True;
            elif event.key == pg.K_PERIOD:
                if gameState.inventory[select] == blocks.PUIT:
                    get(blocks.KAST,blocks.PUIT)
                elif gameState.inventory[select] == blocks.KAST:
                    get(blocks.KUKS,blocks.KAST)
                elif gameState.inventory[select] == blocks.MURU:
                    get(blocks.TEE,blocks.MURU)
                elif gameState.inventory[select] == blocks.PUU:
                    get(blocks.PUIT,blocks.PUU)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
            elif event.key == pg.K_RSHIFT:
                speed = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mxy = pg.mouse.get_pos()
            hxy = globals.hullmyts.getxy()
            tol = tileSize*6
            if event.button == 1 and mxy[0]>screenWidth/2-tol and mxy[0]<screenWidth/2+tol and mxy[1]>screenHeight/2-tol and mxy[1]<screenHeight/2+tol:
                destroy(coordinates.screenToWorld(mxy[0],mxy[1])[0],
                coordinates.screenToWorld(mxy[0],mxy[1])[1])
            elif event.button == 3:
                if mxy[0]>screenWidth/2-tol and mxy[0]<screenWidth/2+tol and mxy[1]>screenHeight/2-tol and mxy[1]<screenHeight/2+tol:
                    mxw = coordinates.screenToWorld(mxy[0],mxy[1])[0]
                    myw = coordinates.screenToWorld(mxy[0],mxy[1])[1]
                    build(mxw, myw)
                    winx, winy = coordinates.worldToWindow(mxw, myw)
                    if globals.activeWindow[winy, winx] == blocks.KUKS:
                        globals.activeWindow[winy, winx] = blocks.LUKS
                        globals.screenBuffer.blit(blocks.blocks[blocks.LUKS], coordinates.windowToScreenBuffer(winx, winy))  
                    elif globals.activeWindow[winy, winx] == blocks.LUKS:
                        globals.activeWindow[winy, winx] = blocks.KUKS
                        globals.screenBuffer.blit(blocks.blocks[blocks.KUKS], coordinates.windowToScreenBuffer(winx, winy)) 
                if gameState.inventory[select] == blocks.MQQK:
                    for x in range(-3,4):
                        for y in range(-3,4):
                            killKolls((hxy[0]+x, hxy[1]+y))
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
        timer.tick(10)
    if gameState.lifes == 0:
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
        timer.tick(10)
    if np.random.uniform() < kollProbability and len(globals.activeKollid)<=12:
        kollin += 1
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
        gameState.punktid += 100
        gameState.kuld += 1
    col = pg.sprite.spritecollide(globals.hullmyts, globals.activeKollid, False)
    if len(col) > 0 and aia == 0:
        gameState.lifes -= 1
        aia = 30
    if aia > 0:
        aia -= 1
    if select < 0:
        select = 9
    if select > 9:
        select = 0
    if gameState.kuld >= 10 and empty != 10:
        gameState.kuld -= 10
        get(blocks.KULD)
    if gameState.kollivaremed >= 10 and empty != 10:
        gameState.kollivaremed -= 10
        get(blocks.KOLLIV)
    
    for s in range(0,10):
        if gameState.amounts[s] <= 0:
            gameState.inventory[s] = -1
        if gameState.inventory[s] == -1:
            gameState.amounts[s] = 0
    try:
        empty = gameState.inventory.index(-1)
    except:
        empty = 10
    ## ---------- screen udpate ----------
    screen.blit(globals.screenBuffer, coordinates.blitShift)
    ## add score and other info
    pg.draw.rect(screen,(0,0,0),(0,18*tileScale,screenWidth,30))
    score = ("punktid: " + str(gameState.punktid) + " elud: " + str(gameState.lifes) +
             " Kuld:" + str(gameState.kuld) + " Kolli varemed:" + str(gameState.kollivaremed))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 18*tileScale
    screen.blit(text,text_rect)
    screen.blit(hotbar,(0,0))
    screen.blit(selslot,(select*18*tileScale,0))
    for s in range(0,10):
        screen.blit(blocks.blocks[gameState.inventory[s]],(18*tileScale*s+tileScale,tileScale))
        textrender(str(gameState.amounts[s]),18*tileScale*s+tileScale, tileSize)
    ## sprite update
    globals.player.update(mup, mdown, mleft, mright)
    # update crazy hat
    spriteBuffer.fill((0,0,0,0))
    if seehome == 1:
        screen.blit(home, coordinates.worldToScreen(gameState.homeX, gameState.homeY))
    ## draw sprites: static: no update need, dynamic: update
    drawSprites(globals.activeMineralGold, spriteBuffer)
    kutid.update()
    kutid.draw(spriteBuffer)
    updateScreen()
    drawSprites(globals.activeKollid, spriteBuffer)
    globals.player.draw(spriteBuffer)
    # add sprites to spritebuffer.  this will be blitted
    # to the screen in the next loop
    screen.blit(spriteBuffer, coordinates.blitShift)
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
print("lendan õhku")
