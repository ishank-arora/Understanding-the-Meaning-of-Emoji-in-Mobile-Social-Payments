import csv
from collections import Counter
import emoji
from emoji import unicode_codes
import pickle
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas
import sys
reload(sys)  
sys.setdefaultencoding("utf-8")

#pd = pandas.read_csv("/data/06333/aroraish/rest.csv", encoding='utf-8')
#pd2 = pandas.read_csv("/data/06333/aroraish/modifiableE.csv", encoding='utf-8', error_bad_lines=False)
#pd3 = pandas.read_csv("/data/06333/aroraish/modifiableN.csv", encoding='utf-8', error_bad_lines=False)




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
    result = [i for i in tokens if not i in stop_words]
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
    return " ".join(result3)


pd = pandas.read_csv("/data/06333/aroraish/rest.csv", encoding='utf-8', error_bad_lines=False, chunksize=1000000)

for p in pd:
    p["message"] = p["message"].apply(preprocess)
    p.to_csv(path_or_buf="/data/06333/aroraish/rest_processed.csv", mode='a')