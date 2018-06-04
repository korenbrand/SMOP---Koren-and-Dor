class Move:
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self, start, end, is_vertical_move):
        self.start = start  # tuple describe the candy (row,col) before the switch
        self.end = end  # tuple describe the candy (row,col) before the switch
        self.is_vertical_move = is_vertical_move

