#!/usr/bin/env python3
import pygame as pg
import random as r
import numpy as np
import subprocess
import sys

pg.init()
pg.mixer.init()
pic = pg.image.load("../data/hullmyts.png")
pew = pg.image.load("pew.png")
ugl = pg.image.load("ugly.png")

## figure out the screen size
## The standard get_size() gives wrong results on multi-monitor setup
## use xrandr instead (only on linux)
xdotool = False
# did we get the data through xdotool?
if sys.platform == 'linux':
    res = subprocess.run("../scripts/activescreen", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(res.returncode == 0):
        # success
        wh = res.stdout.split(b' ')
        screenw = int(wh[0])
        screenh = int(wh[1])
        screen = pg.display.set_mode((screenw, screenh), pg.RESIZABLE)
        xdotool = True
if not xdotool:
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    screenw, screenh = pg.display.get_surface().get_size()
pg.display.set_caption("Crazy Hat Hunting")

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
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
utick = 0
umax = 120
points = 0
sr = 150
## direction vectors
eUp = np.array([0, -1], dtype='float')*dist
eDown = np.array([0, 1], dtype='float')*dist
eLeft = np.array([-1, 0], dtype='float')*dist
eRight = np.array([1, 0], dtype='float')*dist
##
mxy = pg.mouse.get_pos()
player = pg.sprite.Group()
pews = pg.sprite.Group()
ugly = pg.sprite.Group()
class Player(pg.sprite.Sprite):
    def __init__(self,x):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = int(round(x[0]))
        self.rect.y = int(round(x[1]))
        # location as float
        self.x = x.astype('float')
    def update(self, mup, mdown, mleft, mright):
        if self.rect.y <= 0:
            up = False
        else:
            up = True
        if self.rect.y >= screenh-120:
            down = False
        else:
            down = True
        if self.rect.x <= 0:
            left = False
        else:
            left = True
        if self.rect.x >= screenw-148:
            right = False
        else:
            right = True
        if mup and up:
            self.x += eUp
        if mdown and down:
            self.x += eDown
        if mleft and left:
            self.x += eLeft
        if mright and right:
            self.x += eRight
        self.rect.x = int(round(self.x[0]))
        self.rect.y = int(round(self.x[1]))
    def xy(self, w):
        return self.x + np.array([34,44])
class bullet(pg.sprite.Sprite):
    def __init__(self, x, vel):
        pg.sprite.Sprite.__init__(self)
        self.image = pew
        self.rect = self.image.get_rect()
        self.rect.x = int(round(x[0]))
        self.rect.y = int(round(x[1]))
        self.x = x.astype('float')
        self.vel = vel.astype('float')
    def update(self):
        self.x += self.vel
        if self.x[1] <= 0 or self.x[1] >= screenh-30 or self.x[0] <= 0 or self.x[0] >= screenw-90:
            pews.remove(self)
        self.rect.x = int(round(self.x[0]))
        self.rect.y = int(round(self.x[1]))
class Ugly(pg.sprite.Sprite):
    def __init__(self, x, vel):
        pg.sprite.Sprite.__init__(self)
        self.image = ugl
        self.rect = self.image.get_rect()
        self.rect.x = int(round(x[0]))
        self.rect.y = int(round(x[1]))
        self.x = x.astype('float')
        self.vel = vel.astype('float')
    def update(self):
        self.x += self.vel
        if self.x[1] <= 0 or self.x[1] >= screenh-30 or self.x[0] <= 0 or self.x[0] >= screenw-148:
            pews.remove(self)
        self.rect.x = int(round(self.x[0]))
        self.rect.y = int(round(self.x[1]))
        self.vel += np.array([r.uniform(-1,1),r.uniform(-1,1)])
def reset():
    global hullmyts, lifes, points
    lifes = 5
    player.empty()
    hullmyts = Player(np.array([screenw/2,screenh/2]))
    player.add(hullmyts)
    points = 0
    pews.empty()
    ugly.empty()
hullmyts = Player(np.array([screenw/2,screenh/2]))
player.add(hullmyts)
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
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            v = mxy-(hullmyts.xy("asasdfasdfadfasdfasfdadsf")+np.array([64,64]))
            v = v/np.linalg.norm(v) * 21
            pews.add(bullet(hullmyts.xy(2435678), v))
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
    if lifes == 0:
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
                    reset()
    mcol = pg.sprite.groupcollide(pews, ugly,True, True)
    for s in mcol.keys():
        if len(mcol[s]) > 0:
            points += 1
    ccol = pg.sprite.spritecollide(hullmyts,ugly,False)
    if len(ccol) > 0:
        lifes -= 1
        ugly.remove(ccol)
    mxy = np.array(pg.mouse.get_pos())
    screen.fill((0,0,0))
    score = ("Lifes: " + str(lifes) + " Points: " + str(points))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    utick += 1
    if utick >= umax:
        utick = 0
        umax = r.uniform(0,90)
        tx = np.array([r.uniform(10, screenw-90),r.uniform(10, screenh-50)])
        hx = hullmyts.xy(True)
        # ensure uglies will not be created closer than sr to the crazy hat
        if np.linalg.norm(hx-tx) > sr:
            ugly.add(Ugly(tx,np.array([0,0])))
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    pews.update()
    pews.draw(screen)
    ugly.update()
    ugly.draw(screen)
    pg.display.update()
    timer.tick(60)

pg.quit()
