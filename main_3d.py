import sys
import pygame

from camera import Camera
from ray_casting import RayCasting
from map import random_map


pygame.init()


window_size = (1500, 750)
map_size = (2000, 2000)
block_size = (50, 50)
angle_range = 110
rays_count = 200
wall_size = (window_size[0] // rays_count, window_size[1])

sky_color = (0, 213, 237)
ground_color = (42, 101, 0)
colors = (
    (200, 23, 11),
    (12, 1, 251)
)

window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Ray casting 2')

blocks = random_map(map_size, block_size)

camera = Camera(
    map_size=map_size,
    pos=[map_size[0] // 2, map_size[1] // 2]
)

ray_casting = RayCasting(
    map_size=map_size,
    block_size=block_size,
    blocks=blocks
)

positions = [ray_casting.shoot(camera.pos, camera.angle)]

while True:
    camera.do()

    positions = []
    for angle in camera.range(angle_range, rays_count):
        positions.append(ray_casting.shoot(camera.pos, angle))

    for i in range(len(positions)):
        color = list(colors[positions[i][1]])
        k = 300 / max(positions[i][2], 0.01)
        k = max(min(k, 1), 0.3)
        for j in 0, 1, 2:
            color[j] = max(min(color[j] * k, 255), 0)

        height = wall_size[1] * 100 / max(positions[i][2], 0.01)

        # Drawing sky
        pygame.draw.rect(window, sky_color, (wall_size[0] * i, 0, wall_size[0], (window_size[1] - height) // 2))
        # Drawing wall
        pygame.draw.rect(window, color, (wall_size[0] * i, (window_size[1] - height) // 2, wall_size[0], height))
        # Drawing ground
        pygame.draw.rect(window, ground_color, (wall_size[0] * i, (window_size[1] - height) // 2 + height, wall_size[0], window_size[1] - ((window_size[1] - height) // 2) + height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        camera.controls(event)

    pygame.display.update()
    pygame.display.flip()
