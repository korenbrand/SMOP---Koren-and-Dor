# this function is part of board class
def possible_moves(self):
    horizontal_moves = []
    vertical_moves = []
    ########################
    # check horizontal moves
    ########################
    for row in range(self.height):
        for col in range(self.width - 1):
            self.make_move((row, col), (row, col + 1))  # make move only for checking for matching
            if row_matches(row):
                horizontal_moves.append(Move((row, col), (row, col + 1), HORZ))
            self.make_move((row, col), (row, col + 1))  # return to the original board by commit the move again
    ########################
    # check vertical moves
    ########################
    for col in range(self.width):
        for row in range(self.height - 1):
            self.make_move((row, col), (row + 1, col))  # make move only for checking for matching
            if col_matches(col):
                vertical_moves.append(Move((row, col), (row + 1, col), VERT))
            self.make_move((row, col), (row + 1, col))  # return to the original board by commit the move again

    return horizontal_moves, vertical_moves


def cascade(self):
    for col in range(self.width):
        for row in range(self.height - 1, -1, -1):
            col_is_empty = False
            if self.board[(row, col)].empty:
                tmp_row = row  # we don't want to override the original row
                while self.board[(tmp_row, col)].empty:
                    if tmp_row == 0:  # this is the higher candy in the col
                        col_is_empty = True
                        break
                    tmp_row -= 1
                if col_is_empty:
                    break
                else:
                    self.make_move((row, col), (tmp_row, col))
