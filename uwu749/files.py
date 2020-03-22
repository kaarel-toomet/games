### load/save files, file dialogs and all that
import pickle

import globals
import sprites
import pygame as pg
import bz2

hotbar = pg.transform.scale(pg.image.load("hotbar.png"),(180*3, 18*3))
selslot = pg.transform.scale(pg.image.load("selslot.png"),(18*3, 18*3))

def fileChooser(save):
    pg.init()
    choose = True
    select = 0
    timer = pg.time.Clock()
    while choose:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                choose = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    return None
                elif event.key == 13:
                    return "world"+str(select)+".wrld"
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    select -= 1
                elif event.button == 5:
                    select += 1
        if select <= -1:
            select = 9
        elif select >= 10:
            select = 0
        globals.screen.blit(hotbar, (globals.screenWidth/2,200))
        globals.screen.blit(selslot, (globals.screenWidth/2+select*18*3,200))
        for x in range(0,10):
            globals.textrender(str(x),globals.screenWidth/2+x*18*3+27,200+27)
        timer.tick(10)
        pg.display.update()


def loadWorld():
    fName = fileChooser(False)
    if fName is not None:
        file = bz2.open(fName, "rb")
        ##
        components = pickle.load(file)
        ground = components.get("ground", None)
        underground = components.get("underground", None)
        sprites = components.get("sprites", None)
        gameState = globals.GameState()
        if "gameState" in components:
            gameState.undictify(components["gameState"])
        crazyHat = sprites.CrazyHat(gameState.home)
        if "crazyHat" in components:
            crazyHat.undictify(components["crazyHat"])
        ##
        file.close()
        return ground, underground, gameState, crazyHat
    else:
        # cancel pressed
        return None
        
def saveWorld(ground, underground, sprites,
              gameState, crazyHat):
    """
    ground: ground layer
    sprites: dict with components for "kollid" and
               other sprites
    gameState: points and such
    """
    fName = fileChooser(True)
    if fName is not None:
        file = bz2.open(fName, "wb")
        pickler = pickle.Pickler(file)
        components = {
            # save as dict for compatibility
            "ground" : ground,
            "underground" : underground,
            "sprites" : sprites,
            "gameState" : gameState.dictify(),
            "crazyHat" : crazyHat.dictify()
        }
        pickler.dump(components)
        file.close()
