import pygame
from pygame.draw import *
from random import randint
pygame.init()

# задаем фпс и параметры экрана
FPS = 60
HEIGHT = 900
WIDTH = 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# количество очков, набранных игроком
POINTS = 0

# кортежи для фигур-мишеней
balls = []
squares = []

# словарь для рейтинга игроков
dict_rating={}


def new_ball():
    """ Функция создает новую мишень-круг с параметрами
        х - начальная координата центра по ОХ
        у - начальная координата центра по ОУ
        r - радиус мишени
        dx, dy - скорость вдоль ОХ и ОУ соответственно
        t - время жизни мишени
        color - цвет мишени """
    x = randint(100, WIDTH - 100)
    y = randint(100, HEIGHT)
    r = randint(20, 100)
    dx = randint(-10, 10)
    dy = randint(-10, 10)
    color = COLORS[randint(0, 5)]
    t = 3000
    balls.append([x, y, r, dx, dy, color, t])


def new_square():
    """ Функция создает новую мишень-квадрат с параметрами
        х - начальная координата центра по ОХ
        у - начальная координата центра по ОУ
        а - сторона квадрата
        dx, dy - скорость вдоль ОХ и ОУ соответственно
        t - время жизни мишени
        color - цвет мишени """
    x = randint(100, WIDTH - 100)
    y = randint(100, HEIGHT)
    a = randint(50, 100)
    dx = randint(-6, 6)
    dy = randint(-6, 6)
    t = 3000
    color = COLORS[randint(0, 5)]
    squares.append([x, y, a, dx, dy, color, t])


def death_circle(data):
    """ Функция убирает мишень-круг из кортежа, если её время жизни стало нулевым
        (если это время вышло или в мишень попали) """
    if data[6] == 0:
        balls.remove(data)
        new_ball()
        return True
    return False


def death_square(data):
    """ Функция убирает мишень-квадрат из кортежа, если её время жизни стало нулевым
        (если это время вышло или в мишень попали) """
    if data[6] == 0:
        squares.remove(data)
        new_square()
        return True
    return False


def update_circle(data):
    """ Функция обновляет положение мишени-круга: сдвигает или отражает от стены, а также уменьшает её время жизни """
    if (data[0] + data[2] < WIDTH) and (data[0] - data[2] > 0):
        data[0] = data[0] + data[3]
    elif data[0] - data[2] > 0:
        data[3] = -data[3]
        data[0] = data[0] + data[3] - 0.01*data[2]
    else:
        data[3] = -data[3]
        data[0] = data[0] + data[3] + 0.01*data[2]

    if (data[1] + data[2] < HEIGHT) and (data[1] - data[2] > 0):
        data[1] = data[1] + data[4]
    elif data[1] - data[2] > 0:
        data[4] = -data[4]
        data[1] = data[1] + data[4] - 0.01*data[2]
    else:
        data[4] = -data[4]
        data[1] = data[1] + data[4] + 0.01 * data[2]

    data[6] -= 1
    return data


def update_square(data):
    """ Функция обновляет положение мишени-квадрата: сдвигает или отражает от стены,
    а также уменьшает её время жизни """
    if (data[0] + data[2] < WIDTH) and (data[0] > 0):
        data[0] = data[0] + data[3]
    elif data[0] > 0:
        data[3] = -data[3]
        data[0] = data[0] + data[3]
    else:
        data[3] = -data[3]
        data[0] = data[0] + data[3]

    if (data[1] + data[2] < HEIGHT) and (data[1] > 0):
        data[1] = data[1] + data[4]
    elif data[1] > 0:
        data[4] = -data[4]
        data[1] = data[1] + data[4]
    else:
        data[4] = -data[4]
        data[1] = data[1] + data[4]

    data[6] -= 1
    return data


def draw_circle(data):
    """ Функция отрисовывает мишень-круг """
    circle(screen, data[5], (data[0], data[1]), data[2])


def draw_square(data):
    """ Функция отрисовывает мишень-квадрат """
    polygon(screen, data[5], [(data[0], data[1]), (data[0], data[1] + data[2]),
                              (data[0] + data[2], data[1] + data[2]), (data[0] + data[2], data[1])])


# шрифты для текста на экране: отображение очков и запрос имени игрока
score_font = pygame.font.Font(None, 40)
username_font = pygame.font.Font(None, 70)

# добавляем на экран круги и квадраты
for k in range (0, 10, 1):
    new_ball()


for k in range (0, 3, 1):
    new_square()
# выводим на экран просьбу ввести имя игрока
enter_username_text = username_font.render("Введите имя игрока ", True, (255, 255, 0))
screen.blit(enter_username_text, (350, 400))
pygame.display.update()
clock = pygame.time.Clock()
finished = False
# записывам имя игрока в переменную
username = input()

pygame.display.update()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            for i in balls:
                if (pygame.mouse.get_pos()[0] - i[0])**2 + (pygame.mouse.get_pos()[1] - i[1])**2 <= i[2]**2:
                    i[6] = 0
                    if (i[2] >= 80) or (abs(i[3]) < 3):
                        POINTS += 1
                    elif (i[2] >= 40) or (abs(i[3]) < 7):
                        POINTS += 2
                    else:
                        POINTS += 3
            for k in squares:
                if ((pygame.mouse.get_pos()[0] - k[0])**2 + (pygame.mouse.get_pos()[1] - k[1])**2) <= 2*k[2]**2:
                    k[6] = 0
                    POINTS += 5
    for i in range(len(balls)):
        if not death_circle(balls[i]):
            balls[i] = update_circle(balls[i])
            draw_circle(balls[i])
    for i in range(len(squares)):
        if not death_square(squares[i]):
            squares[i] = update_square(squares[i])
            draw_square(squares[i])

    score_text = score_font.render('SCORE: ' + str(POINTS), True, (255, 255, 255))
    screen.blit(score_text, (50, 50))
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
# запишем результат игрока в файл
with open ('C:/Users/Дмитрий/infa_2021_annenkov/rating.txt','a') as inf:
    inf.write(str(username)+' '+str(POINTS)+'\n')

# отсортируем результаты игроков в файле
with open ('C:/Users/Дмитрий/infa_2021_annenkov/rating.txt','r') as inf:
    for line_row in inf:
        if len(line_row) == 0:
            continue
        line = line_row.strip().split()
        dict_rating.update({line[0]: line[1]})
        dict_rating.items()
        sorted_tuple = sorted(dict_rating.items(), key = lambda x: x[1])
        dict_rating = dict(sorted_tuple)
        print(dict_rating)
# выведем отсортированный словарь с результатами игроков
with open ('C:/Users/Дмитрий/infa_2021_annenkov/rating.txt','w') as inf:
        inf.writelines([key+' '+dict_rating[key]+'\n' for key in dict_rating.keys()])
