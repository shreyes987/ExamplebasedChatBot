import csv
import re
import random
from similarity import sent_sim
from bs4 import BeautifulSoup as bs
import requests
import re

class match():
    nlp = None
    def __init__(self,nlp):
        self.nlp = nlp

    def find_match(self,inp,sim_thresh):
        with open('resources/qa_1.csv','r') as f:
            reader = csv.reader(f)
            re_res,sim_res = None,None
            row1,row2 = None,None
            smax = None

            max = 0

            #regEx matching with dataset
            for row in reader:
                if(re.search(row[1],inp)):
                    re_res = row
                    break

            #get back to first line
            f.seek(0)

            #remove ? from input
            inp = inp.replace("?","")

            abc = []
            #similarity matching
            max = 0
            for row in reader:
                ip = [i for i in row[2].split() if i[0] != "\\"]
                if sent_sim(self.nlp(" ".join(ip)),self.nlp(inp)) > 0.80:
                    abc.append(row)

                t = sent_sim(self.nlp(" ".join(ip)),self.nlp(inp))
                if t>max and t > 0.60:
                    # print("////////",t,row)
                    max = t
                    smax = row
            # print(abc)
            temp = False
            max = 0
            for a in abc:
                ax = "xyzxc"
                if a[3] == "*":
                    # print(a)
                    for w in self.nlp(inp).noun_chunks:
                        # print(w)
                        if not re.findall(w.text,a[2]):
                            print("><><>",abc[0][2],w.text)
                            ax = w.text
                    ip = [i[1:] for i in a[2].split() if i[0] == "\\"]
                    ip.append(a[0])
                    if len(ip)>1:
                        hits = 0
                        for i in range(1, 4):
                            web_res = []
                            req = requests.get("http://www.ask.com/web?q=" + ax + "&page=" + str(i))
                            soup = bs(req.content, 'lxml')
                            web_res = [s.get_text() for s in soup.find_all("p", {"class": "PartialSearchResults-item-abstract"})]
                            # web_res += [s.get_text() for s in soup.find_all("p", {"class": "PartialSearchResults-item-url"})]

                            for sent in web_res:
                                for word in sent.split():
                                    if re.findall(ip[0], word.lower()):
                                        hits += 1
                        print(">>>",ip,ax,hits)
                        # print(ax,hits)
                        if hits>0:
                            temp = a
                            row1 = temp
                            break
                else:
                    temp_sim = sent_sim(self.nlp(a[2]),self.nlp(inp))
                    if temp_sim > max and temp_sim > sim_thresh:
                        max = temp_sim
                        row2 = a
            # print("-----",row1,row2)
            if row1 == None:
                sim_res=row2
            else:
                sim_res=row1
            # print("SMAX: ",smax)
            #return both results
            return re_res,sim_res,smax

    def get_dominant_res(self,matches):
        if matches[0] is None and matches[1] is None:
            return None
        elif matches[1] is None:
            return matches[0]
        elif matches[0] is None:
            return matches[1]
        if int(matches[0][0]) != int(matches[1][0]):
            if float(matches[0][5]) >= float(matches[1][6]):
                return matches[0]
            else:
                return matches[1]
        else:
            return matches[0]


    def get_da(self,max_match):
        if max_match != None:
            with open("resources/da_type.csv","r") as f:
                read = csv.reader(f)
                ans = None
                for r in read:
                    print(">>>", max_match[-1], r[0])
                    if max_match[-1] == r[0]:
                        ans = r[random.randint(1,5)]
                return ans
        else:
            return "Not found in database"
