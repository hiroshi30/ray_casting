import math
import time


class Camera:
    def __init__(self, window, map_size, pos):
        self.window = window
        self.map_size = map_size
        self.pos = pos
        # self.pos[0] = 100
        self.angle = [90, 0]

        self.pos_speed = (3, 3)
        self.angle_speed = (2, 3)

        self.start_time = 0
        self.delta_time = 0.007

        self.do_look_up = False
        self.do_look_down = False
        self.do_look_right = False
        self.do_look_left = False

        self.do_move_up = False
        self.do_move_down = False
        self.do_move_right = False
        self.do_move_left = False

    def look_up(self):
        self.angle[1] += self.angle_speed[1]
        self.angle[1] %= 360

    def look_down(self):
        self.angle[1] -= self.angle_speed[1]
        while self.angle[1] < 0:
            self.angle[1] += 360

    def look_right(self):
        self.angle[0] += self.angle_speed[0]
        self.angle[0] %= 360

    def look_left(self):
        self.angle[0] -= self.angle_speed[0]
        while self.angle[0] < 0:
            self.angle[0] += 360

    def move_up(self):
        self.pos[0] -= self.pos_speed[0] * math.cos(math.radians(self.angle[0]))
        self.pos[1] -= self.pos_speed[1] * math.sin(math.radians(self.angle[0]))
        self.pos[0] = max(min(self.pos[0], self.map_size[0]), 0)
        self.pos[1] = max(min(self.pos[1], self.map_size[1]), 0)

    def move_down(self):
        self.pos[0] += self.pos_speed[0] * math.cos(math.radians(self.angle[0]))
        self.pos[1] += self.pos_speed[1] * math.sin(math.radians(self.angle[0]))
        self.pos[0] = max(min(self.pos[0], self.map_size[0]), 0)
        self.pos[1] = max(min(self.pos[1], self.map_size[1]), 0)

    def move_right(self):
        self.pos[0] -= self.pos_speed[0] * math.cos(math.radians(90 + self.angle[0]))
        self.pos[1] -= self.pos_speed[1] * math.sin(math.radians(90 + self.angle[0]))
        self.pos[0] = max(min(self.pos[0], self.map_size[0]), 0)
        self.pos[1] = max(min(self.pos[1], self.map_size[1]), 0)

    def move_left(self):
        self.pos[0] += self.pos_speed[0] * math.cos(math.radians(90 + self.angle[0]))
        self.pos[1] += self.pos_speed[1] * math.sin(math.radians(90 + self.angle[0]))
        self.pos[0] = max(min(self.pos[0], self.map_size[0]), 0)
        self.pos[1] = max(min(self.pos[1], self.map_size[1]), 0)

    def do(self):
        if time.time() - self.start_time > self.delta_time:
            if self.do_look_up:
                self.look_up()

            if self.do_look_down:
                self.look_down()

            if self.do_look_right:
                self.look_right()

            if self.do_look_left:
                self.look_left()

            if self.do_move_up:
                self.move_up()

            if self.do_move_down:
                self.move_down()

            if self.do_move_right:
                self.move_right()

            if self.do_move_left:
                self.move_left()

            self.start_time = time.time()

    def range(self, angle, counts):
        angles = []
        delta_angle = angle / (counts - 1)
        for i in range(counts):
            angles.append(self.angle[0] - angle / 2 + i * delta_angle)
            while angles[i] < 0:
                angles[i] += 360
            angles[i] %= 360

        return angles
