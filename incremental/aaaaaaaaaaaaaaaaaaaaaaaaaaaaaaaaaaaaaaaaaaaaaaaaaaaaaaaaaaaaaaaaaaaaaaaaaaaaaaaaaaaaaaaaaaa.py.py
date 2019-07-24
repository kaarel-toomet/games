import pygame as pg
import random as r
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
click = False
hold = False
stkm = 0
txt = ("l", "厨房", str(3**clvl*200), str(20*1.1**stkm))
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
button = pg.sprite.Group()
class Button(pg.sprite.Sprite):
    def __init__(self,x,y, pic, n, clr=(64, 64, 64), size=21):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clr = clr
        self.fontsize = size
        self.n=n
    def update(self):
        global txt
        rtxt(self.rect.centerx, self.rect.centery, txt[self.n], self.clr, self.fontsize)
    def clicked(self):
        global c
        c=self.n
def reset():
    lifes = 5
    player.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
def rtxt(x,y,txt,color,size=20):
    font = pg.font.SysFont("FreeSans", size)
    text = font.render(txt, True, color)
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text,text_rect)
button.add(Button(screenw/2-100, screenh/2-100, thing, 1, (128, 128, 128), 30))
button.add(Button(100,100,btn,2,(255,255,255),10))
button.add(Button(screenw-300,100,btn,3,(255,255,255),10))
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
            click = True
            hold = True
        elif event.type == pg.MOUSEBUTTONUP:
            caxe=axe
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
        screen.blit(text,text_rect)
        pg.display.update()
    txt = ("l", "厨房", str(3**clvl*200), str(int(20*1.1**stkm)))
    mc = pg.mouse.get_pos()
    bhps = (stkm)/60
    h+=bhps
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
    rtxt(200,50,"richer kitchens",(255,255,255))
    rtxt(200,70,"doubles click base",(255,255,255))
    rtxt(200,20,"UPGRADES",(255,255,255), 50)
    rtxt(screenw-200,50,"helping stickman:",(255,255,255))
    rtxt(screenw-200,70,"a nice stickman to break more kitchens   n: " + str(stkm),(255,255,255))
    rtxt(screenw-200,20,"SHOP",(255,255,255), 50)
    rtxt(screenw/2,10,"h: " + str(int(h)),(255,255,255))
    c=0
    click = False
    button.draw(screen)
    button.update()
    screen.blit(stk,(screenw/2-30,screenh/2-180))
    screen.blit(caxe,(screenw/2-30,screenh/2-160))
    pg.display.update()
    screen.fill((128,128,128))
    timer.tick(60)

pg.quit()
