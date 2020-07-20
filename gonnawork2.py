import csv
import time
import json
import emoji
import re
import pickle
from emoji import unicode_codes


filename = "/data/06333/aroraish/ut_venmo_2018.json"
brokenlines = "/data/06333/aroraish/broken4.txt"


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

total = 0
emojim = 0
emojit = 0

with open(filename, 'r') as f, open("/data/06333/aroraish/modifiableE.csv", 'w') as m, open("/data/06333/aroraish/modifiableN.csv", "w") as mn, open("/data/06333/aroraish/rest.csv","w") as r, open(brokenlines, 'w') as bf:
    fieldnames = ['id', 'type', 'message', 'time']
    csvwrt = csv.DictWriter(m, fieldnames=fieldnames)
    csvwrt.writeheader()

    csvwrt = csv.DictWriter(mn, fieldnames=fieldnames)
    csvwrt.writeheader()

    csvwrt = csv.DictWriter(r, fieldnames=fieldnames)
    csvwrt.writeheader()

    mod = csv.writer(m)
    modnon = csv.writer(mn)
    rest = csv.writer(r)

    for line in f:
        total += 1
        try:
            j = json.loads(line)
            message = j[u'message']
            time = j[u'created_time']
            payment_id = str(j[u'payment_id'])
            what_type = j[u'type']
	        
            if(len(colouredRE.findall(message)) > 0):
                emojim+=1
                mod.writerow([payment_id.encode("utf-8"), what_type.encode("utf-8"), message.encode("utf-8"), time.encode("utf-8")])
            elif(len(ree.findall(message)) > 0):
                emojit += 1
                modnon.writerow([payment_id.encode("utf-8"), what_type.encode("utf-8"), message.encode("utf-8"), time.encode("utf-8")])
	    else:
                rest.writerow([payment_id.encode("utf-8"), what_type.encode("utf-8"), message.encode("utf-8"), time.encode("utf-8")])
        except:
            total -= 1
            bf.write(line)


te = [total, emojim, emojit]
pickle.dump(te, open("stats.pkl","w"))






