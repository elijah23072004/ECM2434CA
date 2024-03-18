import random
from ecomap.models import Word
from django.core.exceptions import ObjectDoesNotExist

class Games:
    def __init__(self):
        pass

    def addWord(self, word, definition):
        # remove the word if it already exists
        self.removeWord(word)
        word = Word(term=word.title(), definition=definition)
        word.save()

    def removeWord(self, word):
        try:
            word = Word.objects.get(term=word.title())
        except ObjectDoesNotExist:
            return
        word.delete()


    def getRandomWord(self):
        words = Word.objects.all()
        words = list(words)
        if len(words) <= 0:
            return "Recycle"
        return random.choice(words).term.strip()

    def getSingleWord(self, length=10):
        # return a word shorter or equal to length and with no whitespaces
        words = Word.objects.all()
        words = list(words)
        random.shuffle(words)
        for word in words:
            term = word.term
            if " " not in term and len(term) < length:
                return term
        return "Recycle"

    def getDefinition(self, word):
        word = Word.objects.get(term=word.title())
        return word.definition.strip()