#GhostDodgerCABSOE
#F5 to play
#P to pause/unpause
#R to reset(may be buggy)
#hold mouse button for the time to go faster
#arrows to move
#apples: +1 score
#ghosts: -1 lives(+1 score with immunity)
#cherries: +1 lives, spawn from the collision of apples and ghosts
#strawberries: +1 strawberry, spawn every 0-20 secs
#oranges: +1 orange, spawn every 0-20 secs
#S to eat a strawberry, +5 secs of immunity
#O to eat an orange, +5 secs of slow time
import pygame as pg
import random as r
pg.init()
pic = pg.image.load("pic.png")
ghost = pg.image.load("darkblueghost.png")
apple = pg.image.load("apple.png")
cherry = pg.image.load("cherry.png")
strawberry = pg.image.load("strawberry.png")
orange = pg.image.load("orange.png")
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("Ghost Dodger")
do = True
dist = 5
mup = False
mdown = False
mleft = False
mright = False
gofast = False
timer = pg.time.Clock()
atick = 0
gtick = 0
points = 0
lifes = 5
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
atimer = False
gtimer = False
sbtick = 0
sbmax = 600
imtick = 0
otick = 0
omax = 600
slowtick = 0
speed = 0
speedf = 1
vel = 0
ownedstrawberries = 0
ownedoranges = 0
player = pg.sprite.Group()
apples = pg.sprite.Group()
ghosts = pg.sprite.Group()
cherries = pg.sprite.Group()
strawberries = pg.sprite.Group()
oranges = pg.sprite.Group()
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
class Thing(pg.sprite.Sprite):
    xvel = 0
    yvel = 0
    def __init__(self, x, y, xvel, yvel, img):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        #print(self.rect)
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.xvel = xvel
        self.yvel = yvel
    def update(self,newspeed = False):
        vel = speed*speedf
        if newspeed:
            self.xvel = r.uniform(-vel,vel)
            self.yvel = r.uniform(-vel,vel)
        if self.x + self.xvel <= screenw-90 and self.rect.x + self.xvel >= 0:
            self.x += self.xvel*speedf
            self.rect.x = int(self.x)
        else:
            self.xvel = -self.xvel
        if self.y + self.yvel <= screenh-90 and self.rect.y + self.yvel >= 0:
            self.y += self.yvel*speedf
            self.rect.y = int(self.y)
        else:
            self.yvel = -self.yvel
def reset():
    global points, lifes, atick, gtick, atimer, gtimer, otick,\
           omax, slowtick, sbtick, sbmax, imtick, gameover, speed,\
           speedf
    speed = 0
    speedf = 1
    gameover = False
    screen.fill((0, 0, 0))
    points = 0
    lifes = 5
    atick = 0
    gtick = 0
    atimer = False
    gtimer = False
    apples.empty()
    ghosts.empty()
    cherries.empty()
    strawberries.empty()
    oranges.empty()
    otick = 0
    omax = 600
    slowtick = 0
    sbtick = 0
    sbmax = 600
    imtick = 0
    slowtick = 0
    apples.add(Thing(r.uniform(10,screenw-90),
                        r.uniform(10,screenh-50), 0, 0, apple))
    ghosts.add(Thing(r.uniform(10,screenw-90),
                    r.uniform(10,screenh-50),0,0, ghost))
Pic = Player(screenw/2,screenh/2)
player.add(Pic)
apples.add(Thing(r.uniform(10,screenw-90),r.uniform(10,screenh-50),
                    0, 0, apple))
ghosts.add(Thing(r.uniform(10,screenw-90),r.uniform(10,screenh-50), 0 ,0,
                 ghost))

while do:
    vel = speed*speedf
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
            elif event.key == pg.K_o:
                if ownedoranges != 0:
                    ownedoranges -= 1
                    speedf = 0.1
                    slowtick += 300
            elif event.key == pg.K_s:
                if ownedstrawberries != 0:
                    ownedstrawberries -= 1
                    imtick += 300
        elif event.type == pg.MOUSEBUTTONDOWN:
            gofast = True
        elif event.type == pg.MOUSEBUTTONUP:
            gofast = False
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
                    reset()
        uded = "GAME OVER"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
        apples.update()
        apples.draw(screen)
        ghosts.update()
        ghosts.draw(screen)
        cherries.update()
        cherries.draw(screen)
        strawberries.update()
        strawberries.draw(screen)
        pg.display.update()
    screen.fill((0,0,0))
    status = ("Score: " + str(points) + " Lifes: " + str(lifes) +
             " Immunity: " + str(imtick//60) + " Slow: " + str(slowtick//60)+
              " Strawberries: " + str(ownedstrawberries) + " Oranges: " +
              str(ownedoranges))
    text = font.render(status, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    apples.update()
    apples.draw(screen)
    ghosts.update()
    ghosts.draw(screen)
    cherries.update()
    cherries.draw(screen)
    strawberries.update()
    strawberries.draw(screen)
    oranges.update()
    oranges.draw(screen)
    acol = pg.sprite.spritecollide(Pic,apples,False)
    if len(acol) > 0:
        points += 1
        speed += 1
        apples.remove(acol)
        atick = 0
        atimer = True
    gcol = pg.sprite.spritecollide(Pic,ghosts,False)
    if len(gcol) > 0:
        if imtick == 0:
            lifes -= 1
        else:
            points += 1
            speed += 1
        ghosts.remove(gcol)
        gtick = 0
        gtimer = True
    mcol = pg.sprite.groupcollide(ghosts, apples,True, True)
    for s in mcol.keys():
        if len(mcol[s]) > 0:
            cherries.add(Thing(s.rect.x,s.rect.y,r.uniform(-points,points),
                               r.uniform(-points,points), cherry))
            gtick = 0
            gtimer = True
            atick = 0
            atimer = True
    ccol = pg.sprite.spritecollide(Pic,cherries,False)
    if len(ccol) > 0:
        lifes += 1
        cherries.remove(ccol)
    scol = pg.sprite.spritecollide(Pic,strawberries,False)
    if len(scol) > 0:
        ownedstrawberries += 1
        strawberries.remove(scol)
    ocol = pg.sprite.spritecollide(Pic,oranges,False)
    if len(ocol) > 0:
        ownedoranges += 1
        oranges.remove(ocol)
    if atimer:
        atick += 1
    if gtimer:
        gtick += 1
    if atick >= 120:
        atimer = False
        atick = 0
        apples.add(Thing(r.uniform(10,screenw-90),r.uniform(10,screenh-50),
                         r.uniform(-vel,vel),r.uniform(-vel,vel),apple))
        ghosts.update(True)
    if gtick >= 120:
        gtimer = False
        gtick = 0
        ghosts.add(Thing(r.uniform(10,screenw-90),r.uniform(10,screenh-50),
                         r.uniform(-vel,vel),r.uniform(-vel,vel),ghost))
        apples.update(True)
    sbtick += 1
    if imtick > 0:
        imtick -= 1
    if sbtick >= sbmax:
        sbtick = 0
        sbmax = r.uniform(0,2400)
        strawberries.add(Thing(r.uniform(10, screenw-90),
                               r.uniform(10, screenh-50),
                               r.uniform(-vel,vel),
                               r.uniform(-vel,vel), strawberry))
    otick += 1
    if slowtick > 0:
        slowtick -= 1
    if slowtick == 0:
        speedf = 1
    if otick >= omax:
        otick = 0
        omax = r.uniform(0,2400)
        oranges.add(Thing(r.uniform(10, screenw-90),
                               r.uniform(10, screenh-50),
                               r.uniform(-vel,vel),
                               r.uniform(-vel,vel), orange))
    pg.display.update()
    if not gofast:
        timer.tick(60)

pg.quit()
