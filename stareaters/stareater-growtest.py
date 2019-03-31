import pygame as pg
import random as r
pg.init()
pg.mixer.init()
pop = pg.mixer.Sound("pop.wav")
blip = pg.mixer.Sound("blip.wav")
blap = pg.mixer.Sound("blap.wav")
pic = pg.image.load("hullmyts.png")
star = pg.image.load("star.png")
thing = pg.image.load("thing.png")
blu = pg.image.load("blub.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("Star Eater")
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
speed = 1
speedf = 1
player = pg.sprite.Group()
potatoes = pg.sprite.Group()
stars = pg.sprite.Group()
thingy = pg.sprite.Group()
blub = pg.sprite.Group()
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
class Thing(pg.sprite.Sprite):
    xvel = 0
    yvel = 0
    def __init__(self, x, y, xvel, yvel, img):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.xvel = xvel
        self.yvel = yvel
    def update(self,newspeed = False, b = False):
        vel = 10
        if newspeed:
            self.xvel = r.randint(-vel,vel)
            self.yvel = r.randint(-vel,vel)
        while (self.xvel == 0 or self.yvel == 0) and b:
            self.xvel = r.randint(-vel,vel)
            self.yvel = r.randint(-vel,vel)
        if self.x + self.xvel <= screenw-90 and self.rect.x + self.xvel >= 0:
            self.x += self.xvel*speedf
            self.rect.x = int(self.x)
        else:
            self.xvel = -self.xvel*speedf
        if self.y + self.yvel <= screenh-90 and self.rect.y + self.yvel >= 0:
            self.y += self.yvel*speedf
            self.rect.y = int(self.y)
        else:
            self.yvel = -self.yvel*speedf
def reset():
    global starseaten, lifes, gameover, hullmyts, stars, thingy, blub
    gameover = False
    screen.fill((0, 0, 0))
    starseaten = 0
    lifes = 5
    time = 600
    thingy.empty()
    stars.empty()
    blub.empty()
hullmyts = Player(screenw/2,screenh/2)
player.add(hullmyts)
stars.add(Thing(r.randint(10,screenw-90),r.randint(10,screenh-90),0,0, star))
bob = Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),
                       r.randint(-10,10),r.randint(-10,10), thing)
thingy.add(bob)
blub.add(Thing(r.randint(10,screenw-90),r.randint(10,screenh-90),0,0, blu))
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
                if event.key == pg.K_r:
                    reset()
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
            " Time: " + str(time//60) + " Stars: " + str(len(stars)))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    stars.update(True, True)
    stars.draw(screen)
    thingy.update(False,  True)
    thingy.draw(screen)
    blub.update()
    blub.draw(screen)
    col = pg.sprite.spritecollide(hullmyts,stars,False)
    if len(col) > 0:
        starseaten +=1
        stars.remove(col)
        tick = 0 
        time += 60
        pop.play()
    ycol = pg.sprite.spritecollide(hullmyts,thingy,False)
    if len(ycol) > 0:
        starseaten +=1
        thingy.remove(ycol)
        tick = 0
        time += 60
        blip.play()
    scol = pg.sprite.spritecollide(hullmyts,blub,False)
    if len(scol) > 0:
        starseaten +=1
        blub.remove(scol)
        tick = 0
        time += 60
        blip.play()
    mcol = pg.sprite.groupcollide(thingy, stars, True, True)
    for s in mcol.keys():
        if len(mcol[s]) > 0:
            stars.add(Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),
                      0,0, star))
            stars.add(Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),
                      0,0, star))
            thingy.add(Thing(s.rect.x,s.rect.y,
                       r.randint(-10,10),r.randint(-10,10), thing))
    bcol = pg.sprite.groupcollide(blub, stars, False, True)
    for s in bcol.keys():
        if len(bcol[s]) > 0:
            bob = Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),
                       r.randint(-10,10),r.randint(-10,10), thing)
            thingy.add(bob)
            blub.add(Thing(s.rect.x,s.rect.y,r.randint(-1,1),r.randint(-1,1), blu))
    if len(stars) > 0:
        time -= 1
    if len(stars) == 0:
        tick += 1
    if tick == 1:
        tick = 0
        stars.add(Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),
                       0,0, star))
    thingy.empty()  ###############ASFDSFADFASDFADFADdsfasdf
    if len(thingy) == 0:
        bob = Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),
                       r.randint(-10,10),r.randint(-10,10), thing)
        thingy.add(bob)
    if len(blub) == 0:
        blub.add(Thing(r.randint(20,screenw-100),r.randint(20,screenh-90),0,0, blu))
    #blub.empty()    #######################SAedfasdfadsasddsfsd
    if time == time-22:
        time = 600
        lifes -= 1
        blip.play()
    pg.display.update()
    timer.tick(60)

pg.quit()
