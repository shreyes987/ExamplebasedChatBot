# from spacy import load
import csv
from os import walk
from re import findall
# nlp = load("en")
#
#
#


class diary():
    nlp = None
    def __init__(self, nlp):
        self.nlp = nlp

    # sent must be nlp()
    def get_sent_type(self,sent):
        sent_type = []
        with open("resources/qna.csv","r") as f:
            read = csv.reader(f)
            max=0
            for r in read:
                if r:
                    lem_r = " ".join([i.lemma_ for i in self.nlp(r[0])])
                    lem_sent = " ".join([i.lemma_ for i in sent])
                    temp = self.nlp(lem_r).similarity(self.nlp(lem_sent))
                    # print(r,s)
                    if temp>max:
                        max=temp
                        sent_type = r
            f.seek(0)
            return sent_type

    #I am 10 Years old, How old am I (both string)
    def get_ques_relevance(self,sent_type,ques):
        max = 0
        for i in range(1,3):
            temp = self.nlp(sent_type[i]).similarity(self.nlp(ques))
            if temp > max:
                max = temp
        # print("--",max,"--")
        if max > 0.80:
            return [True,max]
        else:
            return [False,max]

    # both string
    def extract_ans(self,inp,ques):
        # print(inp,ques)
        ans,nc = [],[]
        inp = inp.replace(".","")
        nlp_inp = self.nlp(inp)
        nlp_ques = self.nlp(ques)
        inp,ques = self.nlp(inp),self.nlp(ques)
        inp = [i.lemma_.lower() for i in inp]
        ques = [q.lemma_.lower() for q in ques]
        # print("><><><><",inp,ques)
        for i in inp:
            if i not in ques:
                ans.append(i)
        inpnc,qunc = [],[]
        for n in nlp_inp.noun_chunks:
            inpnc.append(n.text.lower())
        for n in nlp_ques.noun_chunks:
            qunc.append(n.text.lower())
        flag = True
        # print(inpnc,qunc)
        for i in inpnc:
            if i in qunc:
                flag = True
                break
            else:
                flag = False

        if flag:
            return " ".join(ans)
        else:
            # print(nlp_inp.similarity(nlp_ques))
            return None

    def get_entries(self,user):
        # print("getentry ",user)
        entries = []
        for x in walk("users/"+user+"/"):
            for a in x[2]:
                # print(">>>",a)
                if findall(".txt",a):
                    # print("hello")
                    with open("users/"+user+"/"+a,"r") as f:
                        entries.append(f.read())
                    # print(entries)
        # print(entries)
        return entries

    def loop_qs(self,qs,dia):
        # print("loop: ",qs,dia)
        ans = None
        # print("dia: ",dia)
        for d in dia:
            d = self.nlp(d)
            max = 0
            f_ans = None
            # print("d: ",d)
            for s in d.sents:
                s_type = self.get_sent_type(s)
                print("-----",s,s_type)
                q_rel = self.get_ques_relevance(s_type,qs)
                print("q_rel: ",q_rel)

                if q_rel[0]:
                    ans = self.extract_ans(s.text,qs)
                    # print("[][][][]",ans)
                    # print("max: ",max)
                    if q_rel[1]>max:
                        # print("hello")
                        max = q_rel[1]
                        f_ans = ans
        if f_ans is not None:
            return f_ans
        else:
            return "I don't know what you are saying"
    # user = "My name is Shubham"
    # inp = [s for s in nlp(user).sents]
    # qs = ["what is my name"]
    #
    # for s in inp:
    #     s_type = get_sent_type(s)
    #     for q in qs:
    #         if get_ques_relevance(s_type,q):
    #             ans = extract_ans(s.text,q)
    #             if ans is not None:
    #                 print("ans: ",ans)

# d = diary(nlp)
# dia = d.get_entries("karan")
# d.loop_qs("what was he suffering from",dia)
