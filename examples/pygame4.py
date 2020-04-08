import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Test')

screen.fill((255, 0, 0))
pygame.display.update()
pygame.draw

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
