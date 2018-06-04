class Candy:
    REGULAR, STRIPE_UP, STRIPE_SIDES, WRAP, WRAP_EXPLODE, COLOR_BOMB = 1, 2, 3, 4, 5, 6
    STRIPE_SCORE, WRAP_SCORE, COLOR_BOMB_SCORE = 120, 200, 200
    RED, BLUE, YELLOW, GREEN, PURPLE, ORANGE = 1, 2, 3, 4, 5, 6

    def __init__(self, color, type):
        self.color = color
        self.type = type
