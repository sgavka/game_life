import pygame

pygame.init()

WIN_WIDTH = 500
WIN_HEIGHT = 500
FPS = 60

clock = pygame.time.Clock()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

Rect_Width = 70
Rect_Heigth = 50
x = 0
y = WIN_HEIGHT // 2
move = "right"
acc = 1
while True:
    win.fill((255, 255, 255))
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()
    pygame.draw.rect(win, (0, 255, 255), (x, y - Rect_Heigth, Rect_Width, Rect_Heigth))
    if move == "right":
        x += acc
    if move == "left":
        x -= acc
    if x >= WIN_WIDTH - Rect_Width:
        move = "left"
        acc = 0
    if x <= 0:
        move = "right"
        acc = 0
    acc += 0.25
    pygame.display.update()

