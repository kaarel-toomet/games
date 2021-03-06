## Building block definitions and related code
import pygame as pg

NONE = -1
SEA = 0
LIIV = 1
MURU = 2
KIVI = 3
LUMI = 4
TEE = 5
KAST = 6
SYGAVM = 7
PUU = 8
MQQK = 9
PUIT = 10
KUKS = 11
LUKS = 12
KAKTUS = 13
KOLLIV = 14
KULD = 15
KIRKA = 16
KSEIN = 17
AUK = 18
ACT = 19
AACT = 20
AED = 21
GORE = 22
CORE = 23
BORE = 24
LAMMUTI = 25
KPD = 26
PORTAL = 27
BLOCK_END = 27

unbreakable = set([SYGAVM])
solid = set([KAST, KUKS, KOLLIV, KULD, KSEIN, AED, BORE, CORE, GORE])
breakto = {SYGAVM:SYGAVM, SEA:SYGAVM, LIIV:SEA, MURU:LIIV, TEE:MURU, KAST:LIIV,
            KIVI:MURU, LUMI:KIVI, PUU:MURU, NONE:NONE, MQQK:MQQK, PUIT:MURU,
           KUKS:LIIV, LUKS:LIIV, KAKTUS:LIIV, KOLLIV:MURU, KULD:MURU, KIRKA:KIRKA,
           KSEIN:KIVI, AUK:KIVI, AED:MURU, ACT:LIIV, AACT:LIIV,BORE:KSEIN,
           CORE:KSEIN, GORE:KSEIN, LAMMUTI:LIIV, KPD:LIIV, PORTAL:SYGAVM}
drops = {NONE:NONE, SEA:SEA, LIIV:LIIV, MURU:MURU, KIVI:KIVI, LUMI:LUMI,
         TEE:TEE, KAST:KAST, SYGAVM:NONE, PUU:PUU, MQQK:MQQK, PUIT:PUIT,
         KUKS:KUKS, LUKS:KUKS, KAKTUS:KAKTUS, KOLLIV:KOLLIV, KULD:KULD,
         KIRKA:KIRKA, KSEIN:KSEIN, AUK:AUK, ACT:AACT, AACT:AACT,
         AED:AED, GORE:GORE, CORE:CORE, BORE:BORE, LAMMUTI:LAMMUTI,
         KPD:KPD, PORTAL:PORTAL}
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
    kuld = pg.transform.scale(pg.image.load("blocks/goldblock.png"),
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
    sygavv = pg.transform.scale(pg.image.load("blocks/deepw.png"),
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
    mqqk = pg.transform.scale(pg.image.load("blocks/sword.png"),
                                (size, size))
    kaktus = pg.transform.scale(pg.image.load("blocks/kaktus.png"),
                                (size, size))
    puit = pg.transform.scale(pg.image.load("blocks/wood.png"),
                                (size, size))
    kolliv = pg.transform.scale(pg.image.load("blocks/kollivaremed.png"),
                                (size, size))
    kirka = pg.transform.scale(pg.image.load("blocks/kirka.png"),
                                (size, size))
    auk = pg.transform.scale(pg.image.load("blocks/auk.png"),
                                (size, size))
    bore = pg.transform.scale(pg.image.load("blocks/blupebbl.png"),
                                (size, size))
    gore = pg.transform.scale(pg.image.load("blocks/goldore.png"),
                                (size, size))
    fence = pg.transform.scale(pg.image.load("blocks/fence.png"),
                                (size, size))
    act = pg.transform.scale(pg.image.load("blocks/act.png"),
                                (size, size))
    aact = pg.transform.scale(pg.image.load("blocks/actact.png"),
                                (size, size))
    lammuti = pg.transform.scale(pg.image.load("blocks/lammuti.png"),
                                (size, size))
    kprnd = pg.transform.scale(pg.image.load("blocks/goldfloor.png"),
                                (size, size))
    oprt = pg.transform.scale(pg.image.load("blocks/omniportal.png"),
                                (size, size))
    ## set up the blocks dictionary
    blocks = { SEA:sky, LIIV:block, MURU:ground, TEE:tee,
               KAST:kast, KIVI:kivi, LUMI:lumi, SYGAVM:sygavv,
               PUU:puu, NONE:none, MQQK:mqqk, PUIT:puit,
               KUKS:cdoor, LUKS:odoor, KAKTUS:kaktus, KOLLIV:kolliv,
               KULD:kuld, KIRKA:kirka, KSEIN:pebbl, AUK:auk,
               AED:fence, ACT:act, AACT:aact, BORE:bore, CORE:core,
               GORE:gore, LAMMUTI:lammuti, KPD:kprnd, PORTAL:oprt}
    bn={SEA:"vesi",LIIV:"liiv", MURU:"muru", TEE:"tee",
        KAST:"kast", KIVI:"kivi", LUMI:"lumi",SYGAVM:"sügav vesi",
        PUU:"puu", NONE:"eimiski", MQQK:"mõõk", PUIT:"puit",
        KUKS:"kinnis uks", LUKS:"lahtis uks", KAKTUS:"kaktus",
        KOLLIV: "Kolli varemed", KULD: "kullaplokk", KIRKA:"kirka",
        KSEIN:"koopasein", AUK:"auk (portaal maa alla)", AED:"aed",
        ACT:"aktivaator",AACT:"aktiveeritud aktivaator",
        BORE:"sinivärgi maak", CORE:"söemaak", GORE:"kullamaak",
        LAMMUTI:"Lõhkumismasin", KPD:"Kullast põrand",
        PORTAL:"Portaal lampidesse dimensioonidesse"}

