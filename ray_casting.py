import math
import pygame


class RayCasting:
    def __init__(self, map_size, block_size, blocks):
        self.block_size = block_size
        self.map_size = map_size
        self.blocks = blocks

    def distance(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5

    def shoot(self, pos, angle):
        k = math.tan(math.radians(angle))
        l = pos[1] - k * pos[0]

        x, y = pos[0] // self.block_size[0], pos[1] // self.block_size[1]
        x, y = int(x), int(y)

        if angle == 0:
            x_res, y_res = 0, pos[1]
            _type = 0
            distance = self.distance(*pos, 0, pos[1])
            for x0 in range(x - 1, -1, -1):
                if self.blocks[y][x0] == 1:
                    x_res, y_res = (x0 + 1) * self.block_size[0], pos[1]
                    _type = 1
                    distance = self.distance(*pos, x_res, y_res)
                    return (x_res, y_res), _type, distance
            return (x_res, y_res), _type, distance

        # elif angle == 90:
        #     x_res, y_res = pos[0], 0
        #     _type = 0
        #     distance = self.distance(*pos, x_res, y_res)
        #     for y0 in range(y - 1, -1, -1):
        #         if self.blocks[y0][x] == 1:
        #             x_res, y_res = pos[0], (y0 + 1) * self.block_size[1]
        #             _type = 1
        #             distance = self.distance(*pos, x_res, y_res)
        #             return (x_res, y_res), _type, distance
        #     return (x_res, y_res), _type, distance

        elif angle == 180:
            x_res, y_res = self.map_size[0], pos[1]
            _type = 0
            distance = self.distance(*pos, x_res, y_res)
            for x0 in range(x + 1, self.map_size[0] // self.block_size[0]):
                if self.blocks[y][x0] == 1:
                    x_res, y_res = x0 * self.block_size[0], pos[1]
                    _type = 1
                    distance = self.distance(*pos, x_res, y_res)
                    return (x_res, y_res), _type, distance
            return (x_res, y_res), _type, distance

        # elif angle == 270:
        #     x_res, y_res = pos[0], self.map_size[1]
        #     _type = 0
        #     distance = self.distance(*pos, x_res, y_res)
        #     for y0 in range(y + 1, self.map_size[1] // self.block_size[1]):
        #         if self.blocks[y0][x] == 1:
        #             x_res, y_res = pos[0], y0 * self.block_size[1]
        #             _type = 1
        #             distance = self.distance(*pos, x_res, y_res)
        #             return (x_res, y_res), _type, distance
        #     return (x_res, y_res), _type, distance

        elif 0 < angle <= 90:
            x_res, y_res = -l / k, 0
            _type = 0
            distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x):
                for y0 in range(y + 1):
                    if self.blocks[y0][x0] == 1:
                        y1 = k * ((x0 + 1) * self.block_size[0]) + l
                        if y0 * self.block_size[1] <= y1 <= (y0 + 1) * self.block_size[1]:
                            if self.distance(*pos, (x0 + 1) * self.block_size[0], y1) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = (x0 + 1) * self.block_size[0], y1
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x + 1):
                for y0 in range(y):
                    if self.blocks[y0][x0] == 1:
                        x1 = ((y0 + 1) * self.block_size[1] - l) / k
                        if x0 * self.block_size[0] <= x1 <= (x0 + 1) * self.block_size[0]:
                            if self.distance(*pos, x1, (y0 + 1) * self.block_size[1]) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = x1, (y0 + 1) * self.block_size[1]
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            return (x_res, y_res), _type, distance

        elif 90 < angle < 180:
            x_res, y_res = -l / k, 0
            _type = 0
            distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x + 1, self.map_size[0] // self.block_size[0]):
                for y0 in range(y + 1):
                    # if x0 < self.map_size[0] // self.block_size[0] and y0 < self.map_size[1] // self.block_size[1]:
                    if self.blocks[y0][x0] == 1:
                        y1 = k * (x0 * self.block_size[0]) + l
                        if y0 * self.block_size[1] <= y1 <= (y0 + 1) * self.block_size[1]:
                            if self.distance(*pos, x0 * self.block_size[0], y1) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = x0 * self.block_size[0], y1
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x, self.map_size[0] // self.block_size[0]):
                for y0 in range(y):
                    if self.blocks[y0][x0] == 1:
                        x1 = ((y0 + 1) * self.block_size[1] - l) / k
                        if x0 * self.block_size[0] <= x1 <= (x0 + 1) * self.block_size[0]:
                            if self.distance(*pos, x1, (y0 + 1) * self.block_size[1]) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = x1, (y0 + 1) * self.block_size[1]
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            return (x_res, y_res), _type, distance

        elif 180 < angle <= 270:
            x_res, y_res = (self.map_size[1] - l) / k, self.map_size[1]
            _type = 0
            distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x + 1, self.map_size[0] // self.block_size[0]):
                for y0 in range(y, self.map_size[1] // self.block_size[1]):
                    if self.blocks[y0][x0] == 1:
                        y1 = k * (x0 * self.block_size[0]) + l
                        if y0 * self.block_size[1] <= y1 <= (y0 + 1) * self.block_size[1]:
                            if self.distance(*pos, x0 * self.block_size[0], y1) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = x0 * self.block_size[0], y1
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x, self.map_size[0] // self.block_size[0]):
                for y0 in range(y + 1, self.map_size[1] // self.block_size[1]):
                    if self.blocks[y0][x0] == 1:
                        x1 = (y0 * self.block_size[1] - l) / k
                        if x0 * self.block_size[0] <= x1 <= (x0 + 1) * self.block_size[0]:
                            if self.distance(*pos, x1, y0 * self.block_size[1]) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = x1, y0 * self.block_size[1]
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            return (x_res, y_res), _type, distance

        elif 270 < angle < 360:
            x_res, y_res = (self.map_size[1] - l) / k, self.map_size[1]
            _type = 0
            distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x):
                for y0 in range(y, self.map_size[1] // self.block_size[1]):
                    if self.blocks[y0][x0] == 1:
                        y1 = k * ((x0 + 1) * self.block_size[0]) + l
                        if y0 * self.block_size[1] <= y1 <= (y0 + 1) * self.block_size[1]:
                            if self.distance(*pos, (x0 + 1) * self.block_size[0], y1) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = (x0 + 1) * self.block_size[0], y1
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            for x0 in range(x + 1):
                for y0 in range(y + 1, self.map_size[1] // self.block_size[1]):
                    if self.blocks[y0][x0] == 1:
                        x1 = (y0 * self.block_size[1] - l) / k
                        if x0 * self.block_size[0] <= x1 <= (x0 + 1) * self.block_size[0]:
                            if self.distance(*pos, x1, y0 * self.block_size[1]) < self.distance(*pos, x_res, y_res):
                                x_res, y_res = x1, y0 * self.block_size[1]
                                _type = 1
                                distance = self.distance(*pos, x_res, y_res)

            return (x_res, y_res), _type, distance
