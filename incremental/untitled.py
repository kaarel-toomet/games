#!/usr/bin/env python3

### slightly less WIP

import pygame as pg
import random as r
pg.init()
pg.mixer.init()
pic = pg.image.load("hullmyts.png")
btn = pg.image.load("button.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("untitled (W.I.P.)")
do = True
timer = pg.time.Clock()
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
paper = 0
tpaper = 0
water = 0
wfilters = 0
wwater = 0
ppumps = 0
pplvl = 0
clik = False
unl = 0
mc = pg.mouse.get_pos()
button = pg.sprite.Group()
class Button(pg.sprite.Sprite):
    def __init__(self,x,y, txt, txt2, font):
        pg.sprite.Sprite.__init__(self)
        self.image = btn
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.txt = txt
        self.txt2 = txt2
        self.font = font
    def update(self):
        text = self.font.render(self.txt, True, (64,64,64))
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.x+60
        text_rect.centery = self.rect.y+20
        screen.blit(text,text_rect)
        text = self.font.render(self.txt2, True, (64,64,64))
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.x+60
        text_rect.centery = self.rect.y+40
        screen.blit(text,text_rect)
db = Button(screenw/4, screenh/4, "cheeseburger", "+1 paper", pg.font.SysFont("Times", 21))
button.add(db)
def reset():
    paper = 0
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
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
            clik = True
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
    if clik:
        if db.rect.collidepoint(mc):
            paper += 1
        try:
            if rb.rect.collidepoint(mc) and paper >= 10:
                tpaper += 1
                paper -= 10
        except:
            pass
        try:
            if pb.rect.collidepoint(mc) and tpaper >= 10:
                tpaper -= 10
                ppumps += 1
        except:
            pass
        try:
            if cb.rect.collidepoint(mc) and tpaper >= 1 and paper >= 3:
                tpaper -= 1
                paper -= 3
                wfilters += 1
        except:
            pass
        try:
            if ub.rect.collidepoint(mc) and wfilters >= 5 and tpaper >= 2:
                wfilters -= 5
                tpaper -= 2
                pplvl = 1
                button.remove(ub)
        except:
            pass
    clik = False
    if paper >= 10 and unl == 0:
        unl = 1
        rb = Button(screenw/4, screenh/4+60, "upgrade paper", "-10 p +1 tp", pg.font.SysFont("Times", 21))
        button.add(rb)
    if tpaper >= 10 and unl == 1:
        unl = 2
        pb = Button(screenw/4, screenh/4+120, "make paper pump", "-10 tp +1 pp", pg.font.SysFont("Times", 16))
        button.add(pb)
    if ppumps >= 3 and unl == 2:
        unl = 3
        cb = Button(screenw/4, screenh/4+180, "make weird filter", "-1 tp -3 p +1 wf", pg.font.SysFont("Times", 16))
        button.add(cb)
        ub = Button(screenw/4, screenh/4+240, "upgrade pumps", "-5 wf -2 tp", pg.font.SysFont("Times", 18))
        button.add(ub)
    water += 0.5/60*ppumps
    if pplvl == 1:
        wwater += 0.1/60*ppumps
    score = ("paper (p): " + str(paper))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    score = ("thick paper (tp): " + str(tpaper))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 40
    if unl >= 1:
        screen.blit(text,text_rect)
    score = ("paper pumps (pp): " + str(ppumps) + "  water: " + str(round(water,1)))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 70
    if unl >= 2:
        screen.blit(text,text_rect)
    score = ("weird filters (wf): " + str(wfilters) + "  weird water (ww): " + str(round(wwater,1)))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 100
    if unl >= 3:
        screen.blit(text,text_rect)
    mc = pg.mouse.get_pos()
    button.draw(screen)
    button.update()
    pg.display.update()
    screen.fill((0,0,0))
    timer.tick(60)

pg.quit()
