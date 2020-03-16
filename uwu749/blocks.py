## Building block definitions and related code
import pygame as pg

NONE = -1
SEA = 0
SAND = 1
MURU = 2
KIVI = 3
LUMI = 4
TEE = 5
KAST = 6
SUGAVM = 7
PUU = 8
BLOCK_END = 8

unbreakable = set([SUGAVM])
solid = set([KAST])
breakto = {SUGAVM:SUGAVM, SEA:SUGAVM, SAND:SEA, MURU:SAND, TEE:SAND, KAST:SAND, KIVI:MURU, LUMI:KIVI, PUU:MURU, NONE:NONE}

blocks = {}
# initialize empty dictionary, to be filled with loadBlocks
# as soon as we know the size
bn = {}

def loadBlocks(size):
    ## load blocks and scale to size
    global blocks, bn
    block = pg.transform.scale(pg.image.load("blocks/asdfblock.png"),
                               (size, size))
    rblock = pg.transform.scale(pg.image.load("blocks/redblock.png"),
                                (size, size))
    sky = pg.transform.scale(pg.image.load("blocks/sky.png"),
                             (size, size))
    ground = pg.transform.scale(pg.image.load("blocks/ground.png"),
                                (size, size))
    tee = pg.transform.scale(pg.image.load("blocks/tee.png"),
                                (size, size))
    pebbl = pg.transform.scale(pg.image.load("blocks/pebbl.png"),
                                (size, size))
    core = pg.transform.scale(pg.image.load("blocks/coalpebbl.png"),
                                (size, size))
    kast = pg.transform.scale(pg.image.load("blocks/kast.png"),
                                (size, size))
    lumi = pg.transform.scale(pg.image.load("blocks/☃.png"),
                                (size, size))
    sugavv = pg.transform.scale(pg.image.load("blocks/deepw.png"),
                                (size, size))
    window = pg.transform.scale(pg.image.load("blocks/window.png"),
                                (size, size))
    kivi = pg.transform.scale(pg.image.load("blocks/asdfback.png"),
                                (size, size))
    inf = pg.transform.scale(pg.image.load("blocks/infinity.png"),
                                (size, size))
    cdoor = pg.transform.scale(pg.image.load("blocks/cdoor.png"),
                                (size, size))
    odoor = pg.transform.scale(pg.image.load("blocks/odoor.png"),
                                (size, size))
    puu = pg.transform.scale(pg.image.load("blocks/puu.png"),
                                (size, size))
    none = pg.transform.scale(pg.image.load("blocks/na.png"),
                                (size, size))
    ## set up the blocks dictionary
    blocks = { SEA:sky, SAND:block, MURU:ground, TEE:tee,
               KAST:kast, KIVI:kivi, LUMI:lumi, SUGAVM:sugavv, PUU:puu, NONE:none}
    bn={SEA:"vesi",SAND:"liiv", MURU:"muru", TEE:"tee",
        KAST:"kast", KIVI:"kivi", LUMI:"lumi",SUGAVM:"sügav vesi", PUU:"puu", NONE:"eimiski"}

