import pygame
import time
import random
from os import path

# Kommando til at finde path til billeder
img_dir = path.join(path.dirname(__file__), 'Image')

pygame.init()

FPS = 60
black = [0,0,0]
white = [255,255,255]
green = [0,200,0]
red = [200,0,0]

bright_red = [255,0,0]
bright_green = [0,255,0]

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height),)
pygame.display.set_caption('BoxHead')
clock = pygame.time.Clock()


playerImg = pygame.image.load(path.join(img_dir,"mand_0.png"))
enemyIMG = pygame.image.load(path.join(img_dir,"enemy_1.png"))
Bane1 = pygame.image.load(path.join(img_dir,"Bane1.png"))
Bane1_rect = Bane1.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        # Player scaling
        self.image = pygame.transform.scale(playerImg, (100,100))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - 10

        self.speedx = 0
        self.speedy = 0
    def update(self):
        # Function for updating the player, while playing
        self.speedx = 0
        self.speedy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -1
        if keys[pygame.K_RIGHT]:
            self.speedx = 1
        if keys[pygame.K_UP]:
            self.speedy = -1
        if keys[pygame.K_DOWN]:
            self.speedy = 1
        # boundary checking
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # updating the movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = pygame.transform.scale(enemyIMG, (100,100))
        self.rect = self.image.get_rect()

        # Spawn location for enemies
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - 10

        # enemies speed
        self.speedx = 0
        self.speedy = 0
    def update(self):
        # update enemies
        self.rect.y += self.speedy
        self.rect.x += self.speedx



def button(msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x,y,w,h))
            if click[0] == 1 and action != None:
                if action == "play":
                    main()
                elif action == "quit":
                    pygame.quit()
                    quit()
        else:
            pygame.draw.rect(screen, ic, (x,y,w,h))
        # buttons to press on the start screen_width

        # Text on the buttons
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)

# Function for my font
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

# Start screen for my game
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        textSurf, textRect = text_objects("BoxHead",largeText)
        textRect.center = ((screen_width/2),(screen_height-450))
        screen.blit(textSurf, textRect)


        button("Bane 1",150,450,100,50,green,bright_green,"play")
        button("Bane 2", 260,450,100,50,green,bright_green,"play")
        button("Quit",550,450,100,50,red,bright_red,"quit")

        pygame.display.update()
        clock.tick(15)

all_active_sprites = pygame.sprite.Group()
enemy = Enemy(enemyIMG)
player = Player(playerImg)
all_active_sprites.add(player)
all_active_sprites.add(enemy)

def main():

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        all_active_sprites.update()

        screen.blit(Bane1,Bane1_rect)
        all_active_sprites.draw(screen)


        pygame.display.flip()


game_intro()
main()
pygame.quit()
quit()
