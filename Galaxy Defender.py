"""
Pygame
Galaxy Defender
Author:BLANK
Members: Ruoyu CUI, Chang LIU, Jingzi YUAN

"""
import pygame
import random
import os
from os import path


img_path = path.join(path.dirname(__file__),'img')
snd_path = path.join(path.dirname(__file__),'snd')

WIDTH = 450
HEIGHT = 650
FPS = 60
supply_duration = 5000 #duration of swords
shield_duration = 5000 #duration of shileds

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GOLD = (255,215,0)
GREEN = (0,255,0)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Galaxy Defender")
clock = pygame.time.Clock()

#define the properties of text on the screen
def Text(surf, text, size, x, y):
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#define the properties of health bar and energy bar
def Bar(surf,x, y, remaining,color):
    if remaining < 0: 
        remaining = 0;
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (remaining / 100)*BAR_LENGTH #show how much health/energy there is
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,color,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

#the player has 3 lives    
def Lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+30*i
        img_rect.y = y
        surf.blit(img,img_rect)

def start_screen():
    screen.blit(background,background_rect)
    Text(screen,'GALAXY DEFENDER',40,WIDTH/2,HEIGHT/4)
    Text(screen,'Arrow keys move, Space to fire, Z to use skill',22,WIDTH/2,HEIGHT/2)
    Text(screen,'Press a key to begin',18,WIDTH/2,HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYUP:
                waiting = False
                
def gameover_screen():
    screen.blit(background,background_rect)
    Text(screen,'GAME OVER',64,WIDTH/2,HEIGHT/4)
    Text(screen,'Your score:{}'.format(score),22,WIDTH/2,HEIGHT/2)
    Text(screen,'Press a key to go back to the start page',18,WIDTH/2,HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYUP:
                waiting = False
                
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(60,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 150
        self.speedx = 0
        self.speedy = 2 #the player will continously drop down
        self.radius = 20
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks() 
        self.lives = 3
        self.hidden = False
        self.hide_time = pygame.time.get_ticks()
        self.supply = 1
        self.supply_time = pygame.time.get_ticks()

    def update(self):
        # timeout for supplies
        if self.supply >= 2 and pygame.time.get_ticks() - self.supply_time > supply_duration:
            self.supply -= 1
            self.supply_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-150
            newshield()
        self.speedx = 0
        self.speedy = 2
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx -= 5
        if keystate[pygame.K_RIGHT]:
            self.speedx += 5
        if keystate[pygame.K_UP]:
            self.speedy -= 5
        if keystate[pygame.K_DOWN]:
            self.speedy += 5
        if keystate[pygame.K_SPACE] and self.rect.bottom < HEIGHT :
            self.shoot()
        if keystate[pygame.K_z] and self.rect.bottom < HEIGHT:
            self.use_skill()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0 :
            self.rect.top = 0

    def get_supplies(self):
        self.supply += 1
        self.supply_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now 
            if self.supply == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.supply >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def use_skill(self) :
        global energy
        if energy >= 100 :
            for i in range(0,9) :
                skill = Skill(25+50*i,self.rect.top)
                all_sprites.add(skill)
                skills.add(skill)
            shoot_sound.play()
            energy=0

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+200)

#bullets that released by the player        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

#when the energy bar is full, the player can release a skill to clear all the enemies and obstacles on the screen
class Skill(pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -8
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

#the shield will circle around the player and protect the player from one hit by the enemy or the obstacle           
class Shield(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shield_img,(80,90))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.start_time = pygame.time.get_ticks()
        self.speedx = 0
        self.speedy = 2
        
    def update(self):
        if pygame.time.get_ticks()-self.start_time > shield_duration :
            self.kill()
        self.speedx = 0
        self.speedy = 2
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx -= 5
        if keystate[pygame.K_RIGHT]:
            self.speedx += 5
        if keystate[pygame.K_UP]:
            self.speedy -= 5
        if keystate[pygame.K_DOWN]:
            self.speedy += 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH+10:
            self.rect.right = WIDTH+10
        if self.rect.left < -10:
            self.rect.left = -10
        if self.rect.top < -5 :
            self.rect.top = -5
 
#define the properties of supplies           
class Supplies(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','sword'])
        self.image = pygame.transform.scale(supplies_images[self.type],(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = random.randrange(2,3)
        self.speedx = random.randrange(-2,2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x+=self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()
            
        
class enemy(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image_orin = pygame.transform.scale(enemy_img,(45,55))
        self.image_orin.set_colorkey(BLACK)
        self.image = self.image_orin.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,3)
        self.speedx = random.randrange(-3,3)
        self.radius = int(self.rect.width * 0.85 / 2)
        self.last_update = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks() 
        self.shoot_delay = random.randrange(2000,3000,500)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 :
            self.kill()
            newenemy()
        if self.rect.left<0 or self.rect.right>WIDTH :
            self.speedx=-self.speedx
        self.shoot()
        
    def shoot(self): # the enemy shoots
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullete = enemybullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullete)
            enemybullets.add(bullete) 
            
class enemybullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_path,'enemybullet.png')).convert()
        self.image.set_colorkey()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 3+score//2000 # when the score gets higher, the speed of enemybullets will increase
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        wg=random.randrange(40,80,10)
        self.image_orin = pygame.transform.scale(stone_img,(wg,wg))
        self.image_orin.set_colorkey(BLACK)
        self.image = self.image_orin.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx=random.randrange(-1,1)
        self.speedy=random.randrange(1,(score//2000+5)) #when the score gets higher, the obstacles drop faster
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self): #the obstacles rotate when dropping down
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orin,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()
            newob()
            
class Bottom_line(pygame.sprite.Sprite):
   def __init__(self): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(line_img,(WIDTH,20))
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH / 2 
        self.rect.bottom = HEIGHT

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
#the following 3 functions create new related objects           
def newob():
    obs = Obstacle()
    all_sprites.add(obs)
    Obs.add(obs)
    
def newshield() :
    s=Shield()
    s.start_time = pygame.time.get_ticks()
    s.rect.centerx = player.rect.centerx
    s.rect.bottom = player.rect.bottom
    all_sprites.add(s)
    shields.add(s)
       
def newenemy() :
    e = enemy()
    all_sprites.add(e)
    enemys.add(e)

# Load all game graphics
background = pygame.image.load(path.join(img_path,'background.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_path,'blueship.png')).convert()
enemy_img = pygame.image.load(path.join(img_path,'redfighter.png')).convert()
stone_img = pygame.image.load(path.join(img_path,'starbase.png')).convert()
player_mini_img = pygame.transform.scale(player_img,(20,20))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_path,'bullet.png')).convert()
shield_img = pygame.image.load(path.join(img_path,'shield.png')).convert()
line_img = pygame.image.load(path.join(img_path,'line.png')).convert()
supplies_images = {}
supplies_images['shield'] = pygame.image.load(path.join(img_path,'goldshield.png')).convert()
supplies_images['sword'] = pygame.image.load(path.join(img_path,'goldsword.png')).convert()

#create the exposion animations
explosion_anim = {}
explosion_anim['big'] = []
explosion_anim['small'] = []
explosion_anim['player'] = []
for i in range(8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_path,filename)).convert()
    img.set_colorkey(BLACK)
    img_big = pygame.transform.scale(img,(75,75))
    explosion_anim['big'].append(img_big)
    img_small = pygame.transform.scale(img,(32,32))
    explosion_anim['small'].append(img_small)
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_path,filename)).convert()
    img.set_colorkey(BLACK)
    img_hg = pygame.transform.scale(img,(150,150))
    explosion_anim['player'].append(img_hg)


# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_path,'laser_shoot.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_path,'shield.wav'))
supply_sound = pygame.mixer.Sound(path.join(snd_path,'get_supplies.wav'))
expl_sounds1 = pygame.mixer.Sound(os.path.join(snd_path,'explosion1.wav'))
expl_sounds2 = pygame.mixer.Sound(os.path.join(snd_path,'explosion2.wav'))
player_die_sound = pygame.mixer.Sound(path.join(snd_path,'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_path,'galaxydefender.ogg'))
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        start_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        Obs = pygame.sprite.Group()
        enemys = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        skills=pygame.sprite.Group()
        enemybullets = pygame.sprite.Group()
        supplies = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        player = Player()
        line=Bottom_line()
        all_sprites.add(player,line)
        score = 0
        for i in range(6):
            newob()
        for i in range(5):
            newenemy()

        energy = 0
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    #check if the player hits enemies
    hits = pygame.sprite.spritecollide(player,enemys,True)
    for hit in hits:
        score+= 50
        player.health -= hit.radius 
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'big')
        all_sprites.add(expl)
        newenemy()
        if player.health <= 0:
            energy=0
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            if player.lives > 0 :
                player.health = 100
                
    #check if the player hits the enemybullets
    hits = pygame.sprite.spritecollide(player,enemybullets,True)
    for hit in hits:
        player.health -= 5 
        expl_sounds1.play()
        expl = Explosion(hit.rect.center,'small')
        all_sprites.add(expl)
        if player.health <= 0:
            energy=0
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            if player.lives > 0 :
                player.health = 100
                
    # check if bullets hit the enemies
    hits = pygame.sprite.groupcollide(enemys,bullets,True,True)
    for hit in hits:
        score += 50 
        if energy<100 :
            energy+= 5
            if energy>100 :
                energy=100
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'big')
        all_sprites.add(expl)
        if random.random() > 0.9: #randomly create supplies
            create_supps = Supplies(hit.rect.center)
            all_sprites.add(create_supps)
            supplies.add(create_supps)
        newenemy()
    
    #check if skills hit enemies 
    hits = pygame.sprite.groupcollide(enemys,skills,True,False)
    for hit in hits:
        score += 50 - hit.radius
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'big')
        all_sprites.add(expl)
        if random.random() > 0.98:
            create_supps = Supplies(hit.rect.center)
            all_sprites.add(create_supps)
            supplies.add(create_supps)
        newenemy()
      
    #check if enemies hit the shield
    hits = pygame.sprite.groupcollide(enemys,shields,True,True)
    for hit in hits:
        score += 50 - hit.radius
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'big')
        all_sprites.add(expl)
        if random.random() > 0.9:
            create_supps = Supplies(hit.rect.center)
            all_sprites.add(create_supps)
            supplies.add(create_supps)
        newenemy()
    
    #if enemybullets hit the shield, enemybullets will disappear
    hits = pygame.sprite.groupcollide(enemybullets,shields,True,False)

    #if enemybullets hit skills, enemybullets will disappear
    hits = pygame.sprite.groupcollide(enemybullets,skills,True,False)
    
    #check if obstacles hit shields
    hits = pygame.sprite.groupcollide(Obs,shields,True,True)
    for hit in hits:
        score += 50 - hit.radius
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'big')
        all_sprites.add(expl)
        if random.random() > 0.9:
            create_supps = Supplies(hit.rect.center)
            all_sprites.add(create_supps)
            supplies.add(create_supps)
        newob()

    #check if obstacles hit the skills
    hits = pygame.sprite.groupcollide(Obs,skills,True,False)
    for hit in hits:
        score += 50 - hit.radius
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'big')
        all_sprites.add(expl)
        if random.random() > 0.98:
            create_supps = Supplies(hit.rect.center)
            all_sprites.add(create_supps)
            supplies.add(create_supps)
        newob()
        
    # check to see if an obstacle hit the player
    hits = pygame.sprite.spritecollide(player,Obs,True,pygame.sprite.collide_circle)
    for hit in hits:
        score+=hit.radius
        player.health -= hit.radius
        expl_sounds2.play()
        expl = Explosion(hit.rect.center,'small')
        all_sprites.add(expl)
        newob()
        if player.health <= 0:
            energy=0
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            if player.lives > 0 :
                player.health = 100
     
    #check if the player hits the bottomline           
    hits = pygame.sprite.collide_rect(player,line)
    if hits:
        player.health -= 100
        player.lives -= 1
        energy=0
        player_die_sound.play()
        death_explosion = Explosion(player.rect.center,'player')
        all_sprites.add(death_explosion)
        player.hide()
        if player.lives > 0 :
            player.health = 100

    # check if the player hits supplies
    hits = pygame.sprite.spritecollide(player,supplies,True)
    for hit in hits:
        if hit.type == 'shield':
            shield_sound.play()
            newshield()
        if hit.type == 'sword':
            supply_sound.play()
            player.get_supplies()

    # if the player dies and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        gameover_screen()
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    Text(screen, str(score), 18, WIDTH/2, 10)
    Bar(screen,5,25,player.health,GREEN)
    Bar(screen,WIDTH-105,25,energy,GOLD)
    Lives(screen,5,5,player.lives,player_mini_img)
    if energy == 100 :
        Text(screen, str("Ready!"), 20, WIDTH-78, 10)
    # after drawing everything, flip the display
    pygame.display.flip()

os._exit(0)
