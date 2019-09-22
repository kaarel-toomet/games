## Building block definitions and related code
import pygame as pg

SEA = 0
SAND = 1
MURU = 2
KIVI = 3
LUMI = 4
TEE = 5
KAST = 6
SUGAVM = 7
BLOCK_END = 7

breakable = set([])
solid = set([KAST])
breakto = {SUGAVM:SUGAVM, SEA:SUGAVM, SAND:SEA, MURU:SAND, TEE:SAND, KAST:SAND, KIVI:MURU, LUMI:KIVI}

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
    tee = pg.transform.scale(pg.image.load("tee.png"),
                                (size, size))
    pebbl = pg.transform.scale(pg.image.load("pebbl.png"),
                                (size, size))
    core = pg.transform.scale(pg.image.load("coalpebbl.png"),
                                (size, size))
    kast = pg.transform.scale(pg.image.load("kast.png"),
                                (size, size))
    lumi = pg.transform.scale(pg.image.load("☃.png"),
                                (size, size))
    sugavv = pg.transform.scale(pg.image.load("deepw.png"),
                                (size, size))
    window = pg.transform.scale(pg.image.load("window.png"),
                                (size, size))
    kivi = pg.transform.scale(pg.image.load("blocks/asdfback.png"),
                                (size, size))
    inf = pg.transform.scale(pg.image.load("infinity.png"),
                                (size, size))
    cdoor = pg.transform.scale(pg.image.load("cdoor.png"),
                                (size, size))
    odoor = pg.transform.scale(pg.image.load("odoor.png"),
                                (size, size))
    ## set up the blocks dictionary
    blocks = { SEA:sky, SAND:block, MURU:ground, TEE:tee,
               KAST:kast, KIVI:kivi, LUMI:lumi, SUGAVM:sugavv}
    bn={SEA:"vesi",SAND:"liiv", MURU:"muru", TEE:"tee",
        KAST:"kast", KIVI:"kivi", LUMI:"lumi",SUGAVM:"sügav vesi"}

