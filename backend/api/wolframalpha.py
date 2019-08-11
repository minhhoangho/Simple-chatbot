import requests
import wolframalpha
import random
from api.chemical_balancer import balancer
APP_ID = 'HAXXWJ-TTLV7WAGP5'
client = wolframalpha.Client(APP_ID)

from googletrans import Translator
traslator = Translator()

def removeBrackets(variable):
    return variable.split('(')[0]


def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']





def search_and_solve(input, is_general=True):
    input = traslator.translate(input, dest='en')
    input = input.text
    print(input)
    URL = 'http://api.wolframalpha.com/v2/result?appid=%s&input=%s' % (APP_ID, input)
    try:
        res = None
        print("Is generall: --->",is_general)
        if is_general == True:
            res = requests.get(URL)
            print(res.content)
            if res.status_code == 200:
                return {
                    "result": traslator.translate(str(res.content, 'utf-8'), dest='vi').text
                }
        else:
            res = client.query(input)
            if res['@success'] == 'true':
                try:
                    res = next(res.results)
                    print(res)
                    if int(res['@numsubpods']) > 1:
                        res = [el['plaintext'] for el in res['subpod']]
                        res = ",".join(res)
                    else:
                        res = res['subpod']['plaintext']
                    return {
                        "result": res
                    }
                except:
                    res = res['pod'][1]
                    if int(res['@numsubpods']) > 1:
                        res = [el['plaintext'] for el in res['subpod']]
                        res = ",".join(res)
                    else:
                        res = res['subpod']['plaintext']
                    return {
                        "result": res
                    }
            elif res['didyoumeans']:
                # print(res['didyoumeans'])
                related_question = res['didyoumeans']
                if int(related_question['@count'])>1:
                    for related in related_question["didyoumean"]:
                        return search_and_solve(related["#text"], is_general=False)
                else:
                    return search_and_solve(related_question["didyoumean"]["#text"], is_general=False)

        return {"result": False}
    except:
        return {"result": False}
