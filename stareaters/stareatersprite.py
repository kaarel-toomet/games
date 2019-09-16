import pygame as pg
import random as r
pg.init()
pg.mixer.init()
pop = pg.mixer.Sound("pop.wav")
blip = pg.mixer.Sound("blip.wav")
blap = pg.mixer.Sound("blap.wav")
pic = pg.image.load("hullmyts.png")
star = pg.image.load("star.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("Star Eater")
acc = 0
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
time = 600
tick = 0
starseaten = 0
lifes = 5
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
player = pg.sprite.Group()
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
        if mup and up:
            self.rect.y -= dist
        if mdown and down:
            self.rect.y += dist
        if mleft and left:
            self.rect.x -= dist
        if mright and right:
            self.rect.x += dist
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
def reset():
    global hullmyts, starseaten, lifes, tick, time
    starseaten = 0
    lifes = 5
    tick = 0
    time = 600
    player.empty()
    stars.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
    stars.add(Star(r.randint(10,screenw-30),r.randint(10,screenh-30),0,0))
hullmyts = Player(screenw/2,screenh/2)
player.add(hullmyts)
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
        blap.play()
        uded = "GAME OVER"
        dtext = dfont.render(uded, False, (255,0,0))
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
                    reset()
    screen.fill((0,0,0))
    score = ("Stars Eaten: " + str(starseaten) + " Lives: " + str(lifes) +
            " Time: " + str(time//60))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    stars.update()
    stars.draw(screen)
    col = pg.sprite.spritecollide(hullmyts,stars,False)
    if len(col) > 0:
        starseaten +=1
        stars.remove(col)
        tick = 0
        time = 600
        pop.play()
    if len(stars) > 0:
        time -= 1
    if len(stars) == 0:
        tick += 1
    if tick == 5:
        tick = 0
        stars.add(Star(r.randint(20,screenw-100),r.randint(20,screenh-30),
                       r.randint(-10,10),r.randint(-10,10)))
    if time == 0:
        time = 600
        lifes -= 1
        blip.play()
    pg.display.update()
    timer.tick(60)

pg.quit()
