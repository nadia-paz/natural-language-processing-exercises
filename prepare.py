import pandas as pd
import numpy as np
import unicodedata
import re
import nltk
from nltk.corpus import stopwords

import acquire

def basic_clean(s:str) -> str:
    '''
    Makes a first basic clean:
        Lowercase everything
        Normalize unicode characters
        Replace anything that is not a letter, number, whitespace or a single quote.
    Parameters:
        s -> string to clean
    Returns:
        s -> cleaned string
    '''
    # all leters to lower case
    s = s.lower()
    # leave only ascii symbols
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    # using regex remove everything that is not a letter a-z, number 0-9, whitespace \s or single quote\'
    s = re.sub('[^a-z0-9\'\s]', '', s)
    
    return s

def tokenize(s:str, return_str: bool = True) -> str or list:
    '''
    Tokenizes all words in the string
    
    Parameters:
        s -> string to be tokenized
        return_list -> boolean:
            if False -> returns list of words
            if True -> returs a tokenized string
    Returns:
        a tokenized string or list of tokenized words
    '''
    # define the Tokenizer
    tokenize = nltk.tokenize.ToktokTokenizer()
    if return_str:
        # returns a string
        return tokenize.tokenize(s, return_str=True)
    else:
        # returns a list of words
        return tokenize.tokenize(s, return_str=False)

def stem(s:str) -> str:
    '''
    Applies stemming to all the words
    
    Parameters:
        s: original string
    Returns:
        s: string with word's stems
    '''
    # define the PorterStemmer
    ps = nltk.porter.PorterStemmer()
    # create a list with stems of words
    stems = [ps.stem(word) for word in s.split()]
    # join the words together as a string where words are separated by whitespace and return it
    return ' '.join(stems)

def lemmatize(s:str) -> str:
    '''
    Applies the lemmatization to each word in the passed string
    
    Parameters:
        s: string
    Returns: string with lemmatized words
    ----
    If the function doesn't work after importing nltk package 
    run nltk.download('all') in order to download all helper files
    '''
    # create a lemmatizer
    wnl = nltk.WordNetLemmatizer()
    # save lemmatized words into a list of words
    lemmas = [wnl.lemmatize(word) for word in s.split()]
    # join the words together as a string where words are separated by whitespace and return it
    return ' '.join(lemmas)

def remove_stopwords(s:str,extra_words:list or str = '', exclude_words:list or str = '') -> str:
    '''
    Obtains the list of stopwords in English. Optional: adds or removes certain words from the list.
    Removes the stopwords from the string.
    
    Parameters:
        s: string, original text were the stopwords should be removed
        extra_words: string, single word or list of strings with words to be added to the stoplist
        exclude_words: string, single word or list of strings with words to be removed from the stopwords list
    Returns:
        s: string, the text with stopwords removed from it
    '''
    # string to lower case
    s = s.lower()
    # create a list of stopwords in English
    stopwords_english = stopwords.words('english')
    
    # extra_words
    # if extra_words is a string, append the word
    if type(extra_words) == str:
        stopwords_english.append(extra_words)
    else: # if it is a list of words
        # add that list of words to list of stopwords
        stopwords_english += extra_words
    
    # exclude_words
    # if exclude_words is a single word string and this words is in stopwords list
    if type(exclude_words) == str and (exclude_words in stopwords_english):
        # remove that word from the stopwords list
        try:
            stopwords_english.remove(exclude_words)
        except ValueError:
            pass  
    # if the exclude_words is a list of words
    if type(exclude_words) == list:
        # for every word remove it from the list
        for word in exclude_words:
            try:
                stopwords_english.remove(word)
            except ValueError:
                pass
    # return a string without stopwords
    return ' '.join([word for word in s.split() if word not in stopwords_english])

####### APPLY FUNCTIONS
# acquire a data from inshorts.com website
news_df = pd.DataFrame(acquire.get_news_articles())
# news_df transformations
# rename columns
news_df.rename({'content':'original'}, axis=1, inplace=True)
# create a column 'clean' lower case, ascii, no stopwords
news_df['clean'] = news_df.original.apply(basic_clean).apply(tokenize).apply(remove_stopwords,extra_words="'")
# only stems
news_df['stemmed'] = news_df.clean.apply(stem)
# only lemmas
news_df['lemmatized'] = news_df.clean.apply(lemmatize)

# acquire data from codeuo blod
codeup_df = pd.DataFrame(acquire.get_blog_articles())
# rename columns
codeup_df.rename({'content':'original'}, axis=1, inplace=True)
# create a column 'clean' lower case, ascii, no stopwords
codeup_df['clean'] = codeup_df.original.apply(basic_clean).apply(tokenize).apply(remove_stopwords,extra_words="'")
# only stems
codeup_df['stemmed'] = codeup_df.clean.apply(stem)
# only lemmas
codeup_df['lemmatized'] = codeup_df.clean.apply(lemmatize)

# If your corpus is 493KB, would you prefer to use stemmed or lemmatized text? - lemmatized
# If your corpus is 25MB, would you prefer to use stemmed or lemmatized text? - depends on the memory, but prefer lemmatize
# If your corpus is 200TB of text and you're charged by the megabyte for your hosted computational resources, would you prefer to use stemmed or lemmatized text?
# - stemmed