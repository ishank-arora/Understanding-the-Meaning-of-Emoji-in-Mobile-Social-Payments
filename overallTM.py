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
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
from gensim.test.utils import datapath
from gensim import corpora, models
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


files = ["flat_medium_dark_proc_2.csv", "flat_medium_proc_2.csv", "flat_medium_light_proc_2.csv", "flat_light_proc_2.csv", "flat_yellow_proc_2.csv"]
path = "/data/06333/aroraish/flat/"


pd = pandas.read_csv("/data/06333/aroraish/flat/flat_dark_proc_2.csv", encoding='utf-8', error_bad_lines=False)

processed_docs = pd[u'message'].map(n_all)
dictionary = gensim.corpora.Dictionary(processed_docs)

dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]


tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=25, id2word=dictionary, passes=2)

lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=25, id2word=dictionary, passes=2)


for f in files:
    toRead = path + f
    pd = pandas.read_csv(toRead, encoding='utf-8', error_bad_lines=False)

    processed_docs = pd[u'message'].map(n_all)
    dictionary = gensim.corpora.Dictionary(processed_docs)

    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]

    lda_model.update(bow_corpus, num_topics=25, id2word=dictionary, passes=2)
    lda_model_tfidf.update(corpus_tfidf, num_topics=25, id2word=dictionary, passes=2)


temp_file = datapath("/data/06333/aroraish/models/ModEModelBOW")
lda_model.save(temp_file)

temp_file = datapath("/data/06333/aroraish/models/ModEModelTFIDF")
lda_model_tfidf.save(temp_file)

with open("/data/06333/aroraish/outputs/lda_bag_of_words_overall.txt", 'w') as bw:

    for idx, topic in lda_model.print_topics(-1):
        bw.write('Topic: {} \nWords: {}\n\n'.format(idx, topic.encode('utf-8')))


with open("/data/06333/aroraish/outputs/lda_tfidf_overall.txt", 'w') as tf:

    for idx, topic in lda_model_tfidf.print_topics(-1):
        tf.write('Topic: {} \nWord: {}\n\n'.format(idx, topic.encode('utf-8')))
