import csv
from collections import Counter
import emoji
from emoji import unicode_codes
import pickle
import re
import pandas
import string
from num2words import num2words
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.test.utils import datapath
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
import time

#pd = pandas.read_csv("/data/06333/aroraish/rest.csv", encoding='utf-8')

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
    
def num(token):
    try:
        return num2words(token)
    except:
        return token

def n_all(message):
    #message = message.decode('utf-8')
    tokens = list()
    sp = message.split()
    for i in sp:
        l = ree.findall(i)
        if(l):
            tokens.extend(l)
        else:
            tokens.append(i)
    return sp




pd = pandas.read_csv("/data/06333/aroraish/modifiableN_processed.csv", encoding='utf-8', usecols=['message'], low_memory=False, error_bad_lines=False, chunksize=1000000)
chunklist = []

for c in pd:
    a = c[u'message'].map(n_all)
    chunklist.append(a)


processed_docs = pandas.concat(chunklist)
dictionary = gensim.corpora.Dictionary(processed_docs)

dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

pickle.dump(dictionary, open("/data/06333/aroraish/dictionary2TFNM.pkl", "w"))


from gensim import corpora, models
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=25, id2word=dictionary, passes=2, workers=1)

temp_file = datapath("/data/06333/aroraish/lda_model_tfidf_2_NM")
lda_model.save(temp_file)




#lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)

#pickle.dump(lda_model, open("/data/06333/aroraish/ldaMtfidf.pkl", "w"))

with open("/data/06333/aroraish/lda_tf_idf_2_NM.txt", 'w') as bw:

    for idx, topic in lda_model.print_topics(-1):
        bw.write('Topic: {} \nWords: {}\n\n'.format(idx, topic.encode('utf-8')))

for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}\n'.format(idx, topic.encode('utf-8')))


# with open("/data/06333/aroraish/lda_tfidf.txt", 'w') as tf:

#     for idx, topic in lda_model_tfidf.print_topics(-1):
#         tf.write('Topic: {} Word: {}\n'.format(idx, topic.encode('utf-8')))



