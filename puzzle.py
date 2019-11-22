import random
import copy

LENGTH = 9
WIDTH = 9
COLOR = 6

class MatchGame(object):

    def __init__(self, length=LENGTH, width=WIDTH, color=COLOR):
        self.length = length
        self.width = width
        self.color = color
        self.puzzle = self.__random_init()
        self.matched_history = list()
        self.puzzle_history = list()


    def move(self, point_x, point_y, arrow):
        matched = self.__match_puzzle(point_x, point_y, arrow)
        while True:
            self.matched_history.append(matched)
            self.puzzle_history.append(copy.deepcopy(self.puzzle))
            changed = self.__update_puzzle(matched)
            if not self.__is_not_dead(self.puzzle):
                print('dead')
                self.puzzle = self.__random_init()
                break
            matched = list()
            for x, y in changed:
                matched += self.__match_blocks(x, y)
            matched = list(set(matched))
            if len(matched) == 0:
                break
            

    def __random_init(self):
        puzzle = [[0 for point_x in range(self.length)] for point_y in range(self.width)]
        for point_x in range(self.width):
            for point_y in range(self.length):
                puzzle = self.__fill_block(puzzle, point_x, point_y)
        if not self.__is_not_dead(puzzle):
            print('dead')
            puzzle = self.__random_init()
        return puzzle


    def __fill_block(self, puzzle, point_x, point_y):
        ready_color = set(range(self.color))
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


    def __match_puzzle(self, point_x, point_y, arrow):
        if arrow == 'left':
            x1, y1, x2, y2 = point_x, point_y, point_x, point_y-1
        elif arrow == 'right':
            x1, y1, x2, y2 = point_x, point_y, point_x, point_y+1
        elif arrow == 'up':
            x1, y1, x2, y2 = point_x-1, point_y, point_x, point_y
        elif arrow == 'down':
            x1, y1, x2, y2 = point_x+1, point_y, point_x, point_y
        
        self.puzzle[x1][y1], self.puzzle[x2][y2] = self.puzzle[x2][y2], self.puzzle[x1][y1]
        matched = self.__match_blocks(x1, y1) + self.__match_blocks(x2, y2)
        if len(matched) == 0:
            self.puzzle[x1][y1], self.puzzle[x2][y2] = self.puzzle[x2][y2], self.puzzle[x1][y1]
        return list(set(matched))


    def __match_blocks(self, point_x, point_y):
        matched = list()
        for i in range(self.length-2):
            if self.puzzle[point_x][i] - self.puzzle[point_x][i+1] == self.puzzle[point_x][i+1] - self.puzzle[point_x][i+2] == 0:
                matched += [(point_x, i), (point_x, i+1), (point_x, i+2)]
        for i in range(self.width-2):
            if self.puzzle[i+1][point_y] - self.puzzle[i][point_y] == self.puzzle[i+2][point_y] - self.puzzle[i+1][point_y] == 0:
                matched += [(i, point_y), (i+1, point_y), (i+2, point_y)]
        return matched


    # todo: could be better. too many loop
    def __update_puzzle(self, matched):
        changed = list()
        for row in range(self.width):
            for x, y in matched:
                if row == x:
                    for i in range(x, 0, -1):
                        changed += [(i, y), (i-1, y)]
                        self.puzzle[i][y], self.puzzle[i-1][y] = self.puzzle[i-1][y], self.puzzle[i][y]
                    self.puzzle[0][y] = random.choice(range(self.color))
                    changed.append((0, y))
        return list(set(changed))


    def __is_not_dead(self, puzzle):
        puzzle_mirror = [row[::-1] for row in puzzle]
        puzzle_transfor = list(map(list,zip(*puzzle)))

        # status like [口口]
        if self.__block_status_1(puzzle):
            return True
        if self.__block_status_1(puzzle_mirror):
            return True
        if self.__block_status_1(puzzle_transfor):
            return True
        # status like [口X口]
        if self.__block_status_2(puzzle):
            return True
        if self.__block_status_2(puzzle_transfor):
            return True

        return False


    def __block_status_1(self, puzzle):
        for point_x in range(self.width):
            for point_y in range(self.length-1):
                if puzzle[point_x][point_y] == puzzle[point_x][point_y+1]:
                    if point_x >= 1 and point_y >= 1 and puzzle[point_x-1][point_y-1] == puzzle[point_x][point_y]:
                        return True
                    if point_y >= 2 and puzzle[point_x][point_y-2] == puzzle[point_x][point_y]:
                        return True
                    if point_x+1 < self.length and point_y <= 1 and puzzle[point_x+1][point_y-1] == puzzle[point_x][point_y]:
                        return True
        return False


    def __block_status_2(self, puzzle):
        for point_x in range(self.width):
            for point_y in range(1, self.length-1):
                if puzzle[point_x][point_y-1] == puzzle[point_x][point_y+1]:
                    if point_x >= 1 and puzzle[point_x-1][point_y] == puzzle[point_x][point_y-1]:
                        return True
                    if point_x+1 < self.length and puzzle[point_x+1][point_y] == puzzle[point_x][point_y-1]:
                        return True
        return False
