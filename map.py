import random


def random_map(window_size, block_size):
    height = window_size[1] // block_size[1]
    width = window_size[0] // block_size[0]

    blocks = [[0 for x in range(width)] for y in range(height)]

    # Random block filling
    for i in range(50):
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)
        blocks[y][x] = 1

    # Borders
    indent = 2

    for y in range(height - 2 * indent):
        blocks[indent + y][indent] = 1
        blocks[indent + y][-1 - indent] = 1

    for x in range(width - 2 * indent):
        blocks[indent][indent + x] = 1
        blocks[-1 - indent][indent + x] = 1

    return blocks
