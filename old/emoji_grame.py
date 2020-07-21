import pandas
from collections import Counter
import emoji
import pickle
import re
from emoji import unicode_codes


#pd = pandas.read_csv("/data/06333/aroraish/rest.csv", encoding='utf-8')
pd2 = pandas.read_csv("/data/06333/aroraish/modifiableE.csv", encoding='utf-8', error_bad_lines=False)
#pd3 = pandas.read_csv("/data/06333/aroraish/modifiableN.csv", encoding='utf-8', error_bad_lines=False)


c1 = Counter()
c2 = Counter()
c3 = Counter()
c4 = Counter()

"""a1 = Counter()
a2 = Counter()
a3 = Counter()
a4 = Counter()"""


emojicols = [u"\U0001f3fb", u"\U0001f3fc", u"\U0001f3fd", u"\U0001f3fe", u"\U0001f3ff"]
pattern = u'(' + u'|'.join(re.escape(u) for u in emojicols) + u')'

allCols = re.compile(pattern)

emojiss = unicode_codes.EMOJI_ALIAS_UNICODE
coloured = set()

for key in emojiss:
    if(allCols.findall(emojiss[key])):
        coloured.add(emojiss[key])
        coloured.add(allCols.sub('',emojiss[key]))

#have to remove empty string
coloured.remove(u"")
emojis = sorted(coloured, key=len,
                        reverse=True)
pattern2 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

colouredRE = re.compile(pattern2)


emojis = sorted(emojiss.values(), key=len,
                        reverse=True)
pattern3 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

#ree gets modifiable emojis
ree = re.compile(pattern3)


#calculates n grams
def n_all(message):
    tokens = ree.findall(message)
    n1grams = zip(*[tokens[i:] for i in range(1)])
    n2grams = zip(*[tokens[i:] for i in range(2)])
    n3grams = zip(*[tokens[i:] for i in range(3)])
    n4grams = zip(*[tokens[i:] for i in range(4)])
    
    result1 = [" ".join(ngram) for ngram in n1grams]
    result2 = [" ".join(ngram) for ngram in n2grams]
    result3 = [" ".join(ngram) for ngram in n3grams]
    result4 = [" ".join(ngram) for ngram in n4grams]
    
    for ng in result1:
        c1[ng] += 1
        
    for ng in result2:
        c2[ng] += 1
        
    for ng in result3:
        c3[ng] += 1
        
    for ng in result4:
        c4[ng] += 1
        
        
"""def n_col(message):
    tokens = colouredRE.findall(message)
    n1grams = zip(*[tokens[i:] for i in range(1)])
    n2grams = zip(*[tokens[i:] for i in range(2)])
    n3grams = zip(*[tokens[i:] for i in range(3)])
    n4grams = zip(*[tokens[i:] for i in range(4)])
    
    result1 = [" ".join(ngram) for ngram in n1grams]
    result2 = [" ".join(ngram) for ngram in n2grams]
    result3 = [" ".join(ngram) for ngram in n3grams]
    result4 = [" ".join(ngram) for ngram in n4grams]
    
    for ng in result1:
        a1[ng] += 1
        
    for ng in result2:
        a2[ng] += 1
        
    for ng in result3:
        a3[ng] += 1
        
    for ng in result4:
        a4[ng] += 1
"""        
        
#s = pd3['message']
s2 = pd2['message']
#s.apply(n_all)
s2.apply(n_all)
#s2.apply(n_col)

pickle.dump(c1, open("/data/06333/aroraish/counter_all_1.pkl", "w"))
pickle.dump(c2, open("/data/06333/aroraish/counter_all_2.pkl", "w"))
pickle.dump(c3, open("/data/06333/aroraish/counter_all_3.pkl", "w"))
pickle.dump(c4, open("/data/06333/aroraish/counter_all_4.pkl", "w"))
"""pickle.dump(a1, open("/data/06333/aroraish/counter_col_1.pkl", "w"))
pickle.dump(a2, open("/data/06333/aroraish/counter_col_2.pkl", "w"))
pickle.dump(a3, open("/data/06333/aroraish/counter_col_3.pkl", "w"))
pickle.dump(a4, open("/data/06333/aroraish/counter_col_4.pkl", "w"))"""