import random
import json

class Letters:
    def __init__(self):
        self.valid: bool
        self.user_letters: list
        self.GetUserLetters()

    def GetUserLetters(self):
        with open('word_generator.json') as generatable_words_files:
            all_words = json.load(generatable_words_files)

        picked_word = random.choice(list(all_words.keys()))

        # print(f'From Class: {word["word"]}')
        picked_letters = list(picked_word)
        random.shuffle(picked_letters)
        # print(picked_letters)
        self.user_letters = picked_letters
    
    def CheckWord(self, char_list):
        word_str = "".join(char_list)

        with open('words_dictionary.json') as complete_dictionary:
            data = json.load(complete_dictionary)

        try:
            word = data[word_str]
        except KeyError:
            self.valid = False
        else:
            self.valid = True