from copy import deepcopy

MAX_DEPTH = 5


class Node:  # node of tree
    def __init__(self, value, piece, move, depth, board):
        self.board = board
        self.value = value
        self.piece = piece
        self.move = move
        self.depth = depth
        self.children = list()

    def add_child(self, child):
        self.children.append(child)


def AI_move(board):  # find best move for piece
    current_depth = 0
    root = Node(float('-inf'), None, None, current_depth, None)
    root = make_tree(board, root)
    value, move, piece = min_max_func(root, float('-inf'), float('inf'))
    for n in root.children:
        if n.value == value:
            move = n.move
            piece = n.piece
    return piece, move


def make_tree(board, root):  # from this state make all states of the board
    if board.check_win():
        root.value = h(root.board)
        return root
    if root.depth == MAX_DEPTH:
        root.value = h(root.board)
        return root
    valid_pieces = board.valid_pieces()
    for p in valid_pieces:
        valid_moves = board.valid_moves(p)
        for m in valid_moves:
            new_board = deepcopy(board)
            new_board.move(p, m)
            current_depth = root.depth + 1
            if current_depth == MAX_DEPTH:
                new_node = Node(h(board), p, m, current_depth, board)

            else:
                if root.value == float('inf'):  # make maximum
                    new_node = Node(float('-inf'), p, m, current_depth, board)
                else:  # make minimum
                    new_node = Node(float('inf'), p, m, current_depth, board)
            root.add_child(new_node)
            make_tree(new_board, new_node)
    return root


def cover_another_piece(piece, board):
    northwest = piece.getNorthwest()
    northeast = piece.getNortheast()
    southwest = piece.getSouthwest()
    southeast = piece.getSoutheast()
    if piece.isKing:
        if northeast is not None and board.pieces[northeast[0]][northeast[1]] is not None and \
                board.pieces[northeast[0]][northeast[1]].isAI == piece.isAI:
            if southwest is not None and board.pieces[southwest[0]][southwest[1]] is not None and \
                    board.pieces[southwest[0]][southwest[1]].isAI != piece.isAI:
                return True
        if southwest is not None and board.pieces[southwest[0]][southwest[1]] is not None and \
                board.pieces[southwest[0]][southwest[1]].isAI == piece.isAI:
            if northeast is not None and board.pieces[northeast[0]][northeast[1]] is not None and \
                    board.pieces[northeast[0]][northeast[1]].isAI != piece.isAI:
                return True
        if southeast is not None and board.pieces[southeast[0]][southeast[1]] is not None and \
                board.pieces[southeast[0]][southeast[1]].isAI == piece.isAI:
            if northwest is not None and board.pieces[northwest[0]][northwest[1]] is not None and \
                    board.pieces[northwest[0]][northwest[1]].isAI != piece.isAI:
                return True
        if northwest is not None and board.pieces[northwest[0]][northwest[1]] is not None and \
                board.pieces[northwest[0]][northwest[1]].isAI == piece.isAI:
            if southeast is not None and board.pieces[southeast[0]][southeast[1]] is not None and \
                    board.pieces[southeast[0]][southeast[1]].isAI != piece.isAI:
                return True
    elif piece.isAI:
        if northwest is not None and board.pieces[northwest[0]][northwest[1]] is not None and \
                board.pieces[northwest[0]][northwest[1]].isAI == piece.isAI:
            if southeast is not None and board.pieces[southeast[0]][southeast[1]] is not None and \
                    board.pieces[southeast[0]][southeast[1]].isAI != piece.isAI:
                return True
        if northeast is not None and board.pieces[northeast[0]][northeast[1]] is not None and \
                board.pieces[northeast[0]][northeast[1]].isAI == piece.isAI:
            if southwest is not None and board.pieces[southwest[0]][southwest[1]] is not None and \
                    board.pieces[southwest[0]][southwest[1]].isAI != piece.isAI:
                return True
    else:
        if southwest is not None and board.pieces[southwest[0]][southwest[1]] is not None and \
                board.pieces[southwest[0]][southwest[1]].isAI == piece.isAI:
            if northeast is not None and board.pieces[northeast[0]][northeast[1]] is not None and \
                    board.pieces[northeast[0]][northeast[1]].isAI != piece.isAI:
                return True
        if southeast is not None and board.pieces[southeast[0]][southeast[1]] is not None and \
                board.pieces[southeast[0]][southeast[1]].isAI == piece.isAI:
            if northwest is not None and board.pieces[northwest[0]][northwest[1]] is not None and \
                    board.pieces[northwest[0]][northwest[1]].isAI != piece.isAI:
                return True
    return False


def h(board):
    # return heuristic value this tries to have maximum Pieces and have king and have closing pieces
    score = 0
    if board.check_win():
        if board.isAI:
            return 100000000000000000000
        else:
            return -100000000000000000000
    if board.isAI:
        score += (board.AINumber / board.playerNumber) * 6
    else:
        score += (board.playerNumber / board.AINumber) * 6
    myking = 0.1
    opponentKing = 0.1
    for row in board.pieces:
        for p in row:
            if p is not None:
                if p.isKing:
                    if p.isAI == board.isAI:
                        myking += 1
                    else:
                        opponentKing += 1
    score += (myking / opponentKing) * 2
    for row in board.pieces:
        for p in row:
            if p is not None and p.isAI == board.isAI and cover_another_piece(p, board):
                score += 1

    if board.isAI:
        return score
    return score * -1


def check(p, board):  # utility function for heuristic function
    if p is not None:
        piece = board.pieces[p[0]][p[1]]
        if piece is not None:
            if piece.isAI:
                return 20
            else:
                return 1
        else:
            return 10
    else:
        return 10


def min_max_func(root, alpha, beta):  # set all value from last depth to root
    if root.value != float('-inf') and root.value != float('inf'):
        return root.value, root.move, root.piece
    elif root.value == float('-inf'):  # max node
        for n in root.children:
            temp = min_max_func(n, alpha, beta)
            root.value = max(root.value, temp[0])
            alpha = max(alpha, root.value)
            if beta <= alpha:
                print(alpha, beta)
                break
    else:  # min node
        for n in root.children:
            temp = min_max_func(n, alpha, beta)
            root.value = min(root.value, temp[0])
            beta = min(beta, root.value)
            if beta <= alpha:
                print(alpha, beta)
                break
    return root.value, root.move, root.piece
