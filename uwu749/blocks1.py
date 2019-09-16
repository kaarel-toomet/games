## Building block definitions and related code
import pygame as pg

SEA = 0
SAND = 1
GRASS = 2
KIVI = 3
TEE = 4
KAST = 5
BLOCK_END = 5

breakable = set([])
solid = set([SEA,KAST])
breakto = {SEA:SEA, SAND:SEA, GRASS:SAND, TEE:SAND, KAST:SAND, KIVI:SAND}

blocks = {}
# initialize empty dictionary, to be filled with loadBlocks
# as soon as we know the size
bn = {}

def loadBlocks(size):
    ## load blocks and scale to size
    global blocks, bn
    block = pg.transform.scale(pg.image.load("asdfblock.png"),
                               (size, size))
    rblock = pg.transform.scale(pg.image.load("redblock.png"),
                                (size, size))
    sky = pg.transform.scale(pg.image.load("sky.png"),
                             (size, size))
    ground = pg.transform.scale(pg.image.load("ground.png"),
                                (size, size))
    tee = pg.transform.scale(pg.image.load("tee.png"),
                                (size, size))
    pebbl = pg.transform.scale(pg.image.load("pebbl.png"),
                                (size, size))
    core = pg.transform.scale(pg.image.load("coalpebbl.png"),
                                (size, size))
    kast = pg.transform.scale(pg.image.load("kast.png"),
                                (size, size))
    gold = pg.transform.scale(pg.image.load("goldblock.png"),
                                (size, size))
    gwall = pg.transform.scale(pg.image.load("goldwall.png"),
                                (size, size))
    window = pg.transform.scale(pg.image.load("window.png"),
                                (size, size))
    kivi = pg.transform.scale(pg.image.load("asdfback.png"),
                                (size, size))
    inf = pg.transform.scale(pg.image.load("infinity.png"),
                                (size, size))
    cdoor = pg.transform.scale(pg.image.load("cdoor.png"),
                                (size, size))
    odoor = pg.transform.scale(pg.image.load("odoor.png"),
                                (size, size))
    ## set up the blocks dictionary
    blocks = { SEA:sky, SAND:block, GRASS:ground, TEE:tee, KAST:kast, KIVI:kivi}
    bn={SEA:"vesi",SAND:"liiv", GRASS:"muru", TEE:"tee", KAST:"kast", KIVI:"kivi"}

