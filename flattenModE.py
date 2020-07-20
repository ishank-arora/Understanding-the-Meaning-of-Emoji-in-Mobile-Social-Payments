import csv
import time
import json
import emoji
import re
import pandas as pd
import pickle
from emoji import unicode_codes
import pprint
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

emojicols = [u"\U0001f3fb", u"\U0001f3fc", u"\U0001f3fd", u"\U0001f3fe", u"\U0001f3ff"]
pattern = u'(' + u'|'.join(re.escape(u) for u in emojicols) + u')'

allCols = re.compile(pattern)

all_emojis_dict = unicode_codes.EMOJI_ALIAS_UNICODE


coloured = set()

for key in all_emojis_dict:
    if(allCols.findall(all_emojis_dict[key])):
        coloured.add(all_emojis_dict[key])
        coloured.add(allCols.sub('',all_emojis_dict[key]))

coloured.remove(u"")
emojis = sorted(coloured, key=len,
                        reverse=True)
pattern2 = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'

colouredRE = re.compile(pattern2)

def get_color(text):
    first_emoji = re.search(colouredRE, text)
    if(first_emoji is None):
        return -2
    
    for i in range(len(emojicols)):
        if(emojicols[i] in first_emoji.group()):
            return i
    return -1

modifiableE = pd.read_csv("/data/06333/aroraish/modifiableE_processed2.csv", encoding='utf-8',error_bad_lines=False)

modifiableE["color"] = modifiableE["message"].apply(get_color)


yellow = modifiableE.loc[modifiableE['color'] == -1]
yellow.to_csv("/data/06333/aroraish/flat/flat_yellow_proc_2.csv",index=None, header=True)

light = modifiableE.loc[modifiableE['color'] == 0]
light.to_csv("/data/06333/aroraish/flat/flat_light_proc_2.csv",index=None, header=True)

medium_light = modifiableE.loc[modifiableE['color'] == 1]
medium_light.to_csv("/data/06333/aroraish/flat/flat_medium_light_proc_2.csv",index=None, header=True)

medium = modifiableE.loc[modifiableE['color'] == 2]
medium.to_csv("/data/06333/aroraish/flat/flat_medium_proc_2.csv",index=None, header=True)

medium_dark = modifiableE.loc[modifiableE['color'] == 3]
medium_dark.to_csv("/data/06333/aroraish/flat/flat_medium_dark_proc_2.csv",index=None, header=True)

dark = modifiableE.loc[modifiableE['color'] == 4]
dark.to_csv("/data/06333/aroraish/flat/flat_dark_proc_2.csv",index=None, header=True)
