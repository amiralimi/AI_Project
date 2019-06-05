from Game import *
from copy import deepcopy

MAX_DEPTH = 10


class Node():
    def __init__(self, value, piece, move, depth):
        self.value = value
        self.piece = piece
        self.move = move
        self.depth = depth
        self.children = list()

    def add_child(self, child):
        self.children.append(child)


def AI_move(board):
    current_depth = 0
    root = Node(int('-inf'), None, None, current_depth)
    make_tree(board, root)
    min_max_func(root)
    return root.piece, root.move


def make_tree(board, root):
    if root.board.check_win():
        return
    if root.cuurent_depth == MAX_DEPTH:
        return
    for p in board.valid_pieaces():
        for m in board.valid_moves(p):
            new_board = deepcopy(board)
            new_board.move(p, m)
            current_depth = root.depth + 1
            if current_depth == MAX_DEPTH:
                new_node = Node(h(new_board), p, m, current_depth)
            else:
                if root.value == int('inf'):
                    new_node = Node(int('-inf'), p, m, current_depth)
                else:
                    new_node = Node(int('inf'), p, m, current_depth)
            root.add_child(new_node)
            make_tree(new_board, new_node)


def h(board):
    pass


def min_max_func(root):
    if root.value == int('-inf'):
        for n in root.children:
            min_max_func(n)
            if n.value > root.value:
                root.value = n.value
                root.piece = n.piece
                root.move = n.move
    elif root.value == int('inf'):
        for n in root.children:
            min_max_func(n)
            if n.value < root.value:
                root.value = n.value
                root.piece = n.piece
                root.move = n.move
    else:
        return root.value


game_board = Game(720)
AI_move(game_board)
