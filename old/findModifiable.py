import emoji
import re
from emoji import unicode_codes
from collections import Counter
import pandas
import sys


codings = pandas.read_csv("final_codings.csv", encoding='utf-8')

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


def func(message):
    c = Counter()
    score = 0
    emojis = codingRE.findall(message)
    for e in emojis:
        c[e_to_f[e]] += 1
    score = c[u'H'] - c[u'U']
    if score > 0:
        return u'H'
    elif score < 0:
        return u'U'
    else:
        return u'C'

emojiss = unicode_codes.EMOJI_ALIAS_UNICODE
emojis = sorted(emojiss.values(), key=len,
                        reverse=True)
pattern3 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

ree = re.compile(pattern3)


def func2(message):
    score = 0
    emojis = ree.findall(message)
    cc = Counter()
    for e in emojis:
        if e in e_to_c:
            cc[e_to_c[e]] += 1
        else:
            cc[u'CONTEXT NEEDED'] += 1
    a = cc.most_common()
    if(len(a) > 2 and a[0][1] == a[1][1]):
        return u'CONTEXT NEEDED'
    else:
        return a[0][0]



path = "/data/06333/aroraish/flat/"
path += sys.argv[1]
data = pandas.read_csv(path, encoding='utf-8')

print len(data[u'message'])

mg = data[u'message'].apply(func).value_counts()
print mg
mg = data[u'message'].apply(func2).value_counts()
print mg