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
stuff = 0
clik = False
mc = pg.mouse.get_pos()
button = pg.sprite.Group()
class Button(pg.sprite.Sprite):
    def __init__(self,x,y, txt):
        pg.sprite.Sprite.__init__(self)
        self.image = btn
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.txt = txt
    def update(self):
        text = pfont.render(self.txt, True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.x+60
        text_rect.centery = self.rect.y+30
        screen.blit(text,text_rect)
db = Button(screenw/4, screenh/4, "dig")
button.add(db)
def reset():
    stuff = 0
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
            stuff += 1
    clik = False
    mc = pg.mouse.get_pos()
    screen.fill((0,0,0))
    score = ("stuff: " + str(stuff))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    button.draw(screen)
    button.update()
    pg.display.update()
    timer.tick(60)

pg.quit()
