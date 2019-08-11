import os
STOP_WORDS = None

path = os.getcwd().split("\\")
root_dir = '/'.join(path)
helper_dir = root_dir + '/NLP/main/helper'
with open(helper_dir +'/vietnamese-stopwords-dash.txt', "r", encoding="utf-8") as f:
    lines = f.read()
    STOP_WORDS = set(lines.split('\n'))
    if '' in STOP_WORDS:
        STOP_WORDS.remove('')
