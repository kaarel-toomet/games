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
kollProbability = 0.002   #default is 0.002
# kollProbability = 0.0

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
        globals.screenWidth = int(wh[0])
        globals.screenHeight = int(wh[1])
        globals.screen = pg.display.set_mode((globals.screenWidth, globals.screenHeight), pg.RESIZABLE)
        xdotool = True
if not xdotool:
    globals.screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    globals.screenWidth, globals.screenHeight = pg.display.get_surface().get_size()
    pg.display.set_caption(str(np.random.randint(0,9000)))
    pg.mixer.init()
    globals.screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    globals.screenWidth = globals.screen.get_width()
    globals.screenHeight = globals.screen.get_height()


## load config and all that
blocks.loadBlocks(tileSize)
kutt = pg.transform.scale(pg.image.load("person.png"),(tileSize, tileSize))
home = pg.transform.scale(pg.image.load("home.png"),(tileSize, tileSize))
hotbar = pg.transform.scale(pg.image.load("hotbar.png"),(360*tileScale, 18*tileScale))
selslot = pg.transform.scale(pg.image.load("selslot.png"),(18*tileScale, 18*tileScale))
##
bgColor = (64,64,64)
# dark gray

font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
tfont = pg.font.SysFont("Times",100)

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
chunkWidth = int(np.ceil(globals.screenWidth/2/tileSize))
chunkHeight = int(np.ceil(globals.screenHeight/2/tileSize))
chunkWidth = 32
chunkHeight = 32

# size of tile chunks for loading/saving
windowWidth = 3*chunkWidth  # how many tiles loaded into the active window
windowHeight = 3*chunkHeight

coordinates.setup(globals.screenWidth, globals.screenHeight, chunkWidth, chunkHeight, tileSize)
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
globals.gameState = globals.GameState()  # current running game data

def newGame(terrain=None, underterrain = None,
            spriteData=None,
            state=None, crazyHat=None):
    """
    Re-create everything, including terrain, monsters
    reset lives, score, inventory
    """
    globals.mineralGold = sprites.ChunkSprites()
    ## global params
    if terrain is None:
        globals.ground = world.World("ground", globals.groundNoiseParams)
    else:
        globals.ground = terrain
    if underterrain is None:
        globals.underground = world.World("underground",globals.undergroundNoiseParams)
    else:
        globals.underground = underterrain
    globals.activelayer = globals.ground
    globals.activeWindow = coordinates.ActiveWindow(globals.activelayer,
                                                    windowWidth, windowHeight)
    ## create the active window, centered at 0,0 as we don't
    ## have the CH coordinates yet:
    chunkID = coordinates.chunkID((0, 0))
    coordinates.coordinateShifts(chunkID, globals.gameState.home[0], globals.gameState.home[1])
    globals.activeWindow.update(chunkID)
    # load the world chunks into activeWindow
    globals.activeWindow.draw(None, None, blocks.blocks)  # arguments: dx, dy, blocks
    drawSprites(globals.activeMineralGold, spriteBuffer)
    ## set the game state first: we have to know the initial location
    reset(crazyHat)
    ## sprites: 
    if spriteData is not None:
        ## walk through the sprites dict and see what's there
        if "kollid" in spriteData:
            globals.kollid = spriteData["kollid"]
        else:
            globals.kollid = sprites.ChunkSprites()
        if "gold" in spriteData:
            globals.mineralGold = spriteData["gold"]
        else:
            globals.kollid = sprites.ChunkSprites()
    globals.activeKollid = world.activeSprites(globals.kollid)
    globals.activeMineralGold = world.activeSprites(globals.mineralGold)
    # have to initialize this, in principle we may have a few kolls pre-created
    if state is not None:
        globals.gameState = state

def reset(crazyHat=None):
    """
    reset lives, score etc to the original state
    leave the world geography untouched
    """
    global gameover, aia
    gameover = False
    aia = 0
    # counter for immunity: after a monster hits you, you will be immune
    # agains new hits for this many ticks.
    globals.player.empty()
    if crazyHat is None:
        globals.hullmyts = sprites.CrazyHat(globals.gameState.home)
        globals.hullmyts.setxy(globals.gameState.home)
    else:
        globals.hullmyts = crazyHat
    globals.player.add(globals.hullmyts)
    ## remove existing monsters
    globals.kollid = sprites.ChunkSprites()

sprites.setup(tileSize)
speed = False
empty = 0
select = 0
##

newGame()
    
def build(x,y):
    """
    add blocks to the position
    """
    winx, winy = coordinates.worldToWindow(x, y)
    if globals.gameState.inventory[select] == -1:
        return
    if blocks.breakto[globals.gameState.inventory[select]] != globals.activeWindow[(winy,winx)]:
        return
    globals.activeWindow[(winy,winx)] = globals.gameState.inventory[select]
    globals.screenBuffer.blit( blocks.blocks[globals.gameState.inventory[select]], coordinates.worldToScreenbuffer(x, y)) 
    globals.gameState.amounts[select] -= 1

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
    if material not in globals.gameState.inventory and empty == 20:
        return
    if np.random.randint(0,200) == 0 and material != breakto:
        # there was a gold hidden underneath this block
        globals.mineralGold.add(sprites.Gold((x,y)))
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
    for activeKoll in globals.activeKollid:
        if(activeKoll.getxy() == location):
            globals.kollid.remove([activeKoll])
            globals.activeKollid.remove(activeKoll)
            globals.gameState.punktid += 100
            globals.gameState.kollivaremed += 1

def activate(location, act = 0):
    block = globals.activeWindow[location]
    if block == blocks.KUKS and act > -1:
        block = blocks.LUKS
    elif block == blocks.LUKS and act < 1:
        block = blocks.KUKS
    elif block == blocks.ACT and act > -1:
        block = blocks.AACT
        globals.activeWindow[location] = block
        for x in range(-1,2):
            for y in range(-1,2):
                if globals.activeWindow[(location[0]+x,location[1]+y)] != blocks.AACT:
                    activate((location[0]+x,location[1]+y), 1)
    elif block == blocks.AACT and act < 1:
        block = blocks.ACT
        globals.activeWindow[location] = block
        for x in range(-1,2):
                for y in range(-1,2):
                    if globals.activeWindow[(location[0]+x,location[1]+y)] != blocks.ACT:
                        activate((location[0]+x,location[1]+y),-1)
    elif block == blocks.LAMMUTI and act > -1:
        wxy = coordinates.windowToWorld(location[1], location[0])
        x = wxy[0]
        y = wxy[1]
        destroy(x+1,y)
        destroy(x-1,y)
        destroy(x,y+1)
        destroy(x,y-1)
    globals.activeWindow[location] = block
    globals.screenBuffer.blit(blocks.blocks[block], coordinates.windowToScreenBuffer((location[1],location[0])))

def get(item, n = 1):
    global inventory, amounts, empty
    try:
        empty = globals.gameState.inventory.index(-1)
    except:
        empty = 20
    exists = item in globals.gameState.inventory
    if exists:
        globals.gameState.amounts[gameState.inventory.index(item)] += n
    elif empty <= 20:
        globals.gameState.inventory[empty] = item
        globals.gameState.amounts[empty] = n
    else:
        return
def lose(item, n = 1):
    global inventory, amounts, empty
    exists = item in globals.gameState.inventory
    if exists:
        if globals.gameState.amounts[globals.gameState.inventory.index(item)] >= n:
            globals.gameState.amounts[globals.gameState.inventory.index(item)] -= n
    else:
        return
## initialize player        
reset()

while do:
    #get(blocks.AACT,2)
    while title:
        ## main menu
        for event in pg.event.get():
            if event.type == pg.QUIT:
                title = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_l:
                    ## load world
                    try:
                        l = files.loadWorld()
                    except:
                        l = None
                    if l is not None:
                        ## did not cancel
                        ground, underground, spriteData, gameState, crazyHat = l
                        newGame(ground, underground, spriteData,
                                gameState, crazyHat)
                        if gameState.dimension == "ground":
                            globals.activelayer = globals.ground
                        else:
                            globals.activelayer = globals.underground
                        globals.activeWindow.switchLayer(globals.activelayer)
                        globals.activeWindow.draw(0, 0, blocks.blocks)  # arguments: dx, dy, blocks
                    else:
                        newGame()
                    title = False
                elif event.key == pg.K_s:
                    globals.activeWindow.update(coordinates.chunkID(globals.hullmyts.getxy()))
                    # sync data
                    ## sprites
                    spriteData = {
                        "kollid" : globals.kollid.dictify(),
                        "gold" : globals.mineralGold.dictify()
                    }
                    files.saveWorld(globals.ground, globals.underground,
                                    spriteData,
                                    globals.gameState,
                                    globals.hullmyts)
                    title = False
                elif event.key == pg.K_c:
                    title = False
        globals.textrender("press C to cancel, L to load world from file, S to save",
                   globals.screenWidth/2 - 200, globals.screenHeight/2)
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
                globals.hullmyts.setxy(globals.gameState.home)
            elif event.key == pg.K_h:
                globals.gameState.home = globals.hullmyts.getxy()
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
            elif event.key == 13:
                if globals.activeWindow[coordinates.worldToWindow(globals.hullmyts.getxy()[0],globals.hullmyts.getxy()[1])[1],coordinates.worldToWindow(globals.hullmyts.getxy()[0],globals.hullmyts.getxy()[1])[0]] == blocks.AUK:
                    if globals.activelayer is globals.ground:
                        globals.activelayer = globals.underground
                    else:
                        globals.activelayer = globals.ground
                    globals.gameState.dimension = globals.activelayer.dimension
                    globals.activeWindow.switchLayer(globals.activelayer)
                    globals.activeWindow.draw(0, 0, blocks.blocks)  # arguments: dx, dy, blocks
            elif event.key == pg.K_RSHIFT:
                speed = True
            elif event.key == pg.K_y:
                # go to the main menu
                title = True
            elif event.key == pg.K_PERIOD:
                if globals.gameState.inventory[select] == blocks.PUIT:
                    get(blocks.KAST)
                    lose(blocks.PUIT)
                elif globals.gameState.inventory[select] == blocks.KAST:
                    get(blocks.KUKS)
                    lose(blocks.KAST)
                elif globals.gameState.inventory[select] == blocks.MURU:
                    get(blocks.TEE)
                    lose(blocks.MURU)
                elif globals.gameState.inventory[select] == blocks.PUU:
                    get(blocks.PUIT)
                    lose(blocks.PUU)
                elif globals.gameState.inventory[select] == blocks.GORE:
                    lose(blocks.GORE)
                    globals.gameState.kuld += 2
                elif globals.gameState.inventory[select] == blocks.BORE and globals.gameState.amounts[select] >= 2:
                    get(blocks.AACT)
                    lose(blocks.BORE, 2)
                elif globals.gameState.inventory[select] == blocks.CORE and globals.gameState.amounts[select] >= 5:
                    globals.gameState.lifes += 1
                    lose(blocks.CORE, 5)
                elif globals.gameState.inventory[select] == blocks.KUKS:
                    get(blocks.AED)
                    lose(blocks.KUKS)
                elif globals.gameState.inventory[select] == blocks.AACT:
                    get(blocks.LAMMUTI)
                    lose(blocks.AACT)
                elif globals.gameState.inventory[select] == blocks.KULD:
                    get(blocks.KPD)
                    lose(blocks.KULD)
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
            if event.button == 1 and mxy[0]>globals.screenWidth/2-tol and mxy[0]<globals.screenWidth/2+tol and mxy[1]>globals.screenHeight/2-tol and mxy[1]<globals.screenHeight/2+tol:
                destroy(coordinates.screenToWorld(mxy[0],mxy[1])[0],
                coordinates.screenToWorld(mxy[0],mxy[1])[1])
            elif event.button == 3:
                if mxy[0]>globals.screenWidth/2-tol and mxy[0]<globals.screenWidth/2+tol and mxy[1]>globals.screenHeight/2-tol and mxy[1]<globals.screenHeight/2+tol:
                    mxw = coordinates.screenToWorld(mxy[0],mxy[1])[0]
                    myw = coordinates.screenToWorld(mxy[0],mxy[1])[1]
                    build(mxw, myw)
                    winx, winy = coordinates.worldToWindow(mxw, myw)
                    activate((winy,winx))
                if globals.gameState.inventory[select] == blocks.MQQK:
                    for x in range(-3,4):
                        for y in range(-3,4):
                            killKolls((hxy[0]+x, hxy[1]+y))
                if globals.gameState.inventory[select] == blocks.KIRKA:
                    for x in range(-3,4):
                        for y in range(-3,4):
                            destroy(hxy[0]+x, hxy[1]+y)
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
        ptext_rect.centerx = globals.screen.get_rect().centerx
        ptext_rect.y = 50
        globals.screen.blit(ptext,ptext_rect)
        globals.screen.blit(text,text_rect)
        pg.display.update()
        timer.tick(10)
    if globals.gameState.lifes == 0:
        uded = "SA SURID ÄRA"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = globals.screen.get_rect().centerx
        dtext_rect.y = 30
        globals.screen.blit(dtext,dtext_rect)
        globals.screen.blit(text,text_rect)
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
    if np.random.uniform() < kollProbability and len(globals.activeKollid) <= 12:
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
        globals.gameState.punktid += 100
        globals.gameState.kuld += 1
    col = pg.sprite.spritecollide(globals.hullmyts, globals.activeKollid, False)
    if len(col) > 0 and aia == 0:
        globals.gameState.lifes -= 1
        aia = 30
    if aia > 0:
        aia -= 1
    if select < 0:
        select = 19
    if select > 19:
        select = 0
    if globals.gameState.kuld >= 10  and not (empty == 20 and not blocks.KULD in globals.gameState.inventory):
        globals.gameState.kuld -= 10
        get(blocks.KULD)
    if globals.gameState.kollivaremed >= 10 and not (empty == 20 and not blocks.KOLLIV in globals.gameState.inventory):
        globals.gameState.kollivaremed -= 10
        get(blocks.KOLLIV)
    
    for s in range(0,20):
        if globals.gameState.amounts[s] <= 0:
            globals.gameState.inventory[s] = -1
        if globals.gameState.inventory[s] == -1:
            globals.gameState.amounts[s] = 0
    try:
        empty = globals.gameState.inventory.index(-1)
    except:
        empty = 20
    ## ---------- screen udpate ----------
    globals.screen.blit(globals.screenBuffer, coordinates.blitShift)
    ## add score and other info
    pg.draw.rect(globals.screen,(0,0,0),(0,18*tileScale,globals.screenWidth,30))
    score = ("punktid: " + str(globals.gameState.punktid) + " elud: " + str(globals.gameState.lifes) +
             " Kuld:" + str(globals.gameState.kuld) + " Kolli varemed:" + str(globals.gameState.kollivaremed))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = globals.screen.get_rect().centerx
    text_rect.y = 18*tileScale
    globals.screen.blit(text,text_rect)
    globals.screen.blit(hotbar,(0,0))
    globals.screen.blit(selslot,(select*18*tileScale,0))
    for s in range(0,20):
        globals.screen.blit(blocks.blocks[globals.gameState.inventory[s]],(18*tileScale*s+tileScale,tileScale))
        globals.textrender(str(globals.gameState.amounts[s]),18*tileScale*s+tileScale, tileSize)
    ## sprite update
    globals.player.update(mup, mdown, mleft, mright)
    # update crazy hat
    spriteBuffer.fill((0,0,0,0))
    if seehome == 1:
        globals.screen.blit(home, coordinates.worldToScreen(globals.gameState.home[0], globals.gameState.home[1]))
    ## draw sprites: static: no update need, dynamic: update
    drawSprites(globals.activeMineralGold, spriteBuffer)
    updateScreen()
    drawSprites(globals.activeKollid, spriteBuffer)
    globals.player.draw(spriteBuffer)
    # add sprites to spritebuffer.  this will be blitted
    # to the screen in the next loop
    globals.screen.blit(spriteBuffer, coordinates.blitShift)
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
