import requests
import json
from DB import Db


class Gtranslate():

    def translate(self, sl, tl, word, dbs=True):
        if dbs:
            dbc = Db(sl + "2" + tl + ".db")
            dbm = dbc.searchMean(word)
            if dbm is not False:
                return {"exact":dbm[2], "pron":dbm[4], "othermean":dbm[3], "Error":None}
        else:
            dbc = Db("en2fa.db")
            dbm = dbc.searchMean(word)
            if dbm is not False:
                return {"exact":dbm[2], "pron":dbm[4], "othermean":dbm[3], "Error":None}
        try:
            word = str(word).replace(".", "")
            if sl == "":
                treq = requests.get(url="https://translate.google.com//translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=360000c&tl={0}tl&hl={1}&q={2}".format(tl, tl, word), headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36"}, proxies={})
            else:
                treq = requests.get(url="https://translate.google.com//translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=360000c&sl={0}sl&tl={1}tl&hl={2}&q={3}".format(sl, tl, tl, word), headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36"}, proxies={})

        except:
            return {"exact": "Connection Error", "pron":None, "othermean":None, "Error": "Connection Error!!\nCheck Your Internet Connection!"}
        try:
            jsn = json.loads(treq.text)
        except:
            return {"exact": "Connection Error", "pron": None, "othermean": None, "Error": "Connection Error!!\nCheck Your Internet Connection!"}
        err = None
        exactmean = jsn[0][0][0]
        if jsn[1] == None:
            err = "t1"
            pron = None
            othmean = None
        else:
            if len(jsn[0]) > 1 and len(jsn[0][1]) >= 4:
               pron = jsn[0][1][3]
            else:
                pron = None
            othmean = jsn[1][0][1]
        if err is None or err == "t1":
            if sl == "":
                sl = str(jsn[8][0][0])
                dbc = Db(sl + "2" + tl + ".db")
            dbc.insertWord(word, exactmean, othmean, pron)
        return {"exact":exactmean, "pron":pron, "othermean":othmean, "Error":err}
