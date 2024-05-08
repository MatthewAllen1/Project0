
import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception('Invalid action')
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i].count(board[i][0]) == 3 and board[i][0] is not None:
            return board[i][0]
        if all(board[j][i] == board[0][i] for j in range(3)) and board[0][i] is not None:
            return board[0][i]
    # Check diagonals
    if all(board[i][i] == board[0][0] for i in range(3)) and board[0][0] is not None:
        return board[0][0]
    if all(board[i][2-i] == board[0][2] for i in range(3)) and board[0][2] is not None:
        return board[0][2]
    return None

def terminal(board):
    if winner(board) is not None or not any(EMPTY in row for row in board):
        return True
    return False

def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    if player(board) == X:
        value = -math.inf
        best_move = None
        for action in actions(board):
            move_val = min_value(result(board, action))
            if move_val > value:
                value = move_val
                best_move = action
        return best_move
    else:
        value = math.inf
        best_move = None
        for action in actions(board):
            move_val = max_value(result(board, action))
            if move_val < value:
                value = move_val
                best_move = action
        return best_move

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
