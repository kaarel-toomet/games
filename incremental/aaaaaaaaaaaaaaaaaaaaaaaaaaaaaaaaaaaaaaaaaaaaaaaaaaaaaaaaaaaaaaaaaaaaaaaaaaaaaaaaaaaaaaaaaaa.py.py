import pygame as pg
import random as r
import numpy as np
import re
def num(x):
    x = float(x)
    if x == x//1:
        x = int(x)
    return x
scode = list(input("Enter your save code, or 'x' for a new game:").split(",")) # 10 numbers separated by commas
try:
    scode = [num(x) for x in scode]
    h = scode[0]
    clvl = scode[1]
    slvl = scode[2]
    stkm = scode[3]
    laser = scode[4]
    llvl = scode[5]
    prokoli = scode[6]
    prkbase = scode[7]
    prkbaselvl = scode[8]
    hlvl = scode[9]
    hblvl = scode[10]
except:
    print("except")
    h=0   
    clvl = 0  #click lvl
    slvl = 0
    stkm = 0
    laser = 0
    llvl = 0
    prokoli = 0
    prkbase = 10 # the base of the log function used to generate prokoli amounts
    prkbaselvl = 0
    hlvl = 0  #hold level- 0=no holding, 1=hold to buy, 2=can hold on kitchen
    hblvl = 0 # helper bonus level
pg.init()
pg.font.init()
pg.mixer.init()
btn = pg.image.load("button2.png")
thing = pg.image.load("kitchen1.png")
stk = pg.image.load("stkm.png")
axe = pg.image.load("axe.png")
haxe = pg.transform.rotate(axe,90)
caxe = axe
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("trhtdsfthfghsfghsgfhsfdgtreytw")
do = True
timer = pg.time.Clock()
c = 0 # button thats clicked, 0=no buttons
click = False
hold = False
bx = 0
by = 0
holdable = 0
prkbasecost = 2
#txt = ("l", "厨房", str(3**clvl*200), str(10*1.1**stkm), str(1000*2**slvl), str(100*1.1**laser))
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
button = pg.sprite.Group()
class Button(pg.sprite.Sprite):
    def __init__(self,x,y, pic, n, clr=(64, 64, 64), size=21, still=False, minhold=1):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.clr = clr
        self.fontsize = size
        self.n=n
        self.still = still
        self.minhold = minhold
    def update(self):
        global txt
        rtxt(self.rect.centerx, self.rect.centery, txt[self.n],
             self.clr, self.fontsize, True)
        if not self.still:
            self.rect.x = self.x-bx
            self.rect.y = self.y-by
    def clicked(self):
        global c
        c=self.n
def rtxt(x,y,txt,color,size=20,still=False):
    global bx,by
    font = pg.font.SysFont("Times", size)
    text = font.render(txt, True, color)
    text_rect = text.get_rect()
    if still:
        text_rect.centerx = x
        text_rect.centery = y
    else:
        text_rect.centerx = x-bx
        text_rect.centery = y-by
    screen.blit(text,text_rect)
b1 = Button(screenw/2-100, screenh/2-100, thing, 1, (128, 128, 128), 30, True,2)#köök
b2 = Button(100,100,btn,2,(255,255,255),20) #click lvl
b3 = Button(screenw-400,100,btn,3,(255,255,255),20)#stkm
b4 = Button(100,200,btn,4,(255,255,255),20) #stkm lvl
b5 = Button(screenw-400,200,btn,5,(255,255,255),20) #lasers
b6 = Button(100,300,btn,6,(255,255,255),20) #nonexist
b7 = Button(screenw/2-100,screenh-100,btn,7,(255,0,0),20,True)#prestige
b8 = Button(screenw-300,screenh-100,btn,8,(255,255,255),50) # prokoli upgs
b9 = Button(screenw+100,screenh-100,btn,9,(255,255,255),50) # back
b10 = Button(screenw+100,100,btn,10,(255,255,255),20) #prokoli logbase upg
b11 = Button(screenw+100,150,btn,11,(255,255,255),20,False) #prokoli hold upg buy
b12 = Button(screenw+100,200,btn,12,(255,255,255),20,False) #prokoli hold upg köök
b13 = Button(screenw+100,300,btn,13,(255,255,255),20,False) #prokoli click boost
button.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13)
blist = (b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13)
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_h:
                holdable = 1-holdable
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
                hold = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                caxe = axe
                hold = False
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
    txt = ("l", "köök", str(3**clvl*200), str(int(10*1.1**stkm)),
           str(1000*3**slvl),str(int(100*1.1**laser)), str(2**llvl*500),
           "+" + str(int(np.log(h+0.1)/np.log(prkbase))-3) + " prokolit",
            ">","<", str(prkbasecost),"holdable buttons:3","holdable kitchen:10",
            "helper click bonus:10")
    mc = pg.mouse.get_pos()
    bhps = (stkm*2**slvl + laser*(10+laser*llvl))*(1+prokoli/10)
    h+=bhps/60
    if click:
        for b in button:
            if b.rect.collidepoint(mc):
                b.clicked()
    if hold and holdable == 1:
        for b in button:
            if b.rect.collidepoint(mc) and b.minhold <= hlvl:
                b.clicked()
    if c == 1:
        h += 2**(clvl+hblvl*(stkm//10+laser//10))
        caxe = haxe
    if c == 2 and h >= 3**clvl*200:
        h -= 3**clvl*200
        clvl += 1
    if c == 3 and h >= int(10*1.1**stkm):
        h -= int(10*1.1**stkm)
        stkm += 1
    if c == 4 and h >= 1000*3**slvl:
        h -= 1000*3**slvl
        slvl += 1
    if c == 5 and h >= 100*1.1**laser:
        h -= 100*1.1**laser
        laser += 1
    if c == 6 and h >= 2**llvl*500:
        h -= 2**llvl*500-10
        llvl += 1
    if c == 7 and int(np.log(h)/np.log(prkbase))-3 >= 1:
        prokoli += int(np.log(h)/np.log(prkbase))-3
        h = 0
        llvl = 0
        clvl = 0
        slvl = 0
        stkm = 0
        laser = 0
    if c == 8 and prokoli >= 0:
        bx = screenw
    if c == 9:
        bx = 0
    if c == 10 and prokoli >= prkbasecost:
        prokoli -= prkbasecost
        prkbase = 1 + (prkbase-1)*0.9
        prkbaselvl += 1
        prkbasecost = 2*1.5**prkbaselvl
    if c == 11 and prokoli >= 3:
        prokoli -= 3
        hlvl = 1
        button.remove(b11)
    if c == 12 and prokoli >= 10 and hlvl == 1:
        prokoli -= 10
        hlvl = 2
        button.remove(b12)
    if c == 13 and prokoli >= 1.5**hblvl:
        prokoli -= 1.5**hblvl
        hblvl += 1
    rtxt(200,60,"richer kitchens: " + str(clvl),(255,255,255))
    rtxt(200,80,"doubles click base",(255,255,255))
    rtxt(200,160,"better axes: " + str(slvl),(255,255,255))
    rtxt(200,180,"doubles stickman hps",(255,255,255))
    rtxt(200,260,"non-exist: " + str(llvl),(255,255,255))
    rtxt(200,280,"+10% laser hps per laser",(255,255,255))
    rtxt(200,20,"UPGRADES",(255,255,255), 50)
    rtxt(screenw-300,60,"helping stickman: " + str(stkm),(255,255,255))
    rtxt(screenw-300,80,"a stickman to break kitchens, +" + str(2**slvl) + " hps",(255,255,255))
    rtxt(screenw-300,160,"laser: " + str(laser),(255,255,255))
    rtxt(screenw-300,180,"good for breaking kitchens, + " + str(10+laser*llvl) + " hps",(255,255,255))
    rtxt(screenw-300,20,"SHOP",(255,255,255), 50)
    rtxt(screenw/2,10,"h: " + str(int(h)),(255,255,255),20,True)
    rtxt(screenw/2,30,"hps: " + str(int(bhps)),(255,255,255),20,True)
    rtxt(screenw/2,50,"h/click: " + str(2**(clvl+hblvl*(stkm//10+laser//10))),(255,255,255),20,True)
    rtxt(screenw/2,70,"prokoli: " + str(prokoli),(255,255,255),20,True)
    rtxt(screenw/2,90,"holdable: " + (holdable*"yes")+((1-holdable)*"no") + " (H)",(255,255,255),20,True)
    rtxt(screenw/2,screenh-150,"PRESTIGE",(255,0,0),20,True)
    rtxt(screenw-200,screenh-150,"prokoli upgrades",(255,255,255))
    rtxt(screenw+200,screenh-150,"back",(255,255,255))
    rtxt(screenw+200,50,"Reduce prokoli logarithm base - 1 by 10%" + ":" + str(prkbaselvl),(255,255,255))
    rtxt(screenw+200,275,"Double clicks per 10 of any helper: " + str(hblvl),(255,255,255))
    c=0
    click = False
    button.draw(screen)
    button.update()
    screen.blit(stk,(screenw/2-30,screenh/2-180))
    screen.blit(caxe,(screenw/2-32,screenh/2-160))
    pg.display.update()
    screen.fill((128,128,128))
    timer.tick(60)

pg.quit()
scode = (int(h),clvl,slvl,stkm,laser,llvl,prokoli,prkbase,prkbaselvl,hlvl,hblvl)
print("Here's your save code (don't copy parentheses):",scode)
