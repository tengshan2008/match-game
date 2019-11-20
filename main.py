import random
from pprint import pprint

LENGTH = 9
WIDTH = 9
COLOR = 4

def init_puzzle():
    # init empty puzzle (large 1)
    puzzle = [[0 for point_x in range(LENGTH)] for point_y in range(WIDTH)]

    for point_x in range(LENGTH):
        for point_y in range(WIDTH):
            puzzle = fill_block(puzzle, point_x, point_y)
    
    return puzzle
    
def fill_block(puzzle, point_x, point_y):
    # ready fill color: set(0, 1, 2, 3)
    ready_color = set(range(COLOR))
    # same line duplicate color
    if point_x-2 >= 0 and puzzle[point_x-1][point_y] == puzzle[point_x-2][point_y]:
        ready_color.remove(puzzle[point_x-1][point_y])
    # same column duplicate color
    if point_y-2 >= 0 and puzzle[point_x][point_y-1] == puzzle[point_x][point_y-2]:
        if puzzle[point_x][point_y-1] in ready_color:
            ready_color.remove(puzzle[point_x][point_y-1])
    # fill one block
    puzzle[point_x][point_y] = random.choice(list(ready_color))
    return puzzle

def update_puzzle(puzzle, matched):
    for x, y in matched:
        for i in range(x, 0, -1):
            print(i, y, i-1, y)
            puzzle[i][y], puzzle[i-1][y] = puzzle[i-1][y], puzzle[i][y]
        puzzle[0][y] = random.choice(range(COLOR))
    return puzzle

def is_dead(puzzle):
    for point_x in range(LENGTH):
        for point_y in range(WIDTH):
            if point_x-1 >= 0 and puzzle[point_x][point_y] == puzzle[point_x-1][point_y]:
                if block_status_1(puzzle, point_x, point_y):
                    return True
            elif point_y-1 >= 0 and puzzle[point_x][point_y] == puzzle[point_x][point_y-1]:
                if block_status_2(puzzle, point_x, point_y):
                    return True
            elif point_x-2 >= 0 and puzzle[point_x][point_y] == puzzle[point_x-2][point_y]:
                if block_status_3(puzzle, point_x, point_y):
                    return True
            elif point_y-2 >= 0 and puzzle[point_x][point_y] == puzzle[point_x][point_y-2]:
                if block_status_4(puzzle, point_x, point_y):
                    return True
    return False
                

def match_puzzle(puzzle, point_x, point_y, arrow):
    if arrow == 'left':
        x1, y1, x2, y2 = point_x, point_y, point_x, point_y-1
    elif arrow == 'right':
        x1, y1, x2, y2 = point_x, point_y, point_x, point_y+1
    elif arrow == 'up':
        x1, y1, x2, y2 = point_x-1, point_y, point_x, point_y
    elif arrow == 'down':
        x1, y1, x2, y2 = point_x+1, point_y, point_x, point_y
    
    puzzle[x1][y1], puzzle[x2][y2] = puzzle[x2][y2], puzzle[x1][y1]
    matched = match_blocks(puzzle, x1, y1) + match_blocks(puzzle, x2, y2)

    return list(set(matched))

def match_blocks(puzzle, point_x, point_y):
    matched = list()
    for i in range(LENGTH-2):
        if puzzle[point_x][i] - puzzle[point_x][i+1] == puzzle[point_x][i+1] - puzzle[point_x][i+2] == 0:
            matched += [(point_x, i), (point_x, i+1), (point_x, i+2)]
    for i in range(WIDTH-2):
        if puzzle[i+1][point_y] - puzzle[i][point_y] == puzzle[i+2][point_y] - puzzle[i+1][point_y] == 0:
            matched += [(i, point_y), (i+1, point_y), (i+2, point_y)]
    return list(matched)

def show_image(puzzle):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.matshow(np.array(puzzle))

    plt.show()

if __name__ == "__main__":
    puzzle = init_puzzle()

    # show_image(puzzle)
    matched = match_puzzle(puzzle, 3, 6, 'up')
    pprint(matched)


    for x, y in matched:
        puzzle[x][y] = 8
    
    show_image(puzzle)

    update_puzzle(puzzle, matched)

    show_image(puzzle)

