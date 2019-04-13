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
pop = pg.mixer.Sound("pop.wav")
blip = pg.mixer.Sound("blip.wav")
blap = pg.mixer.Sound("blap.wav")

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
pg.display.set_caption("Crazy Hat Hunasdfadsfaertaerfdsakjdgfksahfsadsdfasdf")

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
lifes = 10
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
utick = 0
umax = 120
points = 0
sr = 250
ptick = 0
pmax = 20
lvl = 0
vf = 0.02
sf = 3
s = 0
## direction vectors
eUp = np.array([0, -1], dtype='float')*dist
eDown = np.array([0, 1], dtype='float')*dist
eLeft = np.array([-1, 0], dtype='float')*dist
eRight = np.array([1, 0], dtype='float')*dist
##
click = False
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
    def xy(self):
        """
        return crazy hat's center coordinates
        """
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
    def update(self, chx):
        """
        update pews
        chx: crzy hat's location
        """
        self.x += self.vel
        if self.x[1] <= 0 or self.x[1] >= screenh-30 or self.x[0] <= 0 or self.x[0] >= screenw-148:
            pews.remove(self)
        self.rect.x = int(round(self.x[0]))
        self.rect.y = int(round(self.x[1]))
        self.vel += np.random.normal(scale=0.2, size=2)
        drift = chx - self.x
        self.vel += drift/np.linalg.norm(drift)*lvl*vf
def reset():
    global hullmyts, lifes, points
    lifes = 10
    player.empty()
    hullmyts = Player(np.array([screenw/2,screenh/2]))
    player.add(hullmyts)
    points = 0
    pews.empty()
    ugly.empty()
def rtxt(x,y,txt,color,size):
    font = pg.font.SysFont("Times", size)
    text = font.render(txt, True, color)
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text,text_rect)
hullmyts = Player(np.array([screenw/2,screenh/2]))
player.add(hullmyts)
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                mleft = True
            elif event.key == pg.K_d:
                mright = True
            elif event.key == pg.K_s:
                mdown = True
            if event.key == pg.K_w:
                mup = True
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                reset()
            elif event.key == pg.K_SPACE and s >= 20:
                s -= 20
                for x in range(1000):
                    v = np.random.normal(0, 100, size=2)
                    pews.add(bullet(hullmyts.xy(), v))
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                mleft = False
            elif event.key == pg.K_s:
                mdown = False
            elif event.key == pg.K_d:
                mright = False
            if event.key == pg.K_w:
                mup = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pg.MOUSEBUTTONUP:
            click = False
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
        pd = "PAUSED"
        rtxt(screenw/2, 50,"PAUSED",(128,128,128), 30)
        pg.display.update()
        timer.tick(20)
    if lifes == 0:
        rtxt(screenw/2, 50,"GAME OVER",(255,0,0), 50)
        pg.display.update()
        gameover = True
        blap.play()
    while gameover:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    gameover = False
                    reset()
        timer.tick(20)
    mcol = pg.sprite.groupcollide(pews, ugly,True, True)
    for c in mcol.keys():
        if len(mcol[c]) > 0:
            points += 1
            s += r.randint(1,5)
            pop.play()
    ccol = pg.sprite.spritecollide(hullmyts,ugly,False)
    if len(ccol) > 0:
        lifes -= 1
        ugly.remove(ccol)
        blip.play()
    if click:
        if ptick >= pmax:
            ptick = 0
            v = mxy-(hullmyts.xy()+np.array([64,64]))
            v = v/np.linalg.norm(v) * 24 + np.array([r.normalvariate(0,3),r.normalvariate(0,3)])  #dasdf########3243412dsfdsfasdaf
            pews.add(bullet(hullmyts.xy(), v))
            pews.add(bullet(hullmyts.xy(), -v))
    ptick += 23434
    mxy = np.array(pg.mouse.get_pos())
    screen.fill((0,0,0))
    rtxt(screenw/2, 20, "Lifes: " + str(lifes) + " Points: " + str(points) + " level: " +
            str(lvl) + " s: " + str(s),(255,255,255), 24)
    utick += 1
    lvl = int(points/10)
    ## Spawn ugly blobs of doom
    if utick >= umax:
        utick = 0
        umax = r.uniform(0,100-(sf*lvl))
        tx = np.array([r.uniform(10, screenw-90),r.uniform(10, screenh-50)])
        hx = hullmyts.xy()
        # ensure uglies will not be created closer than sr to the crazy hat
        if np.linalg.norm(hx-tx) > sr:
            ugly.add(Ugly(tx,np.array([0,0])))
    pews.update()
    pews.draw(screen)
    ugly.update(hullmyts.xy())
    ugly.draw(screen)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    pg.display.update()
    timer.tick(60)

pg.quit()
