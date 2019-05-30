from tkinter import *
from Piece import Piece
from array import *


class Board(Canvas):

    def __init__(self, size):
        self.size = size
        self.rows = 8
        self.cols = 8
        self.gridBox = Tk()
        self.gridBox.minsize(size + 100, size + 100)
        self.board = [[0 for x in range(self.rows)] for y in range(self.cols)]

    def run(self):
        Canvas.__init__(self , self.gridBox,bg='black', height=self.size, width=self.size)
        self.pack()
        self.makeBoard()
        self.putPiece()
        self.gridBox.mainloop()

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
                self.create_rectangle(j * size + .75, i * size + .75, j * size + size - .75, i * size + size - .75, fill=color)
                color = self.changeColor(color)

    def putPiece(self):
        size = self.size / 8
        put = False
        for i in range(3):
            put = not put
            for j in range(self.cols):
                if put:
                    id = self.create_oval(j * size + 4, i * size +4, j * size + size-4, i * size + size - 4, fill="black")
                    self.tag_bind(id, "<ButtonPress-1>", self.onClick)
                    self.board[i][j] = Piece(i, j, True)
                put = not put
        put = True
        for i in range(7, 4, -1):
            put = not put
            for j in range(self.cols):
                if put:
                    id = self.create_oval(j * size+4, i * size+4, j * size + size - 4, i * size + size - 4, fill="red")
                    self.tag_bind(id, "<ButtonPress-1>", self.onClick)
                    self.board[i][j] = Piece(i, j, False)

                put = not put

    def onClick(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        idValue = self.find_closest(x, y)[0]
        print(x)
        print(y)
        print(idValue)


if __name__ == '__main__':
    b = Board(720)
    b.run()
