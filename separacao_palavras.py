import re
import nltk 

splitter = re.compile('\\W*')

stop = nltk.corpus.stopwords.words('portuguese')
stop.append('é')

lista_palavras = []

lista = [p for p in splitter.split('Este lugar é apavorante a b c c++') if p != '']

for p in lista:
    if p.lower() not in stop:
        if len(p) > 1:
            lista_palavras.append(p.lower())
            
