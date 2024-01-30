import sys
import pygame

pygame.init()

from camera import Camera
from ray_casting import RayCasting
from map import *


window_size = (1500, 750)
map_size = (2000, 2000)
block_size = (50, 50)
rays_angle = 90
rays_count = rays_angle * 3
wall_size = (window_size[0] // rays_count, window_size[1])

sky_color = (0, 213, 237)
ground_color = (42, 101, 0)
color0 = (200, 23, 11)
color1 = (12, 1, 251)

window = pygame.display.set_mode(window_size)

blocks = make_blocks(map_size, block_size)

camera = Camera(
    window=window,
    map_size=map_size,
    pos=[window_size[0] // 2, window_size[1] // 2]
)

ray_casting = RayCasting(
    map_size=map_size,
    block_size=block_size,
    blocks=blocks
)

positions = [ray_casting.shoot(camera.pos, camera.angle[0])]

while True:

    window.fill((0, 0, 0))

    if camera.do_move_up or camera.do_move_down or camera.do_move_right or camera.do_move_left or camera.do_look_up or camera.do_look_down or camera.do_look_right or camera.do_look_left:
        positions = []
        for angle in camera.range(rays_angle, rays_count):
            positions.append(ray_casting.shoot(camera.pos, angle))

    for i in range(len(positions)):
        match positions[i][1]:
            case 0:
                color = color0
            case 1:
                color = color1

        color = list(color)
        k = 300 / max(positions[i][2], 0.01)
        k = max(min(k, 1), 0.3)
        for j in 0, 1, 2:
            color[j] = max(min(color[j] * k, 255), 0)

        height = wall_size[1] * 100 / max(positions[i][2], 0.01)

        pygame.draw.rect(window, sky_color, (wall_size[0] * i, 0, wall_size[0], (window_size[1] - height) // 2))
        pygame.draw.rect(window, color, (wall_size[0] * i, (window_size[1] - height) // 2, wall_size[0], height))
        pygame.draw.rect(window, ground_color, (wall_size[0] * i, height + (window_size[1] - height) // 2, wall_size[0], (window_size[1] - height) // 2))

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
