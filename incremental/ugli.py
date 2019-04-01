#!/usr/bin/env python3
#
##0,1,2,3(,4,5,6,7,8,9) to buy stuff, arrows to move
import pygame as pg
import random as r
pg.init()
pg.mixer.init()
#pop = pg.mixer.Sound("pop.wav")
#blip = pg.mixer.Sound("blip.wav")
#blap = pg.mixer.Sound("blap.wav")
pic = pg.image.load("hullmyts.png")
star = pg.image.load("star.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("uglu")
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
stick = 0
sspawn = 256
timer = pg.time.Clock()
lifes = 5
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
player = pg.sprite.Group()
stars = pg.sprite.Group()
thingies = 0
arrowfaces = 0
arrowfacep = 10
derpbits = 0
derpchance = 5
derpbots = 0
dgoo = 0
stuffers = 0
dwalls = 0
asdf = 0
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
        if self.rect.x >= screenw-120:
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
class Star(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = star
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.age = 0
    def update(self):
        self.age += 1
        if self.age >= 240:
           stars.remove(self)
def reset():
    lifes = 5
    player.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
hullmyts = Player(screenw/2,screenh/2)
player.add(hullmyts)
stars.add(Star(r.randint(0,screenw-120),r.randint(0,screenh-148)))
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
            elif event.key == pg.K_0 and thingies >= arrowfacep:
                thingies -= arrowfacep
                arrowfaces += 1
            elif event.key == pg.K_1 and derpbits > 0 and arrowfaces >= 10:
                derpbits -= 1
                arrowfaces -= 10
                derpbots += 1
            elif event.key == pg.K_2 and derpbots >= 2 and derpbits >= 2:
                derpbots -= 2
                derpbits -= 2
                stuffers += 1
            elif event.key == pg.K_3 and asdf >= 2 and dgoo >= 5:
                asdf -= 2
                dgoo -= 2
                dwalls += 1
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
    thingies += 0.1/60*arrowfaces
    dgoo += 0.05/60*derpbots
    asdf += 0.05/60*stuffers
    stick += 1
    if stick >= sspawn:
        stars.add(Star(r.randint(0,screenw-120),r.randint(0,screenh-148)))
        stick = 0
    col = pg.sprite.spritecollide(hullmyts,stars,False)
    if len(col) > 0:
        thingies += 1
        stars.remove(col)
        c = r.randint(0,100)
        if c <= derpchance:
            derpbits += 1
    screen.fill((0,0,0))
    score = ("thingies: " + str(round(thingies)) + " arrowfaces: " + str(arrowfaces))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    if derpbits > 0:
        score = ("derpbits: " + str(derpbits))
        text = font.render(score, True, (0,255,255))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = 30
        screen.blit(text,text_rect)
    if derpbots > 0:
        score = ("derpbots: " + str(derpbots) +
                 " D-goo: " + str(round(dgoo)) +
                 " stuffers: " + str(stuffers))
        text = font.render(score, True, (255,0,255))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = 50
        screen.blit(text,text_rect)
    if asdf > 0:
        score = ("ASDF: " + str(round(asdf)) +
                 " D-walls: " + str(round(dwalls)))
        text = font.render(score, True, (255,255,0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = 70
        screen.blit(text,text_rect)
    player.update(mup, mdown, mleft, mright)
    player.draw(screen)
    stars.update()
    stars.draw(screen)
    pg.display.update()
    timer.tick(60)

pg.quit()
