import pygame
import numpy as np
from pygame.draw import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.update()
clock = pygame.time.Clock()
#задаём нужные цвета в RGB
green_light = (34, 224, 0)
green_dark = (0, 77, 0)
brown_light = (194, 105, 16)
brown_dark = (51, 28, 4)
blue_light = (117, 193, 255)
blue_dark = (0, 77, 102)
pink_light = (255, 140, 157)
pink_dark = (255, 41, 77)
white = (255, 255, 255)
black = (0, 0, 0)
#рисуем землю и небо
ground = polygon(screen, green_light, [(0, 200), (0, 600), (800, 600), (800, 200)], 0)
sky = polygon(screen, blue_light, [(0, 0), (800, 0), (800, 200), (0, 200)], 0)


def house(x, y, height, width):
    '''Функция рисует домик, параметры:
    x,y - координаты левого нижнего угла домика
    height - высота домика
    width - широта домика'''
    house_main = polygon(
        screen,
        brown_light,
        [(x, y), (x + width, y), (x + width, y - height), (x, y - height)],
        0,
    )
    house_border = polygon(
        screen,
        (0, 0, 0),
        [(x, y), (x + width, y), (x + width, y - height), (x, y - height)],
        1,
    )
    house_hat = polygon(
        screen,
        pink_dark,
        [(x, y - height), (x + width, y - height), (x + width / 2, y - 3 * height / 2)],
    )
    house_hat_border = polygon(
        screen,
        (0, 0, 0),
        [(x, y - height), (x + width, y - height), (x + width / 2, y - 3 * height / 2)],
        1,
    )
    window = polygon(
        screen,
        blue_dark,
        [
            (x + 3 * width / 8, y - 3 * height / 9),
            (x + 5 * width / 8, y - 3 * height / 9),
            (x + 5 * width / 8, y - 6 * height / 9),
            (x + 3 * width / 8, y - 6 * height / 9),
        ],
        0,
    )
    window_border = polygon(
        screen,
        pink_dark,
        [
            (x + 3 * width / 8, y - 3 * height / 9),
            (x + 5 * width / 8, y - 3 * height / 9),
            (x + 5 * width / 8, y - 6 * height / 9),
            (x + 3 * width / 8, y - 6 * height / 9),
        ],
        1,
    )


def clouds(x, y, color, r):
    '''Функция рисует облака (пачкой из 6 штук), параметры:
    x,y - координаты центра левого нижнего облачка
    color - цвет облаков
    r - радиус облаков'''
    for i in range(0, 4, 1):
        circle(screen, color, (x + i * 4 * r / 3, y), r, 0)
        circle(screen, (0, 0, 0), (x + i * 4 * r / 3, y), r, 1)
    for i in range(0, 2, 1):
        circle(screen, color, (x + 4 * r / 3 + i * 4 * r / 3, y - 4 * r / 3), r, 0)
        circle(screen, (0, 0, 0), (x + 4 * r / 3 + i * 4 * r / 3, y - 4 * r / 3), r, 1)


def tree(x, y, scale):
    '''Функция рисует дерево, параметры:
    x,y - координаты левого нижнего угла ствола дерева
    scale - коэффициент подобия (можем уменьшать/увеличивать дерево в scale раз)'''
    tree_bottom = polygon(
        screen,
        brown_dark,
        [
            (x, y),
            (x + scale * 20, y),
            (x + scale * 20, y - scale * 100),
            (x, y - scale * 100),
        ],
    )
    d = 0
    h = 0
    c = 0
    for j in range(0, 2, 1):
        circle(screen, green_dark, (x - scale * 5 + d, y - 105 * scale), 20 * scale, 0)
        circle(screen, black, (x - scale * 5 + d, y - 105 * scale), 20 * scale, 1)
        d += 35 * scale
    for i in range(0, 2, 1):
        circle(screen, green_dark, (x + scale * 10, y - 130 * scale - h), 20 * scale, 0)
        circle(screen, black, (x + scale * 10, y - 130 * scale - h), 20 * scale, 1)
        h += 30 * scale
    for j in range(0, 2, 1):
        circle(screen, green_dark, (x - scale * 20 + c, y - 140 * scale), 20 * scale, 0)
        circle(screen, black, (x - scale * 20 + c, y - 140 * scale), 20 * scale, 1)
        c += 60 * scale


'''R1 = 40
R2 = 60
k = 0.0175
a1 = 67.5
a2 = 22.5


def sun(x, y, color):
    polygon(
        screen,
        color,
        [
            (x, y - R1),
            (x + R2 * np.cos(k * a1), y - R2 * np.sin(k * a1)),
            (x + R1 * np.cos(k * 45), y - R1 * np.sin(k * 45)),
            (x + R2 * np.cos(k * a2), y - R2 * np.sin(k * a2)),
            (x + R1, y),
            (x + R2 * np.cos(k * a2), y + R2 * np.sin(k * a2)),
            (x + R1 * np.cos(k * 45), y + R1 * np.sin(k * 45)),
            (x + R2 * np.cos(k * a1), y + R2 * np.sin(k * a1)),
            (x, y + R1),
            (x - R2 * np.cos(k * a1), y + R2 * np.sin(k * a1)),
            (x - np.cos(k * 45) * R1, y + np.sin(k * 45) * R1),
            (x - R2 * np.cos(k * a2), y + R2 * np.sin(k * a2)),
            (x - R1, y),
            (x - R2 * np.cos(k * a2), y - R2 * np.sin(k * a2)),
            (x - np.cos(k * 45) * R1, y - np.sin(k * 45) * R1),
            (x - R2 * np.cos(k * a1), y - R2 * np.sin(k * a1)),
        ],
    )

    polygon(
        screen,
        black,
        [
            (x, y - R1),
            (x + R2 * np.cos(k * a1), y - R2 * np.sin(k * a1)),
            (x + R1 * np.cos(k * 45), y - R1 * np.sin(k * 45)),
            (x + R2 * np.cos(k * a2), y - R2 * np.sin(k * a2)),
            (x + R1, y),
            (x + R2 * np.cos(k * a2), y + R2 * np.sin(k * a2)),
            (x + R1 * np.cos(k * 45), y + R1 * np.sin(k * 45)),
            (x + R2 * np.cos(k * a1), y + R2 * np.sin(k * a1)),
            (x, y + R1),
            (x - R2 * np.cos(k * a1), y + R2 * np.sin(k * a1)),
            (x - np.cos(k * 45) * R1, y + np.sin(k * 45) * R1),
            (x - R2 * np.cos(k * a2), y + R2 * np.sin(k * a2)),
            (x - R1, y),
            (x - R2 * np.cos(k * a2), y - R2 * np.sin(k * a2)),
            (x - np.cos(k * 45) * R1, y - np.sin(k * 45) * R1),
            (x - R2 * np.cos(k * a1), y - R2 * np.sin(k * a1)),
        ],
        1,
    )
'''
R = 50
dr = 5
def sun(x,y,n):
    '''Функция рисует солнышко, параметры:
    x,y - координаты центра
    n - количество вершин *2'''
    phi = 0
    m = []
    for i in range(n):
        m.append([x + (R + dr * (-1) ** i) * np.cos(phi), y + (R + dr * (-1) ** i) * np.sin(phi)])
        phi += 2 * np.pi / n
    polygon(screen, pink_light, m)
    polygon(screen, black, m, 1)

house(100, 400, 150, 200)
house(500, 350, 90, 120)

clouds(450, 100, white, 15)
clouds(600, 75, white, 20)
clouds(300, 75, white, 20)

tree(350, 350, 1)
tree(670, 300, 0.6)

sun(80, 80, 80)

pygame.display.update()
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
