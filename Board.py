import math


class Board:
    def __init__(self, board, pieces, rows, cols, isAI, player_number, AI_number, numOfTie, moveWithoutHit):
        self.moveWithoutHit = moveWithoutHit
        self.numOfTie = numOfTie
        self.playerNumber = player_number
        self.AINumber = AI_number
        self.rows = rows
        self.cols = cols
        self.board = board
        self.pieces = pieces
        self.isAI = isAI
        self.possible_moves = []

    def move(self, piece_tupple, move):
        piece = self.pieces[piece_tupple[1]][piece_tupple[2]]
        # print(piece, move)
        rowMove = -1
        colMove = -1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0] == move:
                    rowMove = self.board[i][j][1]
                    colMove = self.board[i][j][2]
                    break
        check_can_move_again = False
        if math.fabs(piece.row - rowMove) > 1:
            if piece.isAI:
                self.playerNumber = self.playerNumber - 1
            else:
                self.AINumber = self.AINumber - 1
            self.pieces[int((rowMove + piece.row) / 2)][int((colMove + piece.col) / 2)] = None
            self.moveWithoutHit = 0
            check_can_move_again = True
        # print(piece)
        last_row = piece.row
        last_col = piece.col
        self.pieces[piece.row][piece.col].moveTo(rowMove, colMove)
        self.pieces[rowMove][colMove] = self.pieces[last_row][last_col]
        self.pieces[last_row][last_col] = None
        print(self)
        self.isAI = not self.isAI
        return check_can_move_again

    def valid_pieces(self):
        validPieces = []
        canHit = False
        self.possible_moves.clear()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                    self.showHitMove(self.pieces[i][j])
                    if len(self.possible_moves) != 0:
                        validPieces.append([self.pieces[i][j].id, i, j])
                        canHit = True
                        self.possible_moves.clear()

        if canHit:
            return validPieces
        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                    self.showNormalMove(self.pieces[i][j])
                    if len(self.possible_moves) != 0:
                        validPieces.append([self.pieces[i][j].id, i, j])
                        self.possible_moves.clear()

        return validPieces

    def valid_moves(self, piece):
        # possible_moves = []
        self.showHitMove(self.pieces[piece[1]][piece[2]])
        if len(self.possible_moves) != 0:
            possible_moves = self.possible_moves.copy()
            self.possible_moves.clear()
            return possible_moves
        self.showNormalMove(self.pieces[piece[1]][piece[2]])
        possible_moves = self.possible_moves.copy()
        self.possible_moves.clear()
        # print(possible_moves)
        return possible_moves

    def showHitMove(self, selectedPiece):
        if selectedPiece.isKing:
            self.putIfPossible1(selectedPiece.getNortheast(), self.isAI, 1)
            self.putIfPossible1(selectedPiece.getNorthwest(), self.isAI, 2)
            self.putIfPossible1(selectedPiece.getSoutheast(), self.isAI, 3)
            self.putIfPossible1(selectedPiece.getSouthwest(), self.isAI, 4)
        elif selectedPiece.isAI:
            self.putIfPossible1(selectedPiece.getSoutheast(), self.isAI, 3)
            self.putIfPossible1(selectedPiece.getSouthwest(), self.isAI, 4)
        else:
            self.putIfPossible1(selectedPiece.getNortheast(), self.isAI, 1)
            self.putIfPossible1(selectedPiece.getNorthwest(), self.isAI, 2)

    def putIfPossible1(self, neighbour, isAI, dir):
        if neighbour is not None:
            i = neighbour[0]
            j = neighbour[1]
            if self.pieces[i][j] is not None and self.pieces[i][j].isAI != isAI:
                if dir == 1:
                    self.putIfPossible(self.pieces[i][j].getNortheast())
                elif dir == 2:
                    self.putIfPossible(self.pieces[i][j].getNorthwest())
                elif dir == 3:
                    self.putIfPossible(self.pieces[i][j].getSoutheast())
                elif dir == 4:
                    self.putIfPossible(self.pieces[i][j].getSouthwest())

    def putIfPossible(self, neighbour):
        if neighbour is not None:
            i = neighbour[0]
            j = neighbour[1]
            if self.pieces[i][j] is None:
                self.possible_moves.append(self.board[i][j][0])

    def showNormalMove(self, selectedPiece):
        if selectedPiece.isKing:
            self.putIfPossible(selectedPiece.getNortheast())
            self.putIfPossible(selectedPiece.getNorthwest())
            self.putIfPossible(selectedPiece.getSoutheast())
            self.putIfPossible(selectedPiece.getSouthwest())
        elif selectedPiece.isAI:
            self.putIfPossible(selectedPiece.getSoutheast())
            self.putIfPossible(selectedPiece.getSouthwest())
        else:
            self.putIfPossible(selectedPiece.getNortheast())
            self.putIfPossible(selectedPiece.getNorthwest())

    def check_win(self):
        if self.moveWithoutHit >= self.numOfTie:
            return True
        if self.AINumber <= 0:
            return True
        elif self.playerNumber <= 0:
            return True

        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                    self.showHitMove(self.pieces[i][j])
                    if len(self.possible_moves) != 0:
                        return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                    self.showNormalMove(self.pieces[i][j])
                    if len(self.possible_moves) != 0:
                        return False
        return True

    def __str__(self):
        str = ""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is None:
                    str = str + "o "
                elif self.pieces[i][j].isAI:
                    str = str + "B "
                else:
                    str = str + "W "
            str = str + "\n"
        return str

    def __repr__(self):
        return self.__str__()
