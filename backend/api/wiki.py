import requests
from urllib import parse
import wikipedia
import random
wikipedia.set_lang('vi')
def search(s):
    try:
        s = wikipedia.search(s)[:3]
        summary = wikipedia.summary(random.choice(s), sentences=2)
        return {
            "result": summary
        }
    except:
        return {
            "result": False
        }
