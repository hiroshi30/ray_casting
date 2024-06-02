import sys
import pygame

from camera import Camera
from ray_casting import RayCasting
from map import random_map


pygame.init()


window_size = (1500, 750)
block_size = (50, 50)

background_color = (255, 255, 255)
wall_color = (12, 162, 24)
border_color = (100, 100, 100)
colors = (
    (200, 23, 11),
    (12, 1, 251)
)

radius = 10
border = 2

window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Ray casting 1')

blocks = random_map(window_size, block_size)

camera = Camera(
    map_size=window_size,
    pos=[window_size[0] // 2, window_size[1] // 2]
)

ray_casting = RayCasting(
    map_size=window_size,
    block_size=block_size,
    blocks=blocks
)

positions = [ray_casting.shoot(camera.pos, camera.angle)]

while True:
    window.fill(background_color)

    camera.do()

    for y in range(window_size[1] // block_size[1]):
        for x in range(window_size[0] // block_size[0]):
            if blocks[y][x]:
                pygame.draw.rect(window, wall_color, (x * block_size[0], y * block_size[1], block_size[0], block_size[1]))
                pygame.draw.rect(window, border_color, (x * block_size[0], y * block_size[1], block_size[0], block_size[1]), border)

    for y in range(window_size[1] // block_size[1]):
        pygame.draw.aaline(window, border_color, (0, y * block_size[1]), (window_size[0], y * block_size[1]))

    for x in range(window_size[0] // block_size[0]):
        pygame.draw.aaline(window, border_color, (x * block_size[0], 0), (x * block_size[0], window_size[1]))

    positions = []
    for angle in camera.range(45, 15):
        # angle = camera.angle
        positions.append(ray_casting.shoot(camera.pos, angle))

    for i in range(len(positions)):
        color = list(colors[positions[i][1]])
        k = 150 / max(positions[i][2], 0.01)
        k = max(min(k, 1), 0.25)
        for j in range(3):
            color[j] = max(min(color[j] * k, 255), 0)

        pygame.draw.line(window, color, camera.pos, positions[i][0], 3)

    pygame.draw.circle(window, colors[0], camera.pos, radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        camera.controls(event)

    pygame.display.update()
    pygame.display.flip()
