#!/usr/bin/env python3
import pygame as pg
import random as r
import numpy as np
pg.init()
pg.mixer.init()
pic = pg.image.load("../data/hullmyts.png")
pew = pg.image.load("pew.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("sdsadasdasdasdasdadsa")
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
mxy = pg.mouse.get_pos()
player = pg.sprite.Group()
pews = pg.sprite.Group()
class Player(pg.sprite.Sprite):
    def __init__(self,x):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = int(round(x[0]))
        self.rect.y = int(round(x[1]))
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
            self.rect.y -= dist 
        if mdown and down:
            self.rect.y += dist
        if mleft and left:
            self.rect.x -= dist
        if mright and right:
            self.rect.x += dist
        self.x = np.array([self.rect.x, self.rect.y])
    def xy(self, w):
        return self.x
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
        if self.x[1] <= 0 or self.x[1] >= screenh-30 or self.x[0] <= 0 or self.x[0] >= screenw-148:
            pews.remove(self)
        self.rect.x = int(round(self.x[0]))
        self.rect.y = int(round(self.x[1]))
def reset():
    lifes = 5
    player.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
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
            v = mxy-hullmyts.xy("asasdfasdfadfasdfasfdadsf")
            v = v/np.linalg.norm(v) * 5
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
        blap.play()
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
    mxy = np.array(pg.mouse.get_pos())
    screen.fill((0,0,0))
    score = ("Lifes: " + str(lifes))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    pews.update()
    pews.draw(screen)
    pg.display.update()
    timer.tick(60)

pg.quit()
