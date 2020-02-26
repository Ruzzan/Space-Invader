import pygame
from pygame import mixer
import random
import math
import os

os.getcwd()

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init() #initialize the pygame

WIN_WIDTH = 600
WIN_HEIGHT = 450
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # create the screen

#background image
background = pygame.image.load('assets/background.png').convert()
backgroundY = 0

# window title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)

# players 
playerImg = pygame.image.load('assets/ufo.png')
#initial position of player
playerX   = 300
playerY   = 370
# this will handle the change increase/decrease in speed
playerX_change = 0

# enemy 
enemyImg= []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/enemy.png'))
    #initial position of enemy
    enemyX.append(random.randint(0,WIN_HEIGHT-64))
    enemyY.append(random.randint(10,50))
    # this will handle the change increase/decrease in speed
    enemyX_change.append(0.3)
    enemyY_change.append(20)

# bullet 
# READY => you can't see the bullet on the screen (its reloading)
# FIRE => the bullet is curently moving
bulletImg = pygame.image.load('assets/bullet.png')
#initial position of bullet
bulletX   = 0
bulletY   = 370
bulletX_change = 0.4
bulletY_change = 0.5
bullet_state = 'ready'

# explosion 
explosionImg = pygame.image.load('assets/explosion.png')
expolsionX = 0
expolsionY = 0

# Score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf',20)
scoreX, ScoreY = 10,10

def player(posX, posY):
    screen.blit(playerImg, (posX, posY))

def enemy(posX, posY, index):
    screen.blit(enemyImg[index], (posX, posY))

def  fireBullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def explosion(x,y):
    return screen.blit(explosionImg, (x+100, y-20))

# this will calculate distance of enemy and moving bullet and return boolean 
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1-y1,2))+(math.pow(x2-y2,2)))
    if distance < 50: # collision occoured!!
        mixer.music.load('explosion.mp3')
        mixer.music.play()
        return True
    else:
        return False

def showScore(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def gameover():
    game_over_font = pygame.font.Font('freesansbold.ttf', 62)
    game_over_text = game_over_font.render("Game Over", True, (255,255,255))
    screen.blit(game_over_text, (150,250))

# Game loop
is_running = True
while is_running:
    #screen.fill((13, 16, 48)) # this is the background color
    #background image:
    rel_Y = backgroundY % background.get_rect().height
    screen.blit(background, (0,rel_Y - background.get_rect().height))
    if rel_Y < WIN_HEIGHT:
        screen.blit(background, (0, rel_Y))
    backgroundY += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False   
        
        # check keystroke to move the player 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.9

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9
                
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    mixer.music.load('shoot.mp3')
                    mixer.music.play()
                    # Get the current x coordinate of spaceship
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # controlling the boundaries of player
    if playerX <= 0:
        playerX = 0
    elif playerX >= (WIN_WIDTH-62): # width of window (600) - 62px of spaceship
        playerX = (WIN_WIDTH-62)

    # control movement of enemy 
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameover()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= (WIN_WIDTH-64):
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        #collision 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 370 # reset the bullet position
            bullet_state = 'ready' # change state to fire 
            score_value += 1 # increase the score 
            # explosion 
            expolsionX = enemyX[i]
            expolsionY = enemyY[i]
            explosion(expolsionX, expolsionY)
            # generate enemy in random position
            enemyX[i]   = random.randint(0,WIN_HEIGHT-64)
            enemyY[i]   = random.randint(10,50)
            # num_of_enemies -= 1
        # display enemy
        enemy(enemyX[i], enemyY[i], i)

    # BUllet movement 
    if bulletY <= 0:
        bulletY = 370
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # player 
    player(playerX, playerY)

    # show score
    showScore(scoreX, ScoreY)

    pygame.display.update() #updating the display in every iteration

