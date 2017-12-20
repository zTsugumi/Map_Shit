import pygame
import heapq
from pygame.locals import *

pygame.init()

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


class Hero(pygame.Surface):
    def __init__(self, image, heroX=0, heroY=0):
        super().__init__(image.get_size())
        self.image = image
        self.heroX = heroX
        self.heroY = heroY
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = pygame.Rect(heroX, heroY, self.width, self.height)

    def display(self):
        gameDisplay.blit(self.image, (self.heroX, self.heroY))

    def move(self, coord):
        self.heroX = coord[0]
        self.heroY = coord[1]
        self.rect = pygame.Rect(self.heroX, self.heroY, self.width, self.height)


class Map(pygame.Surface):
    def __init__(self, image, mapX=0, mapY=0):
        super().__init__(image.get_size())
        self.image = image
        self.mapX = mapX
        self.mapY = mapY
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = pygame.Rect(mapX, mapY, self.width, self.height)

    def display(self):
        gameDisplay.blit(self.image, (self.mapX, self.mapY))


# Set up the window
dotaImg = pygame.image.load('Game_map_7.00 (Color_Blinded).jpg')
dotaMap = Map(dotaImg, 0, 0)

display_width = dotaMap.width
display_height = dotaMap.height
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Minimap Project')

heroImg = pygame.image.load('Invoker_minimap_icon.png')
hero = Hero(heroImg, 66, 795)

FPS = 30
fpsClock = pygame.time.Clock()


def in_bounds(coord):
    (x, y) = coord
    return 0 <= x < dotaMap.width - hero.width and 0 <= y < 1011 - hero.height


def passable(coord):
    return 190 <= dotaImg.get_at(coord)[0] <= 205


def neighbors(coord):
    (x, y) = coord
    results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1),
               (x + 1, y + 1)]
    if (x + y) % 2 == 0:
        results.reverse()  # aesthetics
    results = filter(in_bounds, results)
    results = filter(passable, results)
    return results


def heuristic(start, current, goal):
    (x1, y1) = current
    (x2, y2) = goal
    (x3, y3) = start
    dx1 = x1 - x2
    dy1 = y1 - y2
    dx2 = x3 - x2
    dy2 = y3 - y2

    # Tie-breaking cross-product added to heuristic
    cross = abs(dx1 * dy2 - dx2 * dy1)
    # p = 1 / expected steps for the path
    p = 1 / 1000
    return abs(dx1) + abs(dy1) - min(abs(dx1), abs(dy1)) + cross * p


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def a_star_search(start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(start, next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def path_finding():
    goal = pygame.mouse.get_pos()
    print(gameDisplay.get_at(goal))
    # have to process if not passable
    # we're gonna use the BFS to find the nearest passable point to go
    if not in_bounds(goal):
        return None
    start = (hero.heroX, hero.heroY)
    came_from = a_star_search(start, goal)
    path = reconstruct_path(came_from, start, goal)
    draw_path(path)


def draw_path(path):
    for coord in path:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 3 and in_bounds(pygame.mouse.get_pos()):
                path_finding()
                return
        dotaImg.set_at(coord, Red)
        dotaMap.display()
        hero.move(coord)
        hero.display()
        pygame.display.update()


def game_loop():
    dotaMap.display()
    hero.display()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                # Right mouse
                if event.button == 3:
                    path_finding()
            if event.type == VIDEORESIZE:
                pass

            print(event)
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    game_loop()
