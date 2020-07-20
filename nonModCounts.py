import emoji
import re
from emoji import unicode_codes
from collections import Counter
import pandas
import csv
import pickle


codings = pandas.read_csv("/home/06333/aroraish/final_codings.csv", encoding='utf-8')

e_to_f = dict()
e_to_c = dict()

for index, row in codings.iterrows():
    key = row['Emoji'].strip()
    e_to_f[key] = row['final']
    e_to_c[key] = row['final_categories'] 

toPatternize = list()
for key in e_to_f:
    toPatternize.append(key)

emojis = sorted(toPatternize, key=len,
                        reverse=True)
pattern3 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

codingRE= re.compile(pattern3)

c4 = Counter()
c5 = Counter()
def func(message):
    c = Counter()
    score = 0
    emojis = codingRE.findall(message)
    for e in emojis:
        c[e_to_f[e]] += 1
    score = c[u'H'] - c[u'U']
    if score > 0:
        c4[u'H'] += 1
    elif score < 0:
        c4[u'U'] += 1
    else:
        c4[u'C'] += 1

emojiss = unicode_codes.EMOJI_ALIAS_UNICODE
emojis = sorted(emojiss.values(), key=len,
                        reverse=True)
pattern3 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

ree = re.compile(pattern3)


def func2(message):
    score = 0
    emojis = ree.findall(message)
    #print emojis
    cc = Counter()
    if(len(emojis) == 0):
        cc[u'CONTEXT NEEDED'] += 1
    
    for e in emojis:
        if e in e_to_c:
            cc[e_to_c[e]] += 1
        else:
            cc[u'CONTEXT NEEDED'] += 1
    a = cc.most_common()
    if(len(a) > 2 and a[0][1] == a[1][1]):
        c5[u'CONTEXT NEEDED'] += 1
    else:
        c5[a[0][0]] += 1

pd = pandas.read_csv("/data/06333/aroraish/modifiableN.csv", encoding='utf-8', usecols=['message'], low_memory=False, error_bad_lines=False, chunksize=1000000)

for c in pd:
    c[u'message'].apply(func)
    c[u'message'].apply(func2)



print c4.most_common()
print c5.most_common()


pickle.dump(c4, open("nonmod-piechartFF2.pkl", "w"))
pickle.dump(c5, open("nonmod-piechartCC2.pkl", "w"))

print c4.most_common()
print c5.most_common()
