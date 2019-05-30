from tkinter import *
from Piece import Piece
from array import *
import numpy as np


class Board(Canvas):

    def __init__(self, size):
        self.size = size
        self.rows = 8
        self.cols = 8
        self.gridBox = Tk()
        self.gridBox.minsize(size + 100, size + 100)
        self.selectedPiece = None
        self.pieces = np.empty((8, 8), dtype=Piece)
        self.board = np.empty((8, 8), dtype=np.object)
        self.isAI = False
        self.possibleMoves = []

    def run(self):
        Canvas.__init__(self, self.gridBox, bg='black', height=self.size, width=self.size)
        cancel = Button(self.gridBox, text="Cancel", command=self.cancelMove)
        cancel.pack()
        self.pack()
        self.makeBoard()
        self.putPiece()
        self.gridBox.mainloop()

    def cancelMove(self):
        if self.selectedPiece is None:
            return
        if self.selectedPiece.canMoveAgain:
            self.isAI = not self.isAI
            self.resetHighlighted()
            return

    def changeColor(self, color):
        if color == "white":
            return "blue"
        return "white"

    def makeBoard(self):
        size = self.size / 8
        color = "white"
        for i in range(self.rows):
            color = self.changeColor(color)
            for j in range(self.cols):
                id = self.create_rectangle(j * size + .75, i * size + .75, j * size + size - .75, i * size + size - .75,
                                           fill=color)
                self.board[i][j] = [id, i, j]
                color = self.changeColor(color)

    def putPiece(self):
        size = self.size / 8
        put = False
        for i in range(3):
            put = not put
            for j in range(self.cols):
                if put:
                    id = self.create_oval(j * size + 4, i * size + 4, j * size + size - 4, i * size + size - 4,
                                          fill="black")
                    self.tag_bind(id, "<ButtonPress-1>", self.onClick)
                    self.pieces[i][j] = Piece(i, j, True, id)
                put = not put
        put = True
        for i in range(7, 4, -1):
            put = not put
            for j in range(self.cols):
                if put:
                    id = self.create_oval(j * size + 4, i * size + 4, j * size + size - 4, i * size + size - 4,
                                          fill="red")
                    self.tag_bind(id, "<ButtonPress-1>", self.onClick)
                    self.pieces[i][j] = Piece(i, j, False, id)

                put = not put

    def onClick(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        id = self.find_closest(x, y)[0]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.pieces[i][j] is None:
                    continue
                if self.pieces[i][j].id == id:
                    self.selectedPiece = self.pieces[i][j]
        if self.selectedPiece.isAI == self.isAI and not self.selectedPiece.canMoveAgain:
            self.resetHighlighted()
            self.showNormalMove()
            self.showHitMove()

    def resetHighlighted(self):
        for id in self.possibleMoves:
            self.itemconfig(id, outline="black")
            self.tag_unbind(id, "<ButtonPress-1>")
        self.possibleMoves.clear()

    def putIfPossible(self, neighbour):
        if neighbour is not None:
            i = neighbour[0]
            j = neighbour[1]
            if self.pieces[i][j] is None:
                self.possibleMoves.append(self.board[i][j][0])
    def onClickedMove(self , event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        id = self.find_closest(x, y)[0]
        self.resetHighlighted()
        #todo inja bayd harkat bdm v agar mitoones badiaro highlight konam v canmoveagain true bshe ntoones avaz she


    def highlighted(self):
        for id in self.possibleMoves:
            self.itemconfig(id, outline="yellow")
            self.tag_bind(id, "<ButtonPress-1>", self.onClickMove)

    def showNormalMove(self):
        if self.selectedPiece.isKing:
            self.putIfPossible(self.selectedPiece.getNortheast())
            self.putIfPossible(self.selectedPiece.getNorthwest())
            self.putIfPossible(self.selectedPiece.getSoutheast())
            self.putIfPossible(self.selectedPiece.getSouthwest())
        elif self.selectedPiece.isAI:
            self.putIfPossible(self.selectedPiece.getSoutheast())
            self.putIfPossible(self.selectedPiece.getSouthwest())
        else:
            self.putIfPossible(self.selectedPiece.getNortheast())
            self.putIfPossible(self.selectedPiece.getNorthwest())
        self.highlighted()

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

    def showHitMove(self):
        if self.selectedPiece.isKing:
            self.putIfPossible1(self.selectedPiece.getNortheast(), self.isAI, 1)
            self.putIfPossible1(self.selectedPiece.getNorthwast(), self.isAI, 2)
            self.putIfPossible1(self.selectedPiece.getSoutheast(), self.isAI, 3)
            self.putIfPossible1(self.selectedPiece.getSouthWest(), self.isAI, 4)
        elif self.selectedPiece.isAI:
            self.putIfPossible1(self.selectedPiece.getSoutheast(), self.isAI, 3)
            self.putIfPossible1(self.selectedPiece.getSouthWest(), self.isAI, 4)
        else:
            self.putIfPossible1(self.selectedPiece.getNortheast(), self.isAI, 1)
            self.putIfPossible1(self.selectedPiece.getNorthwast(), self.isAI, 2)
        self.highlighted()


if __name__ == '__main__':
    b = Board(720)
    b.run()
