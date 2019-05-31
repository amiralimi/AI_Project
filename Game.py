from tkinter import *
from Piece import Piece
import numpy as np
import math


class Game(Canvas):

    def __init__(self, size):
        self.size = size
        self.rows = 8
        self.cols = 8
        self.master = Tk()
        self.master.minsize(size + 100, size + 100)
        self.master.title("Checkers :)")
        self.selectedPiece = None
        self.pieces = np.empty((8, 8), dtype=Piece)
        self.board = np.empty((8, 8), dtype=np.object)
        self.isAI = False
        self.possibleMoves = []
        self.AINumber = 12
        self.playerNumber = 12

    def run(self):
        Canvas.__init__(self, self.master, bg='black', height=self.size, width=self.size)
        self.cancel = Button(self.master, text="Cancel", command=self.cancelMove)
        self.cancel.pack()
        self.pack()
        self.makeBoard()
        self.putPiece()
        self.master.mainloop()

    def cancelMove(self):
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
            self.showNormalMove(True, self.selectedPiece)
            self.showHitMove(True, self.selectedPiece)

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

    def onClickMove(self, event):
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

        self.pieces[rowMove][colMove] = self.pieces[self.selectedPiece.row][self.selectedPiece.col]
        self.pieces[self.selectedPiece.row][self.selectedPiece.col] = None
        self.selectedPiece.moveTo(rowMove, colMove)
        self.pieces[self.selectedPiece.row][self.selectedPiece.col].moveTo(rowMove, colMove)
        size = self.size / 8
        self.coords(self.selectedPiece.id, colMove * size + 4, rowMove * size + 4, colMove * size + size - 4,
                    rowMove * size + size - 4)
        if self.selectedPiece.isKing:
            if self.selectedPiece.isAI:
                self.itemconfig(self.selectedPiece.id, outline="gold")
            else:
                self.itemconfig(self.selectedPiece.id, outline="gold")
        if flag:
            self.showHitMove(True, self.selectedPiece)
        if len(self.possibleMoves) == 0:
            self.selectedPiece.canMoveAgain = False
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = False
            self.selectedPiece = None
            self.isAI = not self.isAI
            self.checkWins()
        else:
            self.pieces[self.selectedPiece.row][self.selectedPiece.col].canMoveAgain = True
            self.selectedPiece.canMoveAgain = True

    def highlighted(self):
        for id in self.possibleMoves:
            self.itemconfig(id, outline="yellow")
            self.tag_bind(id, "<ButtonPress-1>", self.onClickMove)

    def showNormalMove(self, show, selectedPiece):
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

    def showHitMove(self, show, selectedPiece):
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

    def checkWins(self):
        text = 'no wins'
        if self.AINumber <= 0:
            text = 'Player Wins'
        elif self.playerNumber <= 0:
            text = 'AI Wins'
        if text == 'no wins':
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.pieces[i][j] is not None and self.pieces[i][j].isAI == self.isAI:
                        self.showNormalMove(False, self.pieces[i][j])
                        if len(self.possibleMoves) != 0:
                            self.possibleMoves.clear()
                            return
                        self.showHitMove(False, self.pieces[i][j])
                        if len(self.possibleMoves) != 0:
                            self.possibleMoves.clear()
                            return
            if self.isAI:
                text = 'Player Wins'
            else:
                text = 'AI Wins'
        self.delete(ALL)
        self.label = Label(self.master,
                           compound=CENTER,
                           text=text,
                           fg="white",
                           bg="black", font="Helvetica 25 bold italic")
        self.label.place(x=410, y=390, anchor="center")
        self.again = Button(self.master, text="Restart", command=self.restart)
        self.again.place(x=410, y=410, anchor="center")
        self.pack_forget()
        self.cancel.pack_forget()

    def restart(self):
        self.destroy()
        self.master.destroy()
        # self.again.place_forget()
        # self.label.place_forget()
        self.__init__(720)
        self.run()


if __name__ == '__main__':
    b = Game(720)
    b.run()