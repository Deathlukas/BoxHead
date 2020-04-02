import pygame
import time
import random
import math
from pygame.math import Vector2
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
bulletImg = pygame.image.load(path.join(img_dir, "bullet.png"))
Bane1 = pygame.image.load(path.join(img_dir,"Bane1.png"))
Bane1_rect = Bane1.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))

        self.image.set_colorkey((0, 0, 0))
        pygame.draw.polygon(self.image, pygame.Color('dodgerblue'), ((0,0), (32, 16), (0, 32)))
        self.org_image = self.image.copy()
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.rect = self.image.get_rect(center=(screen_width/2, screen_height - 30))
        self.pos = pygame.Vector2(self.rect.center)
        self.speedy = 0
        self.speedx = 0
    def update(self, events, dt):
        self.speedy = 0
        self.speedx = 0
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.groups()[0].add(Projectile(self.rect.center, self.direction.normalize()))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.angle += 3
        if pressed[pygame.K_RIGHT]:
            self.angle -= 3
        if pressed[pygame.K_w]:
            self.speedy -= 1
        if pressed[pygame.K_s]:
            self.speedy += 1
        if pressed[pygame.K_a]:
            self.speedx -= 1
        if pressed[pygame.K_d]:
            self.speedx += 1

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.y += self.speedy
        self.rect.x += self.speedx

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = pygame.transform.scale(enemyIMG, (100,100))
        self.rect = self.image.get_rect()

        # Spawn location for enemies
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - 150

        # enemies speed
        self.speedx = 0
        self.speedy = 0
    def update(self):
        # update enemies
        self.rect.y += self.speedy
        self.rect.x += self.speedx

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, pygame.Color('orange'), (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, events, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

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
bullets = pygame.sprite.Group()
enemy = Enemy(enemyIMG)
all_active_sprites.add(enemy)

def main():

    pygame.init()
    sprites = pygame.sprite.Group(Player())
    clock = pygame.time.Clock()
    dt = 0

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
        sprites.update(events, dt)
        screen.fill(white)
        sprites.draw(screen)
        all_active_sprites.draw(screen)
        pygame.display.update()
        dt = clock.tick(60)



game_intro()
main()
pygame.quit()
quit()
