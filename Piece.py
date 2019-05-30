class Piece:
    def __init__(self, row, col, isAI, id):
        self.col = col
        self.row = row
        self.isAI = isAI
        self.isKing = False
        self.id = id

    def moveTo(self, newRow, newCol):
        self.row = newRow
        self.col = newCol
        if self.row == 0 and not self.isAI:
            self.isKing = True
        elif self.row == 7 and self.isAI:
            self.isKing = True

    def getNortheast(self):
        if self.row > 0 and self.col < 7:
            return [self.row - 1, self.col + 1]
        return -1

    def getNorthwest(self):
        if self.row > 0 and self.col > 0:
            return [self.row - 1, self.col - 1]
        return -1

    def getSoutheast(self):
        if self.row < 7 and self.col < 7:
            return [self.row + 1, self.col + 1]
        return -1

    def getSouthwest(self):
        if self.row < 7 and self.col > 0:
            return [self.row + 1, self.col - 1]
        return -1


if __name__ == '__main__':
    p = Piece(1, 2, False)
    print(p.getNortheast()[0])
