import pygame
import time
import random
from os import path

# Kommando til at finde path til billeder
img_dir = path.join(path.dirname(__file__), 'Image')

pygame.init()

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

playerImg = pygame.image.load(path.join(img_dir,"mand.png"))

def player1(x,y):
    screen.blit(playerImg,(x,y))

def button(msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x,y,w,h))
            if click[0] == 1 and action != None:
                if action == "play":
                    game_loop()
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


        button("Start",150,450,100,50,green,bright_green,"play")
        button("Quit",550,450,100,50,red,bright_red,"quit")


        pygame.display.update()
        clock.tick(15)
# Her er mit game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

def game_loop():
    x = (450)
    y = (350)

    x_change = 0
    y_change = 0

    gameExit  = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -5
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                    x_change = 0

        x += x_change
        y += y_change
        screen.fill(white)
        player1(x,y)



        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
