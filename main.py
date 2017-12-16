import pygame

from implementation import *
from pygame.locals import *

pygame.init()

# Set up the window
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height), 0, 32)
pygame.display.set_caption('TEST')

# Set up the colors
Aqua = (0, 255, 255)
Black = (0, 0, 0)
Blue = (0, 0, 255)
Fuchsia = (255, 0, 255)
Gray = (128, 128, 128)
Green = (0, 128, 0)
Lime = (0, 255, 0)
Maroon = (128, 0, 0)
Navy_Blue = (0, 0, 128)
Olive = (128, 128, 0)
Purple = (128, 0, 128)
Red = (255, 0, 0)
Silver = (192, 192, 192)
Teal = (0, 128, 128)
White = (255, 255, 255)
Yellow = (255, 255, 0)

# Draw on the surface object

# gameDisplay.fill(White)  # method to fill the surface object
# pygame.draw.polygon(gameDisplay, Green, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
# pygame.draw.line(gameDisplay, Blue, (60, 60), (120, 60), 4)
# We can use aaline but it will not have the width of the line
# pygame.draw.line(gameDisplay, Blue, (120, 60), (60, 120))
# pygame.draw.line(gameDisplay, Blue, (60, 120), (120, 120), 4)
# pygame.draw.circle(gameDisplay, Blue, (300, 50), 20, 0)
# pygame.draw.ellipse(gameDisplay, Red, (300, 250, 40, 80), 1)
# pygame.draw.rect(gameDisplay, Red, (200, 150, 100, 50))

# pixObj = pygame.PixelArray(gameDisplay)
# pixObj[480][380] = Black
# pixObj[482][382] = Black
# pixObj[484][384] = Black
# pixObj[486][386] = Black
# pixObj[488][388] = Black
# del pixObj

# Animation
FPS = 30
fpsClock = pygame.time.Clock()
catImg = pygame.image.load('cat.png')


def cat(x, y):
    gameDisplay.blit(catImg, (x, y))


# def esc():


# The game loop
def game_loop():
    catX = 10
    catY = 10
    x_change = 0
    y_change = 0
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameExit = True

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    x_change = -5
                elif event.key == K_RIGHT:
                    x_change = 5
                elif event.key == K_UP:
                    y_change = -5
                elif event.key == K_DOWN:
                    y_change = 5
                    # elif event.key == K_ESCAPE:
                    #   esc()
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    x_change = 0
                if event.key == K_UP or event.key == K_DOWN:
                    y_change = 0
            print(event)
        if catX + x_change > display_width - catImg.get_rect().width or catX + x_change < 0:
            x_change = 0
        if catY + y_change > display_height - catImg.get_rect().height or catY + y_change < 0:
            y_change = 0
        catX += x_change
        catY += y_change
        gameDisplay.fill(White)
        cat(catX, catY)
        pygame.display.update()
        fpsClock.tick(FPS)


# start, goal = (1, 4), (7, 8)
# cameFrom, costSoFar = a_star_search(diagram4, start, goal)
# path = reconstruct_path(cameFrom, start, goal)
# draw_grid(diagram4, width=3, path=path, start=start, goal=goal)
# print()

if __name__ == '__main__':
    game_loop()
    pygame.quit()
    quit()
