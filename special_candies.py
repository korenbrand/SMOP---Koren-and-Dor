

class Striped(Candy):
    def __init__(self, color, location, directions):
        Candy.__init__(self, color, location)
        self.directions = directions

    def explode(self, board):
        board[self.location[0]][self.location[1]].delete = True
        for direction in self.directions: