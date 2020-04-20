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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super(Obstacle, self).__init__()
        self.surf = pygame.Surface((width,height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(
                center=(x, y)
            )
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
class Bullet(pygame.sprite.Sprite):
    def __init__(self, object):
        super(Bullet, self).__init__()
        self.object = object
        self.vector = pygame.Vector2()
        self.vector.y = -1
        self.vector.x = 0
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.speedx = 10
        self.speedy = 10
        self.x = object.get_x_coord()
        self.y = object.get_y_coord()
        self.a = self.vector.x
        self.b = self.vector.y
        self.angle = math.radians(self.object.angle)
        self.a = math.cos(self.angle)*self.vector.x + math.sin(self.angle)*self.vector.y
        self.b = -math.sin(self.angle)*self.vector.x + math.cos(self.angle)*self.vector.y
        self.rect = self.surf.get_rect(
                center=(self.x, self.y)
            )
    def vectorTransform(self):
       pygame.math.Vector2.rotate(self.vector, self.object.angle)
    def update(self):
        self.rect.move_ip(self.speedx*self.a, self.speedy*self.b)
        #self.rect.move_ip(self.speedx*self.vector[0], self.speedy*self.vector[1])
         # Bullet destroyed if goes beyond screen
        if(self.rect.left < 0 or
        self.rect.right > SCREEN_WIDTH or
        self.rect.top <= 0 or
        self.rect.bottom >= SCREEN_HEIGHT
          ):
          self.kill()
    def ifCollide(self, Object1):# works
        if(
            (self.rect.centerx - Object1.rect.centerx) > Object1.rect.w*1.1/2
            ):
            self.speedx= -self.speedx
        elif(
            (self.rect.centerx - Object1.rect.centerx) < Object1.rect.w*1.1/2
            ):
            self.speedy= -self.speedy

def game1():
    # Create a custom event for adding a new enemy
    screen.fill((0,0,0))
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 1000)
    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    obstacle1 = Obstacle(100,100,SCREEN_WIDTH*3/4,SCREEN_HEIGHT/2,(255,255,255))
    obstacle2 = Obstacle(100,100,SCREEN_WIDTH/2,SCREEN_HEIGHT*3/4,(255,255,255))
    obstacle3 = Obstacle(100,100,SCREEN_WIDTH/4,SCREEN_HEIGHT/3,(255,255,255))
    obstacles = pygame.sprite.Group()
    obstacles.add(obstacle1)
    obstacles.add(obstacle2)
    obstacles.add(obstacle3)
    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    boss_appeared = False
    # Variable to keep the main loop running
    # Main loop
    while True:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_SPACE:
                    bullet = Bullet(player)
                    bullets.add(bullet)

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                return False
            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy(1, (20,10),"trooper")
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            if event.type == MOUSEBUTTONDOWN:
                #print event.button
                print(pygame.mouse.get_pos())
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        # Fill the screen with black
        # Update enemy position
        enemies.update()
        bullets.update()
        #fill screen with black
        screen.fill((0, 0, 0))
        draw_text('score : '+str(player.score), pygame.font.SysFont(None, 50), (255, 255, 255), screen, SCREEN_WIDTH*4/5, 20)
        draw_text('lives : '+str(player.hp), pygame.font.SysFont(None, 50), (255, 255, 255), screen, SCREEN_WIDTH/7, 20)
        # Draw all sprites
        playerrot = pygame.transform.rotate(player.surf, player.angle)
        playerpos1 =(player.get_x_coord()-playerrot.get_width()/2,
                     player.get_y_coord()-playerrot.get_height()/2)
        screen.blit(playerrot, playerpos1)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for entity in obstacles:
            screen.blit(entity.surf, entity.rect)
        for bullet in bullets:
            screen.blit(bullet.surf, bullet.rect)
        # Check if any enemies have collided with the player
        for sprite in enemies:
                if pygame.sprite.collide_rect(player, sprite):
                    sprite.kill()
                    player.hp = player.hp - 1
                    if(player.hp == 0):
                        message_screen(screen, "LOSER")
                        player.kill()
                        time.sleep(5)
                        return True
                for bullet in bullets:
                    for enemy in enemies:
                        if pygame.sprite.collide_rect(bullet, enemy):
                            enemy.hp = enemy.hp - 1
                            if (enemy.hp == 0):
                                if(enemy.status=="boss"):
                                    message_screen(screen, "WIN")
                                    time.sleep(5)
                                    return True
                                enemy.kill()
                            bullet.kill()
                            player.score = player.score + 5

                for bullet in bullets:
                    for obstacle in obstacles:
                        if pygame.sprite.collide_rect(bullet, obstacle):
                            bullet.kill()
        for sprite in all_sprites:
            for obstacle in obstacles:
                if pygame.sprite.collide_rect(sprite, obstacle):
                    sprite.ifCollide(obstacle)
                if pygame.sprite.collide_rect(player, obstacle):
                    player.ifCollide(obstacle)
        if(player.score >= 20 and boss_appeared==False):
            new_enemy = Enemy(50, (100,100), "boss")
            print("Boss Appeared")
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            boss_appeared = True
        # Update the display
        pygame.display.flip()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(60)
def game2():
    # Create a custom event for adding a new enemy
    screen.fill((0,0,0))
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 1000)
    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    obstacle1 = Obstacle(100,350,SCREEN_WIDTH*3/4,SCREEN_HEIGHT*3/5,(255,255,255))
    obstacle2 = Obstacle(100,100,200,200,(255,255,255))
    obstacles = pygame.sprite.Group()
    obstacles.add(obstacle1)
    obstacles.add(obstacle2)
    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    boss_appeared = False
    # Variable to keep the main loop running
    # Main loop
    while True:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_SPACE:
                    bullet = Bullet(player)
                    bullets.add(bullet)

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                return False
            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy(1, (20,10),"trooper")
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            if event.type == MOUSEBUTTONDOWN:
                #print event.button
                print(pygame.mouse.get_pos())
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        # Fill the screen with black
        # Update enemy position
        enemies.update()
        bullets.update()
        #fill screen with black
        screen.fill((0, 0, 0))
        # Draw all sprites
        draw_text('score : '+str(player.score), pygame.font.SysFont(None, 50), (255, 255, 255), screen, SCREEN_WIDTH*4/5, 20)
        draw_text('lives : '+str(player.hp), pygame.font.SysFont(None, 50), (255, 255, 255), screen, SCREEN_WIDTH/7, 20)
        playerrot = pygame.transform.rotate(player.surf, player.angle)
        playerpos1 =(player.get_x_coord()-playerrot.get_width()/2,
                     player.get_y_coord()-playerrot.get_height()/2)
        screen.blit(playerrot, playerpos1)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for entity in obstacles:
            screen.blit(entity.surf, entity.rect)
        for bullet in bullets:
            screen.blit(bullet.surf, bullet.rect)
        # Check if any enemies have collided with the player
        for sprite in enemies:
                if pygame.sprite.collide_rect(player, sprite):
                    sprite.kill()
                    player.hp = player.hp - 1
                    if(player.hp == 0):
                        message_screen(screen, "LOSER")
                        time.sleep(5)
                        player.kill()
                        return True
                for bullet in bullets:
                    for enemy in enemies:
                        if pygame.sprite.collide_rect(bullet, enemy):
                            enemy.hp = enemy.hp - 1
                            if (enemy.hp == 0):
                                if(enemy.status=="boss"):
                                    message_screen(screen, "WIN")
                                    time.sleep(5)
                                    return True
                                enemy.kill()
                            bullet.kill()
                            player.score = player.score + 5
                for bullet in bullets:
                    for obstacle in obstacles:
                        if pygame.sprite.collide_rect(bullet, obstacle):
                            bullet.kill()
        for sprite in all_sprites:
            for obstacle in obstacles:
                if pygame.sprite.collide_rect(sprite, obstacle):
                    sprite.ifCollide(obstacle)
                if pygame.sprite.collide_rect(player, obstacle):
                    player.ifCollide(obstacle)
        if(player.score >= 20 and boss_appeared==False):
            new_enemy = Enemy(50, (100,100), "boss")
            print("Boss Appeared")
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            boss_appeared = True
            boss_alive = True
        # Update the display
        pygame.display.flip()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(60)
def message_screen(surface,message):
    screen.fill((0,0,0))
    draw_text(message, pygame.font.SysFont(None, 50), (255, 255, 255), surface, SCREEN_WIDTH/3+60, SCREEN_HEIGHT/3)
    pygame.display.update()
    clock.tick(60)
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:

        screen.fill((0,0,0))
        draw_text('BoxHead', pygame.font.SysFont(None, 50), (255, 255, 255), screen, SCREEN_WIDTH/3+30, SCREEN_HEIGHT/3)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(100, 400, 200, 50)
        button_2 = pygame.Rect(500, 400, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game1()
        if button_2.collidepoint((mx, my)):
            if click:
                game2()
        pygame.draw.rect(screen, (255, 255, 255), button_1)
        pygame.draw.rect(screen, (255, 255, 255), button_2)
        draw_text('level1', pygame.font.SysFont(None, 50), (0, 0, 0), screen, 150, 410)
        draw_text('level2', pygame.font.SysFont(None, 50), (0, 0, 0), screen, 550, 410)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

# Initialize pygame
pygame.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
main_menu()
