"""
Author Xander Hang

this is 2048 game.

a table storage move
"""

import game


UP_TABLE = {}
DOWN_TABLE = {}
LEFT_TABLE = {}
RIGHT_TABLE = {}
HITS = 0


def move_up(matrix):
    if matrix in UP_TABLE:
        global HITS
        HITS += 1
        return UP_TABLE[matrix]
    else:
        UP_TABLE[matrix] = game.move_up(matrix)
        return UP_TABLE[matrix]


def move_down(matrix):
    if matrix in DOWN_TABLE:
        global HITS
        HITS += 1
        return DOWN_TABLE[matrix]
    else:
        DOWN_TABLE[matrix] = game.move_down(matrix)
        return DOWN_TABLE[matrix]


def move_left(matrix):
    if matrix in LEFT_TABLE:
        global HITS
        HITS += 1
        return LEFT_TABLE[matrix]
    else:
        LEFT_TABLE[matrix] = game.move_left(matrix)
        return LEFT_TABLE[matrix]


def move_right(matrix):
    if matrix in RIGHT_TABLE:
        global HITS
        HITS += 1
        return RIGHT_TABLE[matrix]
    else:
        RIGHT_TABLE[matrix] = game.move_right(matrix)
        return RIGHT_TABLE[matrix]


class MoveTable:
    """
    """

    def __init__(self):
        self.up_table = {}
        self.down_table = {}
        self.left_table = {}
        self.right_table = {}
        self.hits = 0

    def move_up(self, matrix):
        if matrix in self.up_table:
            self.hits += 1
            return self.up_table[matrix]
        else:
            self.up_table[matrix] = game.move_up(matrix)
            return self.up_table[matrix]

    def move_down(self, matrix):
        if matrix in self.down_table:
            self.hits += 1
            return self.down_table[matrix]
        else:
            self.down_table[matrix] = game.move_down(matrix)
            return self.down_table[matrix]

    def move_left(self, matrix):
        if matrix in self.left_table:
            self.hits += 1
            return self.left_table[matrix]
        else:
            self.left_table[matrix] = game.move_left(matrix)
            return self.left_table[matrix]

    def move_right(self, matrix):
        if matrix in self. right_table:
            self.hits += 1
            return self.right_table[matrix]
        else:
            self.right_table[matrix] = game.move_right(matrix)
            return self.right_table[matrix]

    def print_hits(self):
        print("the total hits : %d" % self.hits)
