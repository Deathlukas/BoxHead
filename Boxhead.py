import pygame
import time
import random

pygame.init()

# Screen settings
screen = pygame.display.set_mode((1200,768),pygame.FULLSCREEN)
clock = pygame.time.Clock()
# Function for the Screen
def Screen():
    clock.tick(50)
    clock.tick(50)
    screen.fill((255,255,255))




# Her er mit game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
