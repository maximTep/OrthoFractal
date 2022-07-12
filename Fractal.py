import pygame
import math

pygame.init()
screenWidth = 1280
screenHeight = 1024
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Fractal")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# def line_len(p1: list, p2: list):
#     return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


def line_len(line_: list):
    p1 = line_[0]
    p2 = line_[1]
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


def line_to_fract(p1: list, p2: list):
    length = line_len([p1, p2])
    newLines = []
    vec = [(p2[0]-p1[0])/4, (p2[1]-p1[1])/4]
    orth_vec = [(p2[1]-p1[1])/4, -(p2[0]-p1[0])/4]
    # vecLen = math.sqrt(vec[0]**2 + vec[1]**2)
    # vec = [vec[0]/vecLen, vec[1]/vecLen]

    start = p1
    end = [start[0] + vec[0], start[1] + vec[1]]  # ВПРАВО
    newLines.append([start, end])

    start = end
    end = [start[0] + orth_vec[0], start[1] + orth_vec[1]]  # ВВЕРХ
    newLines.append([start, end])

    start = end
    end = [start[0] + vec[0], start[1] + vec[1]]  # ВПРАВО
    newLines.append([start, end])

    start = end
    end = [start[0] - orth_vec[0], start[1] - orth_vec[1]]  # ВНИЗ
    newLines.append([start, end])

    start = end
    end = [start[0] - orth_vec[0], start[1] - orth_vec[1]]  # ВНИЗ
    newLines.append([start, end])

    start = end
    end = [start[0] + vec[0], start[1] + vec[1]]  # ВПРАВО
    newLines.append([start, end])

    start = end
    end = [start[0] + orth_vec[0], start[1] + orth_vec[1]]  # ВВЕРХ
    newLines.append([start, end])

    start = end
    end = [start[0] + vec[0], start[1] + vec[1]]  # ВПРАВО
    newLines.append([start, end])



    # for line in newLines:
    #     pygame.draw.line(screen, WHITE, line[0], line[1], width=1)

    return newLines


def visible_lines(lines_: list, scale_, scale_shift_W_, scale_shift_H_):
    it = 0
    expander = 0
    LB = -expander
    RB = screenWidth + expander
    UB = -expander
    DB = screenHeight + expander
    while it < len(lines_):
        line_ = [lines_[it][0], lines_[it][1]]
        line_[0] = [line_[0][0] * scale_ - scale_shift_W, line_[0][1] * scale_ - scale_shift_H]
        line_[1] = [line_[1][0] * scale_ - scale_shift_W, line_[1][1] * scale_ - scale_shift_H]
        if line_[0][0] < LB or line_[0][0] > RB or line_[0][1] < UB or line_[0][1] > DB:
            if line_[1][0] < LB or line_[1][0] > RB or line_[1][1] < UB or line_[1][1] > DB:
                lines_.pop(it)
                continue
        it += 1

    return lines_



lines = [[[50, screenHeight/2], [screenWidth-50, screenHeight/2]]]
pygame.draw.aaline(screen, WHITE, lines[0][0], lines[0][1])
pygame.display.update()

clock = pygame.time.Clock()
time = pygame.time.get_ticks()
max_iterations = 6
iterations = 0
scale = 1
scale_speed = 0.02
scale_acceleration = 1

running = True
while running:
    #scale += scale_speed * scale_acceleration
    scale *= scale_speed + 1
    # scale_speed = scale_speed * scale_acceleration
    scale_shift_W = (scale-1)*50 # (scale-1) * screenWidth / 2
    scale_shift_H = (scale-1) * screenHeight / 2
    screen.fill(BLACK)
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if line_len(lines[len(lines)//2]) * scale > 3:          # not Done:
        time = pygame.time.get_ticks()
        iterations += 1

        lines = visible_lines(lines, scale, scale_shift_W, scale_shift_H)
        newLines = []
        for ind, line in enumerate(lines):
            if ind <= len(lines) // 5:         # 3 * len(lines) // 5 >= ind >= 2 * len(lines) // 5:
                for fractLine in line_to_fract(line[0], line[1]):
                    newLines.append(fractLine)
            else:
                newLines.append(line)

        lines = newLines

        for i in lines:
            pygame.draw.aaline(screen,
                               WHITE,
                               [i[0][0] * scale - scale_shift_W, i[0][1] * scale - scale_shift_H],
                               [i[1][0] * scale - scale_shift_W, i[1][1] * scale - scale_shift_H])

    else:
        for i in lines:
            pygame.draw.aaline(screen,
                               WHITE,
                               [i[0][0] * scale - scale_shift_W, i[0][1] * scale - scale_shift_H],
                               [i[1][0] * scale - scale_shift_W, i[1][1] * scale - scale_shift_H])



    pygame.display.update()



