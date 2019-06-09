from tkinter import *
from Piece import Piece
import numpy as np
import math
from AI import *
import Board
from threading import Timer


class Game(Canvas):

    def __init__(self, size):
        self.size = size  # make board page size * size
        self.rows = 8
        self.cols = 8
        self.master = Tk()
        self.master.minsize(size + 100, size + 100)  # set size of board background
        self.master.title("Checkers :)")
        self.selectedPiece = None  # this is the man that the Player clicked on
        self.pieces = np.empty((8, 8), dtype=Piece)  # the 2d array of pieces
        self.board = np.empty((8, 8), dtype=np.object)  # the 2d array for tiles to save id and coordinate
        self.isAI = False  # this flag is true if AIs turn and otherwise is false
        self.possible_moves = []  # possible moves for selected piece
        self.AINumber = 12
        self.playerNumber = 12
        self.validPieces = []  # the men that can move
        self.moveWithoutHit = 0
        self.numToTie = 100  # if the game gos on for numToTie move without hit , it becomes tie

    def run(self):
        Canvas.__init__(self, self.master, bg='black', height=self.size, width=self.size)
        self.single_player_button = Button(self.master, text="Single player", command=self.make_single_player_game)
        self.multiplayer_button = Button(self.master, text="Multiplayer", command=self.make_multiplayer_game)
        self.single_player_button.pack()
        self.multiplayer_button.pack()
        self.master.mainloop()

    def make_single_player_game(self):
        self.is_single_player = True
        self.makeGame()

    def make_multiplayer_game(self):
        self.is_single_player = False
        self.makeGame()

    def makeGame(self):
        self.single_player_button.pack_forget()
        self.multiplayer_button.pack_forget()
        # you can cancel the double jump by uncommenting following lines
        # self.cancel = Button(self.master, text="Cancel", command=self.cancelMove)
        # self.cancel.pack()
        self.pack()
        self.makeBoard()
        self.putPiece()
        self.checkWins()

    def cancelMove(self):  # cancel double jump :)
        if self.selectedPiece is None:
            return
        if self.selectedPiece.canMoveAgain:
            self.selectedPiece.canMoveAgain = False
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = False
            self.selectedPiece = None
            self.isAI = not self.isAI
            self.resetHighlighted()
            self.checkWins()
            return

    def changeColor(self, color):
        if color == "white":
            return "blue"
        return "white"

    def makeBoard(self):  # make tiles and  you can change color and changeColor function for different color tiles
        size = self.size / 8
        color = "blue"
        for i in range(self.rows):
            color = self.changeColor(color)
            for j in range(self.cols):
                id = self.create_rectangle(j * size + .75, i * size + .75, j * size + size - .75, i * size + size - .75,
                                           fill=color)  # .75 is border
                self.board[i][j] = [id, i, j]
                color = self.changeColor(color)

    def putPiece(self):  # put the Men in their place
        size = self.size / 8  # size of piece
        put = True
        for i in range(3):  # this for make AI's Men
            put = not put
            for j in range(self.cols):
                if put:
                    id = self.create_oval(j * size + 4, i * size + 4, j * size + size - 4, i * size + size - 4,
                                          fill="black")  # 4 is border
                    if not self.is_single_player:
                        self.tag_bind(id, "<ButtonPress-1>", self.onClick)  # on click handler
                    self.pieces[i][j] = Piece(i, j, True, id)
                put = not put
        put = False
        for i in range(7, 4, -1):  # this for make Player's men
            put = not put
            for j in range(self.cols):
                if put:
                    id = self.create_oval(j * size + 4, i * size + 4, j * size + size - 4, i * size + size - 4,
                                          fill="red")
                    self.tag_bind(id, "<ButtonPress-1>", self.onClick)  # on click handler
                    self.pieces[i][j] = Piece(i, j, False, id)

                put = not put

    def onClick(self, event):  # set selected Man and call function to highlight possible move

        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        id = self.find_closest(x, y)[0]
        if id not in [arr[0] for arr in self.validPieces]:
            return
        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is None:
                    continue
                if self.pieces[i][j].id == id:
                    self.selectedPiece = self.pieces[i][j]
        if self.selectedPiece.isAI == self.isAI and not self.selectedPiece.canMoveAgain:
            self.resetHighlighted()
            if not self.canHit:
                self.showNormalMove(True, self.selectedPiece)
            self.showHitMove(True, self.selectedPiece)

    def resetHighlighted(self):  # unhighlight possible moves
        for id in self.possible_moves:
            self.itemconfig(id, outline="black", width=0, activewidth=0)
            self.tag_unbind(id, "<ButtonPress-1>")
        self.possible_moves.clear()

    def putIfPossible(self, neighbour):  # put a tile if its valid move for normal move
        if neighbour is not None:
            i = neighbour[0]
            j = neighbour[1]
            if self.pieces[i][j] is None:
                self.possible_moves.append(self.board[i][j][0])

    def move_ai(self, id):  # this function move AI's Man with id
        rowMove = -1
        colMove = -1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0] == id:
                    rowMove = self.board[i][j][1]
                    colMove = self.board[i][j][2]
                    break
        flag = False
        if math.fabs(self.selectedPiece.row - rowMove) > 1:
            if self.selectedPiece.isAI:
                self.playerNumber = self.playerNumber - 1
            else:
                self.AINumber = self.AINumber - 1
            flag = True
            self.delete(self.pieces[int((rowMove + self.selectedPiece.row) / 2)][
                            int((colMove + self.selectedPiece.col) / 2)].id)
            self.pieces[int((rowMove + self.selectedPiece.row) / 2)][int((colMove + self.selectedPiece.col) / 2)] = None
            self.moveWithoutHit = 0

        self.pieces[rowMove][colMove] = self.pieces[self.selectedPiece.row][self.selectedPiece.col]
        self.pieces[self.selectedPiece.row][self.selectedPiece.col] = None
        self.selectedPiece.moveTo(rowMove, colMove)
        self.pieces[self.selectedPiece.row][self.selectedPiece.col].moveTo(rowMove, colMove)
        size = self.size / 8
        self.coords(self.selectedPiece.id, colMove * size + 4, rowMove * size + 4, colMove * size + size - 4,
                    rowMove * size + size - 4)
        if self.selectedPiece.isKing:
            if self.selectedPiece.isAI:
                self.itemconfig(self.selectedPiece.id, outline="gold", width=4, activewidth=6)
            else:
                self.itemconfig(self.selectedPiece.id, outline="gold", width=4, activewidth=6)
        self.possible_moves.clear()
        if flag:
            self.showHitMove(False, self.selectedPiece)
        if len(self.possible_moves) == 0:
            self.selectedPiece.canMoveAgain = False
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = False
            self.isAI = not self.isAI
            t1 = Timer(0, self.checkWins)
            t1.start()
            # self.checkWins()
        else:
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = True
            self.selectedPiece.canMoveAgain = True
            self.move_ai(self.possible_moves[0])

    def onClickMove(self, event):  # on clicked this function move Player's Man with id
        self.moveWithoutHit = self.moveWithoutHit + 1
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        id = self.find_closest(x, y)[0]
        self.resetHighlighted()
        rowMove = -1
        colMove = -1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0] == id:
                    rowMove = self.board[i][j][1]
                    colMove = self.board[i][j][2]
                    break
        flag = False
        if math.fabs(self.selectedPiece.row - rowMove) > 1:
            if self.selectedPiece.isAI:
                self.playerNumber = self.playerNumber - 1
            else:
                self.AINumber = self.AINumber - 1
            flag = True
            self.delete(self.pieces[int((rowMove + self.selectedPiece.row) / 2)][
                            int((colMove + self.selectedPiece.col) / 2)].id)
            self.pieces[int((rowMove + self.selectedPiece.row) / 2)][int((colMove + self.selectedPiece.col) / 2)] = None
            self.moveWithoutHit = 0

        self.pieces[rowMove][colMove] = self.pieces[self.selectedPiece.row][self.selectedPiece.col]
        self.pieces[self.selectedPiece.row][self.selectedPiece.col] = None
        self.selectedPiece.moveTo(rowMove, colMove)
        self.pieces[self.selectedPiece.row][self.selectedPiece.col].moveTo(rowMove, colMove)
        size = self.size / 8
        self.coords(self.selectedPiece.id, colMove * size + 4, rowMove * size + 4, colMove * size + size - 4,
                    rowMove * size + size - 4)
        if self.selectedPiece.isKing:
            if self.selectedPiece.isAI:
                self.itemconfig(self.selectedPiece.id, outline="gold", width=4, activewidth=6)
            else:
                self.itemconfig(self.selectedPiece.id, outline="gold", width=4, activewidth=6)
        if flag:
            self.resetHighlighted()
            self.showHitMove(True, self.selectedPiece)
        if len(self.possible_moves) == 0:
            self.selectedPiece.canMoveAgain = False
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = False
            self.isAI = not self.isAI
            t1 = Timer(0.01, self.checkWins)
            t1.start()
            # self.checkWins()
        else:
            self.resetHighlightedPieces()
            self.validPieces.append([self.selectedPiece.id, self.selectedPiece.row, self.selectedPiece.col])
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = True
            self.selectedPiece.canMoveAgain = True

    def highlighted(self):  # highlight possible move
        for id in self.possible_moves:
            self.itemconfig(id, outline="yellow", width=4, activewidth=6)
            self.tag_bind(id, "<ButtonPress-1>", self.onClickMove)

    def showNormalMove(self, show, selectedPiece):  # fill possible_moves with normal move
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
        if show:
            self.highlighted()

    def putIfPossible1(self, neighbour, isAI, dir):
        # put a tile if its valid move for normal move and dir is direct of that this man wanna move
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

    def showHitMove(self, show, selectedPiece):  # fill possible_moves with moves that you can hit a opponent's Man
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
        if show:
            self.highlighted()

    def resetHighlightedPieces(self):  # unhighlight last valid pieces
        for arr in self.validPieces:
            if arr[0] == self.selectedPiece.id:
                if self.selectedPiece.isKing:
                    self.itemconfig(arr[0], outline="gold", width=4, activewidth=0)
                else:
                    self.itemconfig(arr[0], outline="black", width=0, activewidth=0)
            else:
                if self.pieces[arr[1]][arr[2]].isKing:
                    self.itemconfig(arr[0], outline="gold", width=4, activewidth=0)
                else:
                    self.itemconfig(arr[0], outline="black", width=0, activewidth=0)
        self.validPieces.clear()

    def checkWins(self):  # this function check the Game state and set valid_pieces array

        text = 'no wins'
        if self.moveWithoutHit >= self.numToTie:
            text = 'Tie :|'
        if self.AINumber <= 0:
            text = 'Player Wins :)'
        elif self.playerNumber <= 0:
            text = 'AI Wins :('
        if text == 'no wins':
            self.resetHighlightedPieces()
            self.selectedPiece = None
            self.canHit = False
            canNormal = False
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                        self.showHitMove(False, self.pieces[i][j])
                        if len(self.possible_moves) != 0:
                            self.validPieces.append([self.pieces[i][j].id, i, j])
                            self.canHit = True
                            self.possible_moves.clear()

            if self.canHit:
                if self.isAI and self.is_single_player:
                    # add AI
                    new_board = Board.Board(self.board, self.pieces, self.rows, self.cols, self.isAI, self.playerNumber,
                                            self.AINumber, self.numToTie, self.moveWithoutHit)
                    piece, move = AI_move(new_board)
                    self.selectedPiece = self.pieces[piece[1]][piece[2]]
                    self.move_ai(move)
                else:
                    self.highlighteValidPieces()
                return
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                        self.showNormalMove(False, self.pieces[i][j])
                        if len(self.possible_moves) != 0:
                            self.validPieces.append([self.pieces[i][j].id, i, j])
                            canNormal = True
                            self.possible_moves.clear()
            if canNormal:
                if self.isAI and self.is_single_player:
                    # add AI
                    new_board = Board.Board(self.board, self.pieces, self.rows, self.cols, self.isAI, self.playerNumber,
                                            self.AINumber, self.numToTie, self.moveWithoutHit)
                    piece, move = AI_move(new_board)
                    self.selectedPiece = self.pieces[piece[1]][piece[2]]
                    self.move_ai(move)
                else:
                    self.highlighteValidPieces()
                return
            if self.isAI:
                text = 'Player Wins'
            else:
                text = 'AI Wins'
        self.finishGame(text)

    def finishGame(self, text):  # make end game page
        self.delete(ALL)
        self.label = Label(self.master,
                           compound=CENTER,
                           text=text,
                           fg="white",
                           bg="black", font="Helvetica 25 bold italic")
        self.label.place(x=410, y=390, anchor="center")
        self.again = Button(self.master, text="Restart", command=self.restart)
        self.again.place(x=410, y=450, anchor="center")
        self.pack_forget()
        # self.cancel.pack_forget()

    def restart(self):  # restart the game
        self.destroy()
        self.master.destroy()
        self.__init__(720)
        self.run()

    def highlighteValidPieces(self):  # highlight the Men which can move
        for arr in self.validPieces:
            if not self.pieces[arr[1]][arr[2]].isKing:
                self.itemconfig(arr[0], outline="white", width=4, activewidth=6)
            else:
                self.itemconfig(arr[0], outline="yellow", width=4, activewidth=6)


if __name__ == '__main__':
    b = Game(720)
    b.run()
