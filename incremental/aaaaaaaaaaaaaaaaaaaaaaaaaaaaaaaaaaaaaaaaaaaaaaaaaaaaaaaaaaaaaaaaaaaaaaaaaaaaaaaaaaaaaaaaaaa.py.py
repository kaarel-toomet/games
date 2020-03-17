import pygame as pg
import random as r
import numpy as np
pg.init()
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
dist = 5
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
h = 0
c = 0
clvl = 0
slvl = 0
click = False
hold = False
stkm = 0
laser = 0
llvl = 0
prokoli = 0
bx = 0
by = 0
prkbase = 10
prkbasecost = 2
prkbaselvl = 0
holdable = 0
#txt = ("l", "厨房", str(3**clvl*200), str(10*1.1**stkm), str(1000*2**slvl), str(100*1.1**laser))
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
button = pg.sprite.Group()
class Button(pg.sprite.Sprite):
    def __init__(self,x,y, pic, n, clr=(64, 64, 64), size=21, still=False):
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
def reset():
    lifes = 5
    player.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
def rtxt(x,y,txt,color,size=20,still=False):
    global bx,by
    font = pg.font.SysFont("DejaVu Sans", size)
    text = font.render(txt, True, color)
    text_rect = text.get_rect()
    if still:
        text_rect.centerx = x
        text_rect.centery = y
    else:
        text_rect.centerx = x-bx
        text_rect.centery = y-by
    screen.blit(text,text_rect)
button.add(Button(screenw/2-100, screenh/2-100, thing, 1, (128, 128, 128), 30, True))#köök
button.add(Button(100,100,btn,2,(255,255,255),20)) #click lvl
button.add(Button(screenw-400,100,btn,3,(255,255,255),20))#stkm
button.add(Button(100,200,btn,4,(255,255,255),20)) #stkm lvl
button.add(Button(screenw-400,200,btn,5,(255,255,255),20)) #lasers
button.add(Button(100,300,btn,6,(255,255,255),20)) #nonexist
button.add(Button(screenw/2-100,screenh-100,btn,7,(255,0,0),20))#prestige
button.add(Button(screenw-300,screenh-100,btn,8,(255,255,255),50)) # prokoli upgs
button.add(Button(screenw+100,screenh-100,btn,9,(255,255,255),50)) # back
button.add(Button(screenw+100,100,btn,10,(255,255,255),20)) #prokoli base upg
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mup = True
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
        pg.display.update()
    txt = ("l", "厨房", str(3**clvl*200), str(int(10*1.1**stkm)),
           str(1000*3**slvl),str(int(100*1.1**laser)), str(2**llvl*500),
           "+" + str(int(np.log(h+0.1)/np.log(prkbase))-3) + " prokolit", ">","<", str(prkbasecost))
    mc = pg.mouse.get_pos()
    bhps = (stkm*2**slvl + laser*(10+laser*llvl))*(1+prokoli/10)
    h+=bhps/60
    if click:
        for b in button:
            if b.rect.collidepoint(mc):
                b.clicked()
    if c == 1:
        h += 2**clvl
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
    if c == 7 and h >= 10000:
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
        prkbasecost = int(prkbasecost*1.5)
        prkbase = 1 + (prkbase-1)*0.9
        prkbaselvl += 1
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
    rtxt(screenw/2,10,"h: " + str(int(h)),(255,255,255))
    rtxt(screenw/2,30,"hps: " + str(int(bhps)),(255,255,255))
    rtxt(screenw/2,50,"h/click: " + str(2**clvl),(255,255,255))
    rtxt(screenw/2,70,"prokoli: " + str(prokoli),(255,255,255))
    rtxt(screenw/2,screenh-150,"PRESTIGE",(255,255,255))
    rtxt(screenw-200,screenh-150,"prokoli upgrades",(255,255,255))
    rtxt(screenw+200,screenh-150,"back",(255,255,255))
    rtxt(screenw+200,50,"Reduce prokoli logarithm base - 1 by 10%" + ":" + str(prkbaselvl),(255,255,255))
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
