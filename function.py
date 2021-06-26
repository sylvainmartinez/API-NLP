import nltk
from nltk.stem.snowball import FrenchStemmer, EnglishStemmer
from nltk.stem import WordNetLemmatizer

def tokensLem(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = EnglishStemmer()
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    for j, word in enumerate(tokens):
        tokens[j] = lemmatizer.lemmatize(word)
    return tokens
