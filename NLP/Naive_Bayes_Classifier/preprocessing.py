import re
import stemming

stopwords=["or","which","if","also","here","us","me","again""when","will","an","would","so","they","are","there","but","as","all","have","you","from","our","had","on","that","were","this","with","it","at","for","is","we","of","hotel","in","to","was","and","the"]

def tokenize(str):
    str=str.lower()
    tokens=re.compile("(?:[a-z][a-z']*[a-z])")
    return tokens.findall(str)
  
def stopword_removal(wordlist):
    return [w for w in wordlist if not w in stopwords]
    
def preprocessing(str):
    word=tokenize(str)
    word=stopword_removal(word)
    wordlist=stemming.stem(word)
    return word
