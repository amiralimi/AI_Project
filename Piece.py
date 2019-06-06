class Piece:
    def __init__(self, row, col, isAI, id):
        self.col = col
        self.row = row
        self.isAI = isAI
        self.isKing = False
        self.id = id
        self.canMoveAgain = False

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
        return None

    def getNorthwest(self):
        if self.row > 0 and self.col > 0:
            return [self.row - 1, self.col - 1]
        return None

    def getSoutheast(self):
        if self.row < 7 and self.col < 7:
            return [self.row + 1, self.col + 1]
        return None

    def getSouthwest(self):
        if self.row < 7 and self.col > 0:
            return [self.row + 1, self.col - 1]
        return None

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    def __str__(self):
        return str(self.id) + " " + str(self.row) + " " + str(self.col) + " " + str(self.isAI)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    p = Piece(1, 2, False)
    print(p.getNortheast()[0])
