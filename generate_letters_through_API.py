import random
from wordsapy import Dictionary

API_ENDPOINT = 'https://wordsapiv1.p.mashape.com/words'
API_KEY = 'api key goes here'

class Letters:
    def __init__(self):
        self.valid: bool
        self.dictionary = Dictionary(api_key=API_KEY)
        self.user_letters: list
        self.GetUserLetters()

    def GetUserLetters(self):
        space_exists = True
        while space_exists:
            word = self.dictionary.random(letters = 8)

            # API Generates ' ' spaces as well as '-' dashes, so check if there is any spaces. Keep generating until there is none.
            if ' ' not in word['word'] and '-' not in word['word']:
                space_exists = False

        # print(f'From Class: {word["word"]}')
        picked_letters = list(word['word'])
        random.shuffle(picked_letters)
        # print(picked_letters)
        self.user_letters = picked_letters
    
    def CheckWord(self, char_list):
        word_str = "".join(char_list)
        try:
            check_validity_through_api = self.dictionary.word(word=word_str)
            # print(check_validity_through_api)
        except:
            self.valid = False
        else:
            self.valid = True
