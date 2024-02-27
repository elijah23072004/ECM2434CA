import os
import random

class Games:


    def __init__(self):
        self.file_path = os.path.abspath(os.path.dirname(__file__)) + "/eco_words.txt"
        self.words = self.readWordsFile()

    def readWordsFile(self):
        #get the words from the eco_words file
        with open(self.file_path, "r") as f:
            file = f.read()
        words = file.split("\n")

        #remove any empty words and strip the words in case any whitespace at start or end
        words_cleaned = []
        for word in words:
            if word.replace(" ", "") != "":
                words_cleaned.append(word.strip())
        return words_cleaned

    def getRandomWord(self):
        return random.choice(self.words)

    def getSingleWord(self, length=10):
        word = self.getRandomWord()
        while " " in word or len(word) > length:
            word = self.getRandomWord()
        return word
