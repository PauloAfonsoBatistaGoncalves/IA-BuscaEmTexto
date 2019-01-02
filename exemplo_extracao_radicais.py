import nltk 

stemmer = nltk.stem.RSLPStemmer()

stemmer.stem('nova')
stemmer.stem('novamente')