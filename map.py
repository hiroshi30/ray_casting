import random


def make_blocks(window_size, block_size):
    blocks = [[0 for j in range(window_size[0] // block_size[0])] for j in range(window_size[1] // block_size[1])]

    for i in range(50):
        x = random.randint(0, window_size[0] // block_size[0] - 1)
        y = random.randint(0, window_size[1] // block_size[1] - 1)
        blocks[y][x] = 1

    index = 2

    for i in range(window_size[0] // block_size[0] - 2 * index):
        blocks[index][index + i] = 1
        blocks[-(index + 1)][index + i] = 1

    for i in range(window_size[1] // block_size[1] - 2 * index):
        blocks[index + i][index] = 1
        blocks[index + i][-(index + 1)] = 1

    return blocks
