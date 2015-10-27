"""
Author Xander Hang

this only contains the eval of single board;

without contain minimax tree.
"""

import game


BOARD_DEFAULT_SCORE = 1000.0
EMPTY_WEIGHT = 120.0
SCORE_WEIGHT = 20.0
MONOTONICITY_WEIGHT = -5.0
SMOOTHNESS_WEIGHT = 30.0


def score_matrix(matrix):
    empty = count_empty(matrix)
    monoto, smooth = monoto_smooth(matrix)
    return BOARD_DEFAULT_SCORE + \
           empty*EMPTY_WEIGHT + \
           monoto*MONOTONICITY_WEIGHT +\
           smooth*SMOOTHNESS_WEIGHT


def count_empty(matrix):
    count = 0
    for i in range(16):
        if ((matrix >> i*4) & 0xf) == 0:
            count += 1
    return count


def monoto_smooth(matrix):
    """
    calc monotonicity and smoothness of matrix

    return monoto, smooth
    """
    left, right = 0, 0
    _smooth = 0
    for i in [i for i in range(15, -1, -1) if i % 4 != 0]:
        t = ((matrix >> i*4) & 0xf) - ((matrix >> (i-1)*4) & 0xf)
        if t > 0:
            left += 1
        elif t < 0:
            right += 1
        else:
            _smooth += 1
    hor_score = min(left, right)

    _matrix = game.transposition(matrix)
    up, down = 0, 0
    for i in [i for i in range(15, -1, -1) if i % 4 != 0]:
        t = ((_matrix >> i*4) & 0xf) >= ((_matrix >> (i-1)*4) & 0xf)
        if t > 0:
            up += 1
        elif t < 0:
            down += 1
        else:
            _smooth += 1
    return min(up, down) + hor_score, _smooth


def find_best_move(matrix):
    best_move = None
    best_score = -1
    matrixes = [game.move_up(matrix),
                game.move_down(matrix),
                game.move_left(matrix),
                game.move_right(matrix)]
    for i in range(4):
        if matrixes[i] != matrix:
            score = score_matrix(matrixes[i])
            if score >= best_score:
                best_score = score
                best_move = i
    return best_move, best_score


def ai_play():
    step = 0
    matrix = game.init_matrix()
    moves = [game.move_up,
             game.move_down,
             game.move_left,
             game.move_right]
    while not game.is_over(matrix):
        game.print_matrix(matrix)
        best_move, best_score = find_best_move(matrix)
        if best_move == -1:
            print('cannot find best move, quit game.')
            break
        matrix = moves[best_move](matrix)
        print('step %4d the best move is %4s, the score %5d' % \
              (step,
               ['up', 'down', 'left', 'right'][best_move],
               best_score))
        matrix = game.random_insert(matrix)
        step += 1
    return


if __name__ == '__main__':
    ai_play()