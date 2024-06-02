import math
import time

import pygame


class Camera:
    def __init__(self, map_size, pos=[0, 0], pos_sensitivity=2.4, angle_sensitivity=1):
        info = pygame.display.Info()
        self.display_half = (info.current_w // 2, info.current_h // 2)

        self.map_size = map_size
        self.pos = pos
        self.angle = 90
        self.recalculate_vects = True
        self.front_vect = [
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ]
        self.right_vect = [
            math.cos(math.radians(90 + self.angle)),
            math.sin(90 + math.radians(self.angle))
        ]

        self.pos_sensitivity = pos_sensitivity
        self.angle_sensitivity = angle_sensitivity

        self.dx = 0
        self.dy = 0
        pygame.mouse.set_visible(0)
        self.time = time.time()

    def move(self):
        if self.dx != 0 or self.dy != 0:
            if self.recalculate_vects:
                self.front_vect = [
                    math.cos(math.radians(self.angle)),
                    math.sin(math.radians(self.angle))
                ]
                self.right_vect = [
                    math.cos(math.radians(90 + self.angle)),
                    math.sin(90 + math.radians(self.angle))
                ]
                self.recalculate_vects = False

            vect = [
                self.dy * self.front_vect[0] + self.dx * self.right_vect[0],
                self.dy * self.front_vect[1] + self.dx * self.right_vect[1],
            ]
            length = (vect[0]**2 + vect[1]**2)**.5
            if length != 0:
                self.pos[0] -= self.pos_sensitivity * vect[0] / length
                self.pos[1] -= self.pos_sensitivity * vect[1] / length

                self.pos[0] = max(min(self.pos[0], self.map_size[0]), 0)
                self.pos[1] = max(min(self.pos[1], self.map_size[1]), 0)

    def look(self):
        mouse_delta = pygame.mouse.get_pos()[0] - self.display_half[0]
        if mouse_delta != 0:
            self.angle += self.angle_sensitivity * mouse_delta

            while self.angle >= 360:
                self.angle -= 360
            while self.angle < 0:
                self.angle += 360

            self.recalculate_vects = True

            pygame.mouse.set_pos(self.display_half)

    def do(self):
        current_time = time.time()
        if current_time - self.time > 0.011:
            self.move()
            self.look()
            self.time = current_time

    def controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.dy += 1
            if event.key == pygame.K_a:
                self.dx -= 1
            if event.key == pygame.K_s:
                self.dy -= 1
            if event.key == pygame.K_d:
                self.dx += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.dy -= 1
            if event.key == pygame.K_a:
                self.dx += 1
            if event.key == pygame.K_s:
                self.dy += 1
            if event.key == pygame.K_d:
                self.dx -= 1

    def range(self, angle_range, rays_count):
        angles = []
        delta_angle = angle_range / (rays_count - 1)
        for i in range(rays_count):
            angles.append(self.angle - angle_range / 2 + i * delta_angle)
            while angles[i] >= 360:
                angles[i] -= 360
            while angles[i] < 0:
                angles[i] += 360

        return angles
