import random

TOTAL_CHAR = 7

class Generate:
    def __init__(self):
        self.placeholder = []
        word1_len = random.randint(2,5)
        word2_len = TOTAL_CHAR - word1_len
        self.placeholder = [word1_len, 0, word2_len]