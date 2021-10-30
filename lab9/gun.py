import math
from random import choice, randint
from time import sleep
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GUN_COLOR = (39, 100, 59)

GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
text_font = pygame.font.SysFont('courier new', 20)
points = 0
tank = pygame.image.load('tank.png').convert_alpha()  # загружаем картинку танка
width_of_tank = 50  # установленные размеры чтобы не сжался
tank = pygame.transform.scale(tank, (2 * width_of_tank, width_of_tank))  # создаем отраженную картинку
tank.set_colorkey('white')  # убираем белый фон


class Ball:
    def __init__(self, x=20, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 20

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx * 30 / FPS
        self.y += self.vy * 30 / FPS
        self.vy += 0.8 * 30 / FPS
        if self.x + self.r > WIDTH and self.vx > 0 or self.x - self.r < 0 and self.vx < 0:
            self.vx = -0.6 * self.vx
            self.vy = 0.6 * self.vy
            self.live -= 1  # если <= 0, то удаление
        if self.y + self.r > HEIGHT and self.vy > 0:
            self.live -= 1
            self.vy = -0.6 * self.vy
            self.vx = 0.6 * self.vx

    def draw(self):
        """рисует цель в виде круга"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (obj.r + self.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.shots = 0
        self.x = 20
        self.y = 450
        self.vx = 0  # скорость принимает -1, 0, 1 и показывает направление движения
        self.vy = 0  # скорость принимает -1, 0, 1 и показывает направление движения
        self.v0 = 4  # модуль скорости по каждой координате
        self.way = 1  # показывает куда до этого ехал танк
        self.width = 4
        self.high = 50
        self.f_power = 15
        self.f_on = 0
        self.an = 0
        self.color = GUN_COLOR
        self.balls = []
        self.bullet = 0

    def fire_start(self):
        """начало заряжания"""
        self.f_on = 1

    def fire_end(self, event_gun):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.shots += 1
        self.bullet += 1
        new_ball = Ball(self.x, self.y)
        self.an = math.atan2((event_gun.pos[1] - new_ball.y), (event_gun.pos[0] - new_ball.x))
        new_ball.vx = self.f_power * math.cos(self.an)
        new_ball.vy = self.f_power * math.sin(self.an)
        self.balls.append(new_ball)
        self.f_on = 0
        self.f_power = 15
        self.high = 30

    def input_moving(self, event_gun):
        """Считывает с клавиатуры куда двигаться"""
        if event.type == pygame.KEYDOWN:
            if event_gun.key == pygame.K_LEFT:
                self.vx = -1
            elif event_gun.key == pygame.K_RIGHT:
                self.vx = 1
            else:
                self.vx = 0

            if event_gun.key == pygame.K_UP:
                self.vy = -1
            elif event_gun.key == pygame.K_DOWN:
                self.vy = 1
            else:
                self.vy = 0
        else:
            self.vx = 0
            self.vy = 0

    def move(self):
        """Движение танка в зависимости от направления мыши и нажатия кнопок"""
        if self.vx != 0:
            self.x += self.vx * self.v0 * 30 // FPS
        if self.vy != 0:
            self.y += self.vy * self.v0 * 30 // FPS

    def targeting(self, event_gun):
        """Прицеливание. Зависит от положения мыши."""
        if event_gun:
            if event_gun.pos[0] - self.x > 0:
                self.an = math.atan((event_gun.pos[1] - self.y) / (event_gun.pos[0] - self.x))
            elif event_gun.pos[0] - self.x < 0:
                self.an = math.pi + math.atan((event_gun.pos[1] - self.y) / (event_gun.pos[0] - self.x))
            elif event_gun.pos[0] - self.x == 0 and event_gun.pos[1] - self.y >= 0:
                self.an = math.pi / 2
            elif event_gun.pos[0] - self.x == 0 and event_gun.pos[1] - self.y <= 0:
                self.an = - math.pi / 2

    def draw(self):
        """рисует пушку"""
        if self.vx == 1 or (self.way == 1 and self.vx == 0 and self.vy == 0):
            screen.blit(tank, (self.x - width_of_tank, self.y - width_of_tank // 2))
            self.way = 1
        elif self.vx == -1 or (self.way == 2 and self.vx == 0 and self.vy == 0):
            screen.blit(pygame.transform.flip(tank, True, True), (self.x - width_of_tank, self.y - width_of_tank // 2))
            self.way = 2
        elif self.vy == 1 or (self.way == 3 and self.vy == 0):
            screen.blit(pygame.transform.rotate(tank, -90), (self.x - width_of_tank // 2, self.y - width_of_tank))
            self.way = 3
        elif self.vy == -1 or self.way == 4:
            screen.blit(pygame.transform.rotate(tank, 90), (self.x - width_of_tank // 2, self.y - width_of_tank))
            self.way = 4

        pygame.draw.polygon(screen, self.color, [(self.x, self.y), (
            self.x + self.width * math.sin(self.an), self.y - self.width * math.cos(self.an)), (
                                                     self.x + self.width * math.sin(self.an) + self.high * math.cos(
                                                         self.an),
                                                     self.y - self.width * math.cos(self.an) + self.high * math.sin(
                                                         self.an)), (self.x + self.high * math.cos(self.an),
                                                                     self.y + self.high * math.sin(self.an))])
        pygame.draw.polygon(screen, 'black', [(self.x, self.y), (
            self.x + self.width * math.sin(self.an), self.y - self.width * math.cos(self.an)), (
                                                     self.x + self.width * math.sin(self.an) + self.high * math.cos(
                                                         self.an),
                                                     self.y - self.width * math.cos(self.an) + self.high * math.sin(
                                                         self.an)), (self.x + self.high * math.cos(self.an),
                                                                     self.y + self.high * math.sin(self.an))], 1)

    def hit(self):
        """Попадание шарика в цель"""
        screen.fill('white')
        text_surface = text_font.render('Вы уничтожили цель за ' + str(self.shots) + ' выстрелов', False, BLACK)
        screen.blit(text_surface, (WIDTH // 4, HEIGHT // 3))
        pygame.display.update()
        self.shots = 0
        sleep(1)

    def power_up(self):
        """увеличивает мощность выстрела и длину пушки"""
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
                self.high += 2
            self.color = 'orange'
        else:
            self.color = GUN_COLOR


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.r = randint(2, 50)
        self.x = randint(3 * WIDTH // 4, WIDTH - self.r)
        self.y = randint(HEIGHT // 2, 7 * HEIGHT // 8 - self.r)
        self.vx = randint(-10, 10)
        self.vy = randint(-20, 20)
        self.color = 'orange'

    def move(self):
        """обработка координат цели"""
        self.x += self.vx * 30 / FPS
        self.y += self.vy * 30 / FPS
        self.vy += 0.5 * 30 / FPS
        if self.x + self.r >= WIDTH and self.vx > 0 or self.x - self.r <= WIDTH // 2 and self.vx < 0:
            self.vx = -self.vx
        if self.y + self.r >= 3 * HEIGHT // 4 and self.vy > 0 or self.y - self.r <= 0 and self.vy < 0:
            self.vy = -self.vy

    def draw(self):
        """Прорисовка цели"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, 'black', (self.x, self.y), self.r, 1)


def draw_everything():
    """рисует все элементы"""
    screen.fill('white')
    text_surface = text_font.render('Всего попаданий: ' + str(points), False, BLACK)
    screen.blit(text_surface, (0, 0))
    gun.draw()
    target_1.draw()
    target_2.draw()
    for num_ball in gun.balls:
        num_ball.draw()
    pygame.display.update()


def deleting():
    """удаление ненужных шариков"""
    copy_of_balls = gun.balls.copy()
    counter = 0
    for b in copy_of_balls:
        if b.live <= 0:
            del gun.balls[counter]
        else:
            counter += 1


clock = pygame.time.Clock()
gun = Gun()
target_1 = Target()
target_2 = Target()
finished = False


def kill_everybody():
    """После этого все шарики удалятся"""
    for b in gun.balls:
        b.live = 0


def processing():
    """изменение параметров элементов"""
    gun.power_up()
    for b in gun.balls:
        b.move()
        if b.hit_test(target_1) or b.hit_test(target_2):
            gun.hit()
            kill_everybody()
            return points + 1, Target(), Target()
    gun.move()
    target_1.move()
    target_2.move()
    return points, target_1, target_2


while not finished:
    draw_everything()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targeting(event)

        gun.input_moving(event)
    points, target_1, target_2 = processing()
    deleting()

pygame.quit()
