"""
Author Xander Hang

this is 2048 game.

bit manipulation was deployed in matrix storage.
"""


def print_matrix(matrix):
    """
    attention: print from high bit to low bit
    """
    for i in range(15, -1, -1):
        print("%6d" % trans_num((matrix >> i*4) & 0xf), end='')
        if i % 4 == 0:
            print('')


def trans_num(hex_num):
    """
    transfer hex num into real game number
    0->0
    1->2
    2->4
    ...
    """
    if hex_num == 0:
        return 0
    return 2 ** hex_num


def _move_left(matrix):
    ret = 0
    rows = to_rows(matrix)
    for each_row in rows:
        row = [(each_row & 0xf000) >> 12,
               (each_row & 0x0f00) >> 8,
               (each_row & 0x00f0) >> 4,
               (each_row & 0x000f) >> 0]

        i = 0
        while i < 4:
            j = i + 1
            while j < 4 and row[j] == 0:
                j += 1
            if j == 4:
                break

            if row[i] == 0:
                row[i] = row[j]
                row[j] = 0
            elif row[i] == row[j]:
                if row[i] != 15:
                    row[i] += 1
                    row[j] = 0
                i += 1
            else:
                i += 1

        for item in row:
            ret <<= 4
            ret |= item
    return ret


def flop(matrix):
    """
    flop matrix in horizon
    """
    ret = 0
    for row in [(matrix >> 48) & 0xffff, (matrix >> 32) & 0xffff, (matrix >> 16) & 0xffff, (matrix >> 0) & 0xffff]:
        a, b, c, d = row & 0xf, row >> 4 & 0xf, row >> 8 & 0xf, row >> 12 & 0xf
        ret <<= 16
        ret |= (a << 12) | (b << 8) | (c << 4) | d
    return ret


def to_rows(matrix):
    """
    rows = [row1, row2, row3, row4]
    """
    rows = []
    for _ in range(4):
        rows.insert(0, matrix & 0xffff)
        matrix >>= 16
    return rows


def to_cols(matrix):
    matrix = transposition(matrix)
    return to_rows(matrix)


def move_right(matrix):
    """
    input matrix bit, output matrix bit
    """
    return flop(_move_left(flop(matrix)))


def move_left(matrix):
    return _move_left(matrix)


def move_up(matrix):
    return transposition(_move_left(transposition(matrix)))


def move_down(matrix):
    return transposition(move_right(transposition(matrix)))


def transposition(matrix):
    """
    0 1 2 3     0 4 8 c
    4 5 6 7 --> 1 5 9 d
    8 9 a b     2 6 a e
    c d e f     3 7 b f
    """
    a1 = matrix & 0xF0F00F0FF0F00F0F
    a2 = matrix & 0x0000F0F00000F0F0
    a3 = matrix & 0x0F0F00000F0F0000
    a = a1 | (a2 << 12) | (a3 >> 12)
    b1 = a & 0xFF00FF0000FF00FF
    b2 = a & 0x00FF00FF00000000
    b3 = a & 0x00000000FF00FF00
    return b1 | (b2 >> 24) | (b3 << 24)


def random_insert(matrix):
    import random
    zeros = [i for i in range(16) if ((matrix >> (i*4)) & 0xf) == 0]
    zero = random.choice(zeros)
    num = random.random() > 0.9 and 2 or 1
    return matrix | (num << (zero*4))


def init_matrix():
    return random_insert(0)


def is_over(matrix):
    """
    if game is over
    """
    matrix_items = []
    for i in range(16):
        item = (matrix >> i*4) & 0xf
        if item == 0:
            return False
        else:
            matrix_items.insert(0, item)

    for i in [_ for _ in range(12) if _ % 4 != 3]:
        if matrix_items[i] == matrix_items[i+1] or matrix_items[i] == matrix_items[i+4]:
            return False
    else:
        return True


def play():
    matrix = init_matrix()
    while not is_over(matrix):
        print('')
        print_matrix(matrix)

        _input = get_input()
        if _input == 'w':
            _matrix = move_up(matrix)
        elif _input == 's':
            _matrix = move_down(matrix)
        elif _input == 'a':
            _matrix = move_left(matrix)
        elif _input == 'd':
            _matrix = move_right(matrix)
        elif _input != 'q':
            print('You entered a wrong key.')

        if _matrix == matrix:
            print('\ninvalid move, nothing changed.')
        else:
            matrix = random_insert(_matrix)

        if _input == 'q':
            return


def get_input(prompt="Wait input: "):
    import termios, sys
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON          # lflags
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        sys.stderr.write(prompt)
        sys.stderr.flush()
        c = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return c


if __name__ == '__main__':
    play()