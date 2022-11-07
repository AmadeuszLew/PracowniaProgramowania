import pygame
import os
import random
pygame.font.init()
width,height=1368,768
WINDOW=pygame.display.set_mode((width,height))
pygame.display.set_caption("gra-projekt")

#load images
#enemies
enemy1=pygame.image.load(os.path.join("img1","enemy1.png"))
enemy2=pygame.image.load(os.path.join("img1","enemy2.png"))
enemy3=pygame.image.load(os.path.join("img1","enemy3.png"))
#playerplayer
ourself=pygame.image.load(os.path.join("img1","me.png"))
#lasers
violetlaser=pygame.image.load(os.path.join("img1","fioletowylaser.png"))
bluelaser=pygame.image.load(os.path.join("img1","niebieskilaser.png"))
yellowlaser=pygame.image.load(os.path.join("img1","zoltylaser.png"))
greylaser=pygame.image.load(os.path.join("img1","szarylaser.png"))
#background
bg=pygame.image.load(os.path.join("img1","bg.jpg"))

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y+=vel

    def off_screen(self,height):
        return not (self.y<=height and self.y>=0)

    def collision(self, obj):
        return collide(self, obj)
class ship: #to interact
    COOLDOWN= 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img,(self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter>self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser=Laser(self.x+25,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img=ourself
        self.laser_img=violetlaser
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)
    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10, self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10, self.ship_img.get_width()*(self.health/self.max_health),10))
class Enemy(ship):
    ENEMY_MAP={
                "enemy1":(enemy1, greylaser),
                "enemy2":(enemy2,yellowlaser),
                "enemy3":(enemy3,bluelaser)
             }
    def __init__(self,x,y,enemy,health=100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img=self.ENEMY_MAP[enemy]
        self.mask=pygame.mask.from_surface(self.ship_img)
    def move(self,vel):
        self.y+=vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None #(x,y)

def main():
    run=True
    FPS=60
    level=0
    lives=5
    player_vel=5
    player=Player(600,650)
    main_font=pygame.font.SysFont("comicsans",50)
    lost_font=pygame.font.SysFont("comicsans",60)

    enemies=[]
    wave_length=0
    enemy_vel=1

    laser_vel=6
    lost=False
    lost_count=0
    clock=pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(bg,(0,0))
        #draw text
        lives_label=main_font.render(f"Lives:{lives}",1,(240,0,0))
        level_label=main_font.render(f"Level:{level}",1,(240,0,0))
        WINDOW.blit(lives_label,(10,10))
        WINDOW.blit(level_label,(width-level_label.get_width()-10,10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)
        if lost:
            lost_label=lost_font.render("You Lost!",1,(255,255,255))
            WINDOW.blit(lost_label,(width/2-lost_label.get_width()/2,height/2))
        pygame.display.update() #lastone
    while run:
        clock.tick(FPS)
        redraw_window()
        if lives <=0 or player.health<=0:
            lost=True
            lost_count+=1
        if lost:
            if lost_count>FPS*3:
                run=False
            else:
                continue
        if len(enemies)==0:
            level+=1
            wave_length+=5
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,width-100),random.randrange(-100,0),random.choice(["enemy1","enemy2","enemy3"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
        keys=pygame.key.get_pressed()#to chceck 2 keys in 1 time

        if keys[pygame.K_UP]and player.y -player_vel:
            player.y -=player_vel
        if keys[pygame.K_DOWN] and player.y+player_vel+player.get_height()<height:
            player.y+=player_vel
        if keys[pygame.K_LEFT]and player.x -player_vel>0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT]and player.x +player_vel +player.get_width()<width:
            player.x += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0,5*60)==1:
                enemy.shoot()

            if collide(enemy,player):
                player.health-=10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height()> height:
                lives-=1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel,enemies)



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WINDOW.blit(bg, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WINDOW.blit(title_label, (width/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
main()