from random import randint, sample
from math import sqrt

START_COORD = [(6, 2)]
END_COORD = [(10, 7)]
COORDS = [(12, 2), (16, 2), (17, 5), (14, 7), (17, 17), (13, 17), (5, 15), (2, 9), (8, 5), (11, 10)]

class Traveling:
    def __init__(self, coords):
        self.coords = coords