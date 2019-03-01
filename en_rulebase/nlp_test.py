#win10 1709版本控制台存在bug，需要引入这个包防止print意外报错
import win_unicode_console
win_unicode_console.enable()

import spacy
from spacy import displacy

nlp = spacy.load('en')

doc = nlp("i ' m not sure if you ' re being serious or not but i ' m not sure what you mean by that")


for token in doc:
    print(token.text,token.i, token.dep_, token.head.text,token.head.i, token.head.pos_,
          [child.text for child in token.children],[child.i for child in token.children])

# options = {'compact': True, 'bg': '#09a3d5',
#            'color': 'white', 'font': 'Source Sans Pro'}
# displacy.serve(doc, style='dep', options=options)

displacy.serve(doc, style='dep')