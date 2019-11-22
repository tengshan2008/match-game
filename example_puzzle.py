from puzzle import MatchGame
from pprint import pprint

def show_image(puzzle):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.matshow(np.array(puzzle))

    plt.show()

def show_detail(puzzle_history, matched_history):
    for puzzle, matched in zip(puzzle_history, matched_history):
        for x, y in matched:
            puzzle[x][y] = 8
        show_image(puzzle)


if __name__ == "__main__":
    mg = MatchGame(9, 9, 6)
    show_image(mg.puzzle)

    mg.move(int(input()), int(input()), input())
    show_detail(mg.puzzle_history, mg.matched_history)
    show_image(mg.puzzle)
