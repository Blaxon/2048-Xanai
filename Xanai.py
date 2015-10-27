"""
Author Xander Hang

this is 2048 game.

this is the actual ai
"""


class Xanai:
    """
    """
    def __init__(self, matrix, depth):
        self.matrix = matrix
        self.depth = depth
        return

    def find_best_move(self):
        import move_table

        best = 0
        best_move = None
        moves = [move_table.move_up,
                 move_table.move_down,
                 move_table.move_left,
                 move_table.move_right]
        for each_move in moves:
            board = each_move(self.matrix)
            # skip invalid move
            if board == self.matrix:
                continue
            _score = self.depth_score(board, self.depth, 1)
            if _score >= best and board != self.matrix:
                best = _score
                best_move = each_move
        return best_move, best

    def score_board(self):
        import BoardEval as Be
        return Be.score_matrix(self.matrix)

    def depth_score(self, board, depth, player):
        import BoardEval as Be
        if depth == 0:
            return Be.score_matrix(board)
        if player == 1:  # if is computer turn
            _total_score = 0
            zeros = [i for i in range(16) if ((board >> (i*4)) & 0xf) == 0]
            for zero in zeros:
                _board = board | (1 << (zero*4))  # only consider insert 2 first
                _total_score += self.depth_score(_board, depth-1, 0)
            return _total_score/len(zeros)
        else:  # if is player turn
            import move_table
            best = 0
            moves = [move_table.move_up,
                     move_table.move_down,
                     move_table.move_left,
                     move_table.move_right]
            for direction in moves:
                _board = direction(board)
                # skip those invalid move
                if _board == board:
                    continue
                _score = self.depth_score(_board, depth-1, 1)
                if _score > best:
                    best = _score
            return best

    def auto_play(self):
        import game
        self.matrix = game.init_matrix()
        while not game.is_over(self.matrix):
            print('')

            game.print_matrix(self.matrix)
            move, _score = self.find_best_move()
            print("best move:", move, 'with score: ', _score)
            _matrix = move(self.matrix)

            if _matrix == self.matrix:
                print("invalid move, nothing changed.")
            else:
                self.matrix = game.random_insert(_matrix)


# test
if __name__ == '__main__':
    # 1. empty board
    ai = Xanai(0, 2)
    score = ai.find_best_move()
    print(score)

    # 2. general board
    ai = Xanai(8, 2)
    score = ai.find_best_move()
    print(score)

    # 3.use auto play
    ai = Xanai(0, 5)
    ai.auto_play()