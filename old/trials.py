import csv
from collections import Counter
import emoji
from emoji import unicode_codes
import pickle
import re
import string
from num2words import num2words
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


#pd = pandas.read_csv("/data/06333/aroraish/rest.csv", encoding='utf-8')
#pd2 = pandas.read_csv("/data/06333/aroraish/modifiableE.csv", encoding='utf-8', error_bad_lines=False)
#pd3 = pandas.read_csv("/data/06333/aroraish/modifiableN.csv", encoding='utf-8', error_bad_lines=False)


c1 = Counter()
c2 = Counter()
c3 = Counter()
#c4 = Counter()



emojicols = [u"\U0001f3fb", u"\U0001f3fc", u"\U0001f3fd", u"\U0001f3fe", u"\U0001f3ff"]
pattern = u'(' + u'|'.join(re.escape(u) for u in emojicols) + u')'

allCols = re.compile(pattern)

emojiss = unicode_codes.EMOJI_ALIAS_UNICODE
coloured = set()

for key in emojiss:
    if(allCols.findall(emojiss[key])):
        coloured.add(emojiss[key])
        coloured.add(allCols.sub('',emojiss[key]))

coloured.remove(u"")
emojis = sorted(coloured, key=len,
                        reverse=True)
pattern2 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

colouredRE = re.compile(pattern2)


emojis = sorted(emojiss.values(), key=len,
                        reverse=True)
pattern3 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

ree = re.compile(pattern3)

        
def pipe(message):
    text = preprocess(message)
    n_all(text)
    
def num(token):
    try:
        return num2words(token)
    except:
        return token
    
def preprocess(message):
    message = message.decode("utf-8")
    toReturn = message.lower()
    #toReturn = toReturn.translate(None, string.punctuation)
    #table = string.maketrans("","")
    for c in string.punctuation:
        toReturn = toReturn.replace(c,"")
    #toReturn = re.sub(ur"\p{P}+", "", toReturn)
    toReturn = toReturn.strip()
    
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(toReturn)
    tokens_num = [num(i) for i in tokens]
    result = [i for i in tokens_num if not i in stop_words]
    stemmer= PorterStemmer()
    result2 = []
    for r in result:
        a = ree.findall(r)
        if(len(a) > 0):
            result2.append(r)
        else:
            result2.append(stemmer.stem(r))
    result3 = []
    
    lemmatizer=WordNetLemmatizer()

    for r in result2:
        a = ree.findall(r)
        if(len(a) > 0):
            result3.append(r)
        else:
            result3.append(lemmatizer.lemmatize(r))
    return result3

def n_all(message):
    tokens = message
    n1grams = zip(*[tokens[i:] for i in range(1)])
    n2grams = zip(*[tokens[i:] for i in range(2)])
    n3grams = zip(*[tokens[i:] for i in range(3)])
    #n4grams = zip(*[tokens[i:] for i in range(4)])
    
    result1 = [" ".join(ngram) for ngram in n1grams]
    result2 = [" ".join(ngram) for ngram in n2grams]
    result3 = [" ".join(ngram) for ngram in n3grams]
    #result4 = [" ".join(ngram) for ngram in n4grams]
    
    for ng in result1:
        c1[ng] += 1
        
    for ng in result2:
        c2[ng] += 1
        
    for ng in result3:
        c3[ng] += 1
        
    #for ng in result4:
    #    c4[ng] += 1









modN = csv.DictReader(open("/data/06333/aroraish/mynew.csv", "r"))

for row in modN:
    pipe(row['message'])

#modN = csv.DictReader(open("/data/06333/aroraish/modifiableN.csv", "r"))

#for row in modN:
#    pipe(row['message'])

#modN = csv.DictReader(open("/data/06333/aroraish/rest.csv", "r"))

#for row in modN:
#    pipe(row['message'])


pickle.dump(c1, open("/data/06333/aroraish/text1.pkl", "w"))
pickle.dump(c2, open("/data/06333/aroraish/text2.pkl", "w"))
pickle.dump(c3, open("/data/06333/aroraish/text3.pkl", "w"))
#pickle.dump(c4, open("/data/06333/aroraish/text4.pkl", "w"))



