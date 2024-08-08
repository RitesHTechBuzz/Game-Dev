import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()

#create the screen 
screen = pygame.display.set_mode((800,600))

#background 
background = pygame.image.load('background.png')

#background sound 

mixer.music.load('backgroundsong.mp3')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("MyFirstGame")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerx_change=0


#Enemy

enemyimg =[]
enemyX = []
enemyY = []
enemyx_change = []
enemyy_change = []
num_enemy = 6

for i in range(num_enemy):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyx_change.append(2.0)
    enemyy_change.append(40)

#bullet
#ready -> can't see the bullet on screen 
#fire -> the bullet is actually fired
bulletimg = pygame.image.load('bomb.png')
bulletX = 0
bulletY = 480
bulletx_change=0
bullety_change=10
bullet_state ="ready"

#score

score_value =0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over 
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_overtext():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200,250) )



def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score, (x,y) )

def player(x,y):
    screen.blit(playerimg, (x,y) )

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x,y) )    

def fire_bullet(x,y):
       global bullet_state
       bullet_state="fire" 
       screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance <27:
        return True
    else:
        return False
    
#Game Loop
running = True
while running:
    #RGB  = Red Green Blue
    screen.fill( (0,0,0) )
    #Background Image
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            #if keystroke is pressed check if its right or left
        if event.type== pygame.KEYDOWN:
            if event.key== pygame.K_a:
               playerx_change=-4.0
            if event.key== pygame.K_d:
                playerx_change=4.0
            if event.key== pygame.K_SPACE:
                if bullet_state == "ready":
                 bullet_sound = mixer.Sound('laser.wav')
                 bullet_sound.play()
                 bulletX=playerX
                fire_bullet(bulletX,bulletY) 

        if event.type== pygame.KEYUP:
            if  event.key == pygame.K_a or event.key == pygame.K_d:
             playerx_change=0.0


# setting boundaries for player
    playerX+=playerx_change
    
    if playerX <=0:
         playerX=0
    elif playerX >=736:
        playerX=736


#setting boundaries for enemy + enemy movement
    for i in range(num_enemy): 

         #game over
         if enemyY[i] > 445 :
             for j in  range(num_enemy): 
                 enemyY[j]=2000
                 game_overtext()
                 break
               
         enemyX[i]+=enemyx_change[i]

         if enemyX[i] <=0:
             enemyx_change[i]=2.0
             enemyY[i]+=enemyy_change[i]

        
         elif enemyX[i] >=736:
            enemyx_change[i]=-2.0
            enemyY[i]+=enemyy_change[i]

             #collision 
         collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
         if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state="ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
         enemy(enemyX[i],enemyY[i],i)   


   
 #bullet movement
        
    if bulletY <= 0:
        bulletY=480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=bullety_change 

   

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
    
