import pygame
import time
import random

pygame.init()

black = [0,0,0]
white = [255,255,255]
green = [50,205,50]
red = [255,0,0]

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('BoxHead')
clock = pygame.time.Clock()

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

        # buttons to press on the start screen_width
        pygame.draw.rect(screen, green, (150,450,100,50))

        # Text on the buttons
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Start", smallText)
        textRect.center = ( (150+(100/2)), (450+(50/2)) )
        screen.blit(textSurf, textRect)

        pygame.draw.rect(screen, red, (550,450,100,50))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Exit", smallText)
        textRect.center = ( (550+(100/2)), (450+(50/2)) )
        screen.blit(textSurf, textRect)



        pygame.display.update()
        clock.tick(15)
# Her er mit game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

game_intro()
