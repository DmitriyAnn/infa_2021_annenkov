import pygame
from pygame.draw import *
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.update()
clock = pygame.time.Clock()
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
screen.fill(white)
base_face = circle(screen, yellow, (350,350), 150, 0)
left_eye_under = circle(screen, red, (270,300), 30, 0 )
left_eye_upper = circle(screen, black, (270,300), 10, 0 )
rgiht_eye_under = circle(screen, red, (430,300), 20, 0 )
right_eye_upper = circle(screen, black, (430,300), 10, 0 )
mouth = polygon(screen, black, [(270, 420), (430,420), (430, 440), (270, 440)], 0)
left_brow = polygon(screen, black, [(310, 280),(240, 210),(250, 200), (320, 270)], 0)
right_brow = polygon(screen, black, [(390, 280), (490, 230), (480, 220), (380, 270)], 0)
pygame.display.update()
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

