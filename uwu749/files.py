### load/save files, file dialogs and all that
import pickle

import globals
import sprites
import pygame as pg                                                        

hotbar = pg.transform.scale(pg.image.load("hotbar.png"),(180*3, 18*3))
selslot = pg.transform.scale(pg.image.load("selslot.png"),(18*3, 18*3))

def fileChooser(save):
    pg.init()
    choose = True
    select = False
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
        file = open(fName, "rb")
        ##
        world = pickle.load(file)
        ##
        stateDict = pickle.load(file)
        gameState = globals.GameState()
        gameState.undictify(stateDict)
        ##
        crazyHat = sprites.CrazyHat(gameState.home)
        try:
            CHDict = pickle.load(file)
            crazyHat.undictify(CHDict)
        except:
            print("cannot read Crazy Hat data")
        ##
        file.close()
        return world, gameState, crazyHat
    else:
        # cancel pressed
        return None
        
def saveWorld(world, gameState, crazyHat):
    """
    worlds: should contain terrain and such
    gameState: points and such
    """
    fName = fileChooser(True)
    if fName is not None:
        file = open(fName, "wb")
        pickler = pickle.Pickler(file)
        pickler.dump(world)
        pickler.dump(gameState.dictify())
        # save as dict for compatibility
        pickler.dump(crazyHat.dictify())
        file.close()

## Global window
gtkRootWin = Gtk.Window(title="File chooser GTK parent")
gtkRootWin.connect("destroy", Gtk.main_quit)
gtkRootWin.hide()
