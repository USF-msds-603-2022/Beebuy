import numpy as np
import pandas as pd
import nltk
from nltk.stem.porter import *
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

"""
input:
1. list of keyword
2. a string of text

from keyword_sentiment import keyword_sentiment
keyword_sentiment(text,keyword_list)

output:
{'keyword1':score, 'keyword1': score .....}
"""

def tokenize(text):
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3, strip digits.
    """
    text = text.lower()
    text = re.sub('[' + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    tokens = nltk.word_tokenize(text)
    stopwords = list(ENGLISH_STOP_WORDS)
    tokens = [w for w in tokens if w not in stopwords and len(w) > 2]  # ignore a, an, to, at, be, ...
    
    return tokens

def stemwords(words):
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stemmer =PorterStemmer()
    return [stemmer.stem(w) for w in words]

def tokenizer(text):
    return stemwords(tokenize(text))

def tokenize_keyword(keyword_list):
    kw = ' '.join(keyword_list)
    return tokenizer(kw)

def get_phrases(text,kw):
    token_text = tokenizer(text)
    token_kw = tokenize_keyword(kw)
    
    phrases = []
    for i in range(len(token_text)):
        if token_text[i] in token_kw:
            phrases.append(' '.join(token_text[i-1:i+2]))
            
    return phrases

def sentiment_scores(phrases):
    key_score = {}
    sid = SentimentIntensityAnalyzer()
    for p in phrases:
        score = sid.polarity_scores(p)['compound']
        words = p.split()
        idx = len(words)//2
        key = words[idx]
        
        if key in key_score.keys():
            key_score[key].append(score)
        else:
            key_score[key]=[score]
            
    for k,v in key_score.items():
        key_score[k] = np.mean(v)
        
    return key_score

def keyword_sentiment(text,kw):
    return sentiment_scores(get_phrases(text,kw))
