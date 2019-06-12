# from spacy.en import English
from bs4 import BeautifulSoup as bs
import requests
# import string
import re
# nlp = English()
# key = nlp("red green blue white black cyan magenta yellow")
# key = nlp("fruit")

key = "movie"
while True:
    s = input(">").replace(" ", "+")
    hits=0
    for i in range(1,4):

        web_res = []
        req = requests.get("http://www.ask.com/web?q=" + s+"&page="+str(i))
        soup = bs(req.content, 'lxml')
        web_res = [s.get_text() for s in soup.find_all("p", {"class": "PartialSearchResults-item-abstract"})]
        web_res += [s.get_text() for s in soup.find_all("p", {"class": "PartialSearchResults-item-url"})]

        for sent in web_res:
            for word in sent.split():
                if re.findall(key,word.lower()):
                    hits+=1
        print(".", hits)
    print("("+str(hits)+")")

    # s = "flavour+taste+of+"
    # s=input(">").replace(" ","+")
    # req = requests.get("http://www.ask.com/web?q="+s)
    #
    # soup = bs(req.content,'lxml')
    #
    # web_res = [s.get_text() for s in soup.find_all("p",{"class":"web-result-description"})]
    # web_res += [s.get_text() for s in soup.find_all("h2",{"class":"web-result-title"})]
    #
    # uniq = set()

    # for s in web_res:
    #     s = nlp(s.lower())
    #     for w in s:
    #         uniq.add(w)

    # ret = []

    # for s in uniq:

         # if nlp(s.text).similarity(key) > 0.80:
         #     ret.append(s)
    # print(ret)


