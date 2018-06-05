class Move:
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self, start, end, is_vertical_move):
        if (start[0] == end[0] and abs(start[1] - end[1]) == 1) or (start[1] == end[1] and abs(start[0] - end[0]) == 1):
            self.start = start  # tuple describe the candy (row,col) before the switch
            self.end = end  # tuple describe the candy (row,col) before the switch
            self.is_vertical_move = is_vertical_move

        else:
            # illegal move
            raise ValueError("start and end location are not adjacent")

