import pygame as pg
import random as r
pg.init()
pic = pg.image.load("hullmyts.png")
star = pg.image.load("redstar.png")
potato = pg.image.load("potato.png")
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("Star Dodger")
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
ptick = 0
stick = 0
potatoeseaten = 0
lifes = 5
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
ptimer = False
stimer = False
player = pg.sprite.GroupSingle()
potatoes = pg.sprite.Group()
stars = pg.sprite.Group()
class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, mup, mdown, mleft, mright):
        if self.rect.y <= 0:
            up = False
        else:
            up = True
        if self.rect.y >= screenh-100:
            down = False
        else:
            down = True
        if self.rect.x <= 0:
            left = False
        else:
            left = True
        if self.rect.x >= screenw-124:
            right = False
        else:
            right = True
        if mup and up:
            self.rect.y -= dist 
        if mdown and down:
            self.rect.y += dist
        if mleft and left:
            self.rect.x -= dist
        if mright and right:
            self.rect.x += dist
    def tele(self,coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]
class Potato(pg.sprite.Sprite):
    xvel = 0
    yvel = 0
    def __init__(self, x, y, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        self.image = potato
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = xvel
        self.yvel = yvel
    def update(self,newspeed = False):
        if newspeed:
            self.xvel = r.randint(-10,10)
            self.yvel = r.randint(-10,10)
        if self.rect.x <= 10 or self.rect.x >= screenw-90:
            self.xvel = -self.xvel
        if self.rect.y <= 10 or self.rect.y >= screenh-30:
            self.yvel = -self.yvel
        self.rect.x += self.xvel
        self.rect.y += self.yvel
class Star(pg.sprite.Sprite):
    xvel = 0
    yvel = 0
    def __init__(self, x, y, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        self.image = star
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = xvel
        self.yvel = yvel
    def update(self,newspeed = False):
        if newspeed:
            self.xvel = r.randint(-10,10)
            self.yvel = r.randint(-10,10)
        if self.rect.x <= 10 or self.rect.x >= screenw-90:
            self.xvel = -self.xvel
        if self.rect.y <= 10 or self.rect.y >= screenh-30:
            self.yvel = -self.yvel
        self.rect.x += self.xvel
        self.rect.y += self.yvel
hullmyts = Player(screenw/2,screenh/2)
player.add(hullmyts)
potatoes.add(Potato(r.randint(10,screenw-30),r.randint(10,screenh-30),
                    r.randint(-10,10),r.randint(-10,10)))
stars.add(Star(r.randint(10,screenw-30),r.randint(10,screenh-30),0,0))
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
                potatoeseaten = 0
                lifes = 5
                ptick = 0
                stick = 0
                ptimer = False
                stimer = False
                player.empty()
                potatoes.empty()
                stars.empty()
                hullmyts = Player(screenw/2,screenh/2)
                player.add(hullmyts)
                potatoes.add(Potato(r.randint(10,screenw-30),r.randint(10,screenh-30),
                                    r.randint(-10,10),r.randint(-10,10)))
                stars.add(Star(r.randint(10,screenw-30),r.randint(10,screenh-30),0,0))


            elif event.key == pg.K_1:
                mp = pg.mouse.get_pos()
                hullmyts.tele((mp[0]-50,mp[1]-50))
            elif event.key == pg.K_2:
                points += 5
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
    if lifes <= 0:
        uded = "GAME OVER"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
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
                    potatoeseaten = 0
                    lifes = 5
                    ptick = 0
                    stick = 0
                    ptimer = False
                    stimer = False
                    player.empty()
                    potatoes.empty()
                    stars.empty()
                    hullmyts = Player(screenw/2,screenh/2)
                    player.add(hullmyts)
                    potatoes.add(Potato(r.randint(10,screenw-30),r.randint(10,screenh-30),
                                        r.randint(-10,10),r.randint(-10,10)))
                    stars.add(Star(r.randint(10,screenw-30),r.randint(10,screenh-30),0,0))
    screen.fill((0,0,0))
    score = "Potatoes Eaten: " + str(potatoeseaten) + " Lives: " + str(lifes)
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    potatoes.update()
    potatoes.draw(screen)
    stars.update()
    stars.draw(screen)
    pcol = pg.sprite.spritecollide(hullmyts,potatoes,False)
    if len(pcol) > 0:
        potatoeseaten += 1
        potatoes.remove(pcol)
        ptick = 0
        ptimer = True
    scol = pg.sprite.spritecollide(hullmyts,stars,False)
    if len(scol) > 0:
        lifes -= 1
        stars.remove(scol)
        stick = 0
        stimer = True
    if ptimer:
        ptick += 1
    if stimer:
        stick += 1
    if ptick >= 120:
        ptimer = False
        ptick = 0
        potatoes.add(Potato(r.randint(10,screenw-30),r.randint(10,screenh-30),
                            r.randint(-10,10),r.randint(-10,10)))
        stars.update(True)
    if stick >= 120:
        stimer = False
        stick = 0
        stars.add(Star(r.randint(10,screenw-30),r.randint(10,screenh-30),
                       r.randint(-10,10),r.randint(-10,10)))
        potatoes.update(True)
    pg.display.update()
    timer.tick(60)

pg.quit()
