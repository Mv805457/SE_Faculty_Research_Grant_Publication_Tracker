"""Evaluate a three-by-three board."""
def check_winner(board):
    lines = list(board) + list(zip(*board))
    lines.extend(([board[i][i] for i in range(3)],
                  [board[i][2 - i] for i in range(3)]))
    return next((a for a, b, c in lines if a is not None and a == b == c), None)


def is_board_full(board):
    return all(cell is not None for row in board for cell in row)
