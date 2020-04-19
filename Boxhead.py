# Import the pygame module
import pygame
import random
import time
import math
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_s,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,
    K_d,
    MOUSEBUTTONDOWN,
    K_SPACE,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 20))
        self.img = pygame.image.load("Image/invader.png").convert()
        self.img_copy = self.img
        self.surf = pygame.transform.scale(self.img, (50,50))
        self.hp = 3
        self.score = 0
        self.direction = 0
        self.angle = 0
        self.rect = self.surf.get_rect(
                center=(SCREEN_WIDTH/2, SCREEN_HEIGHT)
            )
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -3)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 3)
        if pressed_keys[K_a]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(3, 0)
        if pressed_keys[K_LEFT]:
            self.angle += 5
        if pressed_keys[K_RIGHT]:
            self.angle -= 5
         # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    def get_x_coord(self):
        return self.rect.centerx
    def get_y_coord(self):
        return self.rect.centery
    def get_coord(self):
        return (self.rect.centerx,self.rect.centery)
    def get_width(self):
        return self.rect.w
    def get_height(self):
        return self.rect.h
    def ifCollide(self, Object1):# works
        if(
            self.rect.bottom<=Object1.rect.bottom and
            self.rect.top>=Object1.rect.top and
            self.rect.left<=Object1.rect.left and
            self.rect.right>=Object1.rect.left):
            self.rect.right= Object1.rect.left
        elif(
            self.rect.bottom<=Object1.rect.bottom and
            self.rect.top>=Object1.rect.top and
            self.rect.left<=Object1.rect.right and
            self.rect.right>=Object1.rect.right):
            self.rect.left= Object1.rect.right
        elif(
            self.rect.top<Object1.rect.bottom and
            self.rect.bottom>Object1.rect.top and
            self.rect.centery>Object1.rect.centery):
            self.rect.top= Object1.rect.bottom

        elif(
            self.rect.top<Object1.rect.top and
            self.rect.bottom>Object1.rect.top and
            self.rect.centery<Object1.rect.centery
            ):
            self.rect.bottom= Object1.rect.top


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, size, status):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface(size)
        self.hp = hp
        self.surf.fill((255, 255, 255))
        self.status = status
        x = SCREEN_WIDTH/10
        y = SCREEN_WIDTH*9/10
        if(self.status == "boss"):
            self.rect = self.surf.get_rect(
            center=(
                394,
                87
            )
        )
        else:
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(x, y),
                    10
                )
            )
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(-3, -1)
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speedx, self.speedy)
         # Keep player on the screen
        if self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.right > SCREEN_WIDTH:
            self.speedx = -self.speedx
        if self.rect.top <= 0:
            self.speedy = -self.speedy
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.speedy = -self.speedy
    def get_x_coord(self):
        return self.rect.centerx
    def get_y_coord(self):
        return self.rect.centery
    def get_coord(self):
        return (self.rect.centerx,self.rect.centery)
    def get_width(self):
        return self.rect.w
    def get_height(self):
        return self.rect.h
    def ifCollide(self, Object1):# works
        if(
            self.rect.bottom<=Object1.rect.bottom and
            self.rect.top>=Object1.rect.top and
            self.rect.left<=Object1.rect.left and
            self.rect.right>=Object1.rect.left):
            self.speedx= -self.speedx
        elif(
            self.rect.bottom<=Object1.rect.bottom and
            self.rect.top>=Object1.rect.top and
            self.rect.left<=Object1.rect.right and
            self.rect.right>=Object1.rect.right):
            self.speedx= -self.speedx
        elif(
            self.rect.top<Object1.rect.top and
            self.rect.bottom>Object1.rect.top,
            ):
            self.speedy= -self.speedy
        elif(
            self.rect.top>Object1.rect.top and
            self.rect.bottom<Object1.rect.top):
            self.speedy= -self.speedy

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

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, green)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

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
sprites = pygame.sprite.Group(Player())
bullets = pygame.sprite.Group()
enemy = pygame.sprite.Group()
for i in range(8):
    m = Enemy(enemyIMG)
    all_active_sprites.add(m)
    enemy.add(m)

def main():

    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    score = 0

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        hits = pygame.sprite.groupcollide(sprites, enemy, True, True)
        for hit in hits:
            score += random.randint(1,10)
            print(score)
            m = Enemy(enemyIMG)
            all_active_sprites.add(m)
            enemy.add(m)

        hits = pygame.sprite.groupcollide(sprites, enemy, False, True)
        if hits:
            quit()

        sprites.update(events, dt)
        all_active_sprites.update()

        screen.fill(white)
        sprites.draw(screen)
        all_active_sprites.draw(screen)
        dt = clock.tick(60)

        pygame.draw.rect(screen,green,(200,150,100,50))

        draw_text(screen, str(score), 18, screen_width / 2, 10)

        pygame.display.update()
        pygame.display.flip()


game_intro()
main()
pygame.quit()
quit()
