import pygame
#11.45
import pygame.freetype
import random
pygame.init()
x=1366
y=768
window=pygame.display.set_mode((x, y))
pygame.display.set_caption("Gra Pracownia Programowania")
bg=pygame.image.load('img/bg.jpg ')
look = pygame.image.load('img/statek.png')
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel =16 * facing
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 25
        self.hitbox = (self.x + 30, self.y, 40, 40)
        self.hitbox1 = (self.x, self.y + 40, 100, 60)
    def draw(self,window):
        window.blit(look,(self.x,self.y))
        self.hitbox = (self.x+30, self.y, 40, 40)
        self.hitbox1 = (self.x, self.y+40, 100, 60)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox1, 2)

class Enemy(object):
    def __init__(self,x,y,width,height,health,design,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [self.x, y-height]
        self.health= health
        self.design=design
        self.vel=vel
        self.hitbox = (self.x, self.y, self.width, self.height)
    def draw (self,window):
        self.move()
        self.hitbox = (self.x, self.y, self.width, self.height)
        window.blit(self.design,(self.x,self.y))
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
    def move (self):
        if self.vel>0:
            if self.health>0:
                self.y+=self.vel
    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            print('umar')
        print('hit')
    def colision(self):
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('zderzenie', 1, (255, 0, 0))
        window.blit(text, (250 - (text.get_width() / 2), 200))
#mainstuff
def redrawGameWindow():
    window.blit(bg,(0,0))
    spaceship.draw(window)
    for Enemy in enemies:
        Enemy.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    #zawszeostatnie
    pygame.display.update()
##
font=pygame.font.SysFont('comicsans',30,True,True)
clock = pygame.time.Clock()
run=True
spaceship=player((x-100)/2,y-105,100,100)
bullets=[]
enemies=[]
wave_lenght=0
#enemies.append(Enemy(random.randint(0,x-100),0,100,100,10,pygame.image.load('img/enemy2.png'),1)) #enemi[0]
#enemies.append(Enemy(random.randint(0,x-100),0,100,100,20,pygame.image.load('img/enemy1.png'),3)) #enemi[1]
#enemies.append(Enemy(random.randint(0,x-100),0,100,100,50,pygame.image.load('img/enemy3.png'),2)) #enemi[2]
on_window=[]
score=1
#mainloop
while run:
    clock.tick(27)
    # enemi  self.hitbox = (self.x, self.y, self.width, self.height)
    # statek self.hitbox = (self.x + 30, self.y, 40, 40)
    # dol st self.hitbox1 = (self.x, self.y + 40, 100, 60)
    # if score%8==0:
    #     i+=1
    #     enemies.append(Enemy(random.randint(0, x - 100), 0, 100, 100, 10, pygame.image.load('img/enemy2.png'), 1))
    #     break
    #najutrosprobujforem
    if len(enemies)==0:
        wave_lenght+=3
        for i in range (wave_lenght):
            enemy=Enemy(random.randint(0, x - 100), 0, 100, 100, 10, pygame.image.load('img/enemy2.png'), 1)  # enemi[0]
            enemies.append(enemy)
    for enemy in enemies[:]:

        if spaceship.hitbox1[1]+spaceship.hitbox1[3] < enemy.hitbox[1]+enemy.hitbox[3]:
             print ('przelecial')
        if spaceship.hitbox[1]< enemy.hitbox[1]+enemy.hitbox[3]and spaceship.hitbox[0]<enemy.hitbox[0]+enemy.hitbox[2] and enemy.hitbox[0]<spaceship.hitbox[0]+spaceship.hitbox[2]:#nadlatuje od gory do dzioba/jego koniec mniejszy niz moj poczatek czyli po lewej/jego poczatek mniejszy niz moj koniec czyli po prawej
             print('zderzenie')
        if spaceship.hitbox1[1]< enemy.hitbox[1]+enemy.hitbox[3]and spaceship.hitbox1[0]<enemy.hitbox[0]+enemy.hitbox[2] and enemy.hitbox[0]<spaceship.hitbox1[0]+spaceship.hitbox1[2]:#nadlatuje od gory do dzioba/jego koniec mniejszy niz moj poczatek czyli po lewej/jego poczatek mniejszy niz moj koniec czyli po prawej
             print ('zderzenie')
        for bullet in bullets:
            if bullet.y-bullet.radius<enemy.hitbox[1]+enemy.hitbox[3] and bullet.y+bullet.radius>enemy.hitbox[1]:
                if bullet.x+bullet.radius>enemy.hitbox[0] and bullet.x-bullet.radius<enemy.hitbox[0]+enemy.hitbox[2]:
                    enemy.health-=1
                    bullets.pop(bullets.index(bullet))
                    score+=1
                    if enemy.health==0:
                        enemies.remove(enemy)
            if bullet.y> 0:
                bullet.y -=bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship.x>0:
        spaceship.x -= spaceship.vel
    if keys[pygame.K_RIGHT] and spaceship.x< x-100:
        spaceship.x += spaceship.vel
    if keys[pygame.K_SPACE]:
        if len(bullets) < 50:
            bullets.append(projectile(round(spaceship.x + spaceship.width // 2), round(spaceship.y), 6, (255, 0, 0), 1))
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run=False
    redrawGameWindow()
