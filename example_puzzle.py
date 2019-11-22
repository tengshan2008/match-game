from puzzle import MatchGame
from pprint import pprint

def show_image(puzzle):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.matshow(np.array(puzzle))

    plt.show()

mg = MatchGame(9, 9, 6)
show_image(mg.puzzle)

x = input()
y = input()
arrow = input()
mg.move(int(x), int(y), arrow)

for puzzle, matched in zip(mg.puzzle_history[1:], mg.matched_history):
    pprint(matched)
    for x, y in matched:
        puzzle[x][y] = 8
    show_image(puzzle)

show_image(mg.puzzle)
