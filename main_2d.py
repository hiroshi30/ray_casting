import sys
import pygame

pygame.init()

from camera import Camera
from ray_casting import RayCasting
from map import *


window_size = (1500, 750)
block_size = (50, 50)

background_color = (255, 255, 255)
wall_color = (12, 162, 24)
border_color = (100, 100, 100)
color0 = (200, 23, 11)
color1 = (12, 1, 251)

radius = 10
border = 2

window = pygame.display.set_mode(window_size)

blocks = make_blocks(window_size, block_size)

camera = Camera(
    window=window,
    map_size=window_size,
    pos=[window_size[0] // 2, window_size[1] // 2]
)

ray_casting = RayCasting(
    map_size=window_size,
    block_size=block_size,
    blocks=blocks
)

positions = [ray_casting.shoot(camera.pos, camera.angle[0])]

while True:

    window.fill(background_color)

    for y in range(window_size[1] // block_size[1]):
        for x in range(window_size[0] // block_size[0]):
            if blocks[y][x]:
                pygame.draw.rect(window, wall_color, (x * block_size[0], y * block_size[1], block_size[0], block_size[1]))
                pygame.draw.rect(window, border_color, (x * block_size[0], y * block_size[1], block_size[0], block_size[1]), border)

    for y in range(window_size[1] // block_size[1]):
        pygame.draw.aaline(window, border_color, (0, y * block_size[1]), (window_size[0], y * block_size[1]))

    for x in range(window_size[0] // block_size[0]):
        pygame.draw.aaline(window, border_color, (x * block_size[0], 0), (x * block_size[0], window_size[1]))

    pygame.draw.circle(window, color0, camera.pos, radius)

    if camera.do_move_up or camera.do_move_down or camera.do_move_right or camera.do_move_left or camera.do_look_up or camera.do_look_down or camera.do_look_right or camera.do_look_left:
        positions = []
        # for angle in camera.range(45, 15):
        angle = camera.angle[0]
        positions.append(ray_casting.shoot(camera.pos, angle))

    for i in range(len(positions)):
        match positions[i][1]:
            case 0:
                color = color0
            case 1:
                color = color1

        color = list(color)
        k = 150 / max(positions[i][2], 0.01)
        k = max(min(k, 1), 0.25)
        for j in 0, 1, 2:
            color[j] = max(min(color[j] * k, 255), 0)

        pygame.draw.line(window, color, camera.pos, positions[i][0], 3)

    camera.do()
    pygame.display.set_caption(f'angle {camera.angle} pos {camera.pos}')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_w:
                camera.do_move_up = True
            if event.key == pygame.K_a:
                camera.do_move_left = True
            if event.key == pygame.K_s:
                camera.do_move_down = True
            if event.key == pygame.K_d:
                camera.do_move_right = True

            if event.key == pygame.K_UP:
                camera.do_look_up = True
            if event.key == pygame.K_LEFT:
                camera.do_look_left = True
            if event.key == pygame.K_DOWN:
                camera.do_look_down = True
            if event.key == pygame.K_RIGHT:
                camera.do_look_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                camera.do_move_up = False
            if event.key == pygame.K_a:
                camera.do_move_left = False
            if event.key == pygame.K_s:
                camera.do_move_down = False
            if event.key == pygame.K_d:
                camera.do_move_right = False

            if event.key == pygame.K_UP:
                camera.do_look_up = False
            if event.key == pygame.K_LEFT:
                camera.do_look_left = False
            if event.key == pygame.K_DOWN:
                camera.do_look_down = False
            if event.key == pygame.K_RIGHT:
                camera.do_look_right = False

    pygame.display.update()
    pygame.display.flip()
