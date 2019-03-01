import spacy

class nlpModel:
    def __init__(self):
        self.nlp = spacy.load('en')