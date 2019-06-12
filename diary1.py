import csv
import re
import os
# queries = ["where did I go","who went to mom's home","who likes ice cream","what does mom like","what does mom love","what did I buy","who bought ice cream",
#            "what does karan like","who likes clash royale","what does karan play","who plays clash royale","what is clash royale",
#            "what is a frustrating game","where did go","who likes karan","clash royale","who likes","where did go","where did she go",
#            "what is frustrating","what do i suck at playing","who made clash royale","what did clash royale make"]
# users = "I went to mom's house. Mom likes ice cream. I bought some ice cream. Karan likes clash royale. Karan plays clash royale everyday." \
#         "Clash royale is a frustrating game.But, I love playing Clash royale."



for x in os.walk("users/karan/"):
    for a in x[2]:
        if re.findall(".csv",a):
            print(a)
    print(x[2])




class diary():
    nlp = None
    def __init__(self, nlp):
        self.nlp = nlp

    def diary_to_tuple(self,diary):
        noun, verb = [], []
        wrong_hits = 0
        diary = diary.split(".")
        for s in diary:
            s = self.nlp(s)
            tn,tv =[],[]
            for w in s.noun_chunks:
                tn.append(w.text.strip())
            noun.append(tn)
            for w in s:
                if w.pos_ is "VERB":
                    tv.append(w.lemma_)
            if len(tv) == 1:
                verb.append(tv)
            else:
                ts = self.nlp(diary[len(verb)-1])
                tv = []
                i=0
                for w in s:
                    if w.pos_ is "VERB" and i is 0:
                        tv.append(w.lemma_)
                        i+=1
                    elif w.pos_ is "VERB" and i is 1:
                        tv.append(w.lemma_)
                        break
                    elif i is 1:
                        tv.append(w.lemma_)
                verb.append([" ".join(tv)])

        tuple = []

        for i in range(len(noun)):
            if len(noun[i]) is 2  and len(verb[i]) is 1:
                tuple.append([noun[i][0],verb[i][0],noun[i][1]])
            else:
                wrong_hits += 1
        print("wrong_hits:",wrong_hits)
        return tuple

    def print_tuple_to_file(self,tuple,user,date):
        print("users/"+user+"/"+user+"_data.csv")
        for sent in tuple:
            sent[1] = sent[1].replace(" ","-")
            with open("users/"+user+"/"+user+"_data.csv", "a") as f:
                write = csv.writer(f)
                write.writerow([sent[0].lower(),sent[1].lower(),sent[2].lower()])
        print("printed")

    def create_diary(self,user):
        print("users/"+user+"/"+user+"_data.csv")
        with open("users/"+user+"/"+user+"_data.csv", "r") as f:
            read = csv.reader(f)
            diary = []
            for d in read:
                diary.append(d)
        print(diary)
        return diary


    def add_new_verbs(self,diary):
        verbs = []
        with open("resources/qna.csv","r") as f:
            for s in csv.reader(f):
                verbs.append(s[0])
        print(diary)
        for d in diary:
            if d[1].replace(" ","-") not in verbs:
                max = 0
                verb = ""
                for v in verbs:
                    temp = self.nlp(d[1]).similarity(self.nlp(v.replace("-"," ")))
                    if temp > max:
                        max = temp
                        # verb =["like","like-to-play"]
                        verb = [v,d[1].replace(" ","-")]


                with open("resources/qna.csv","r") as f:
                    for s in csv.reader(f):
                        # "like","-each verb in QNA-"
                        print(verb,s)
                        if re.match(verb[0],s[0]):
                            sent = s

                    sent[0] = verb[1]
                    for s in sent:
                        for w in s.split():
                            if re.match(w[0],"/") and not re.match(w,"/word"):
                                sent[1] = sent[1].replace(w,"/"+verb[1])
                                sent[2] = sent[2].replace(w,"/"+verb[1])
                with open("resources/qna.csv","a") as f:
                    write = csv.writer(f)
                    write.writerow(sent)



    # print(users)
    def retrieve_from_diary(self,q,diary,user,asker):
        q = self.nlp(q)
        with open("resources/qna.csv","r") as f:
            max = 0
            ans = ""
            sent = ""
            for s in csv.reader(f):
                # s =["like-to-play","what does /word /like-to-play","who /like-to-play /word"]
                st = s[1]
                for w in s[1].split():
                    # w = /like-to-play
                    if w[0] == "/" and not re.match(w,"/word"):
                        # st = what does /word /like-to-play
                        st = st.replace(w,w[1:])
                        st = st.replace("-"," ")
                        # st = what does /word like to play
                    elif w[0] == "/":
                        st = st.replace(w, w[1:])
                print(st)
                temp = q.similarity(self.nlp(st))
                # print(q,st,q.similarity(nlp(st)))
                if temp>max:
                    max=temp
                    sent = s
                st = s[2]
                for w in s[2].split():
                    if w[0] == "/" and not re.match(w,"/word"):
                        # st = what does /word /like-to-play
                        st = st.replace(w,w[1:])
                        st = st.replace("-"," ")
                        # st = what does /word like to play
                    elif w[0] == "/":
                        st = st.replace(w, w[1:])
                print(st)
                temp = q.similarity(self.nlp(st))
                # print(q,st,q.similarity(nlp(st)))
                if temp>max:
                    max=temp
                    sent = s
            print("09090909",sent)
            # sent = ["like-to-play","what does /word /like-to-play","who /like-to-play /word"]

            max = 0
            for d in diary:
                if re.match(d[1],sent[0]):
                    st = sent[1]
                    for w in sent[1].split():
                        if re.match(w,"/word"):
                            st = st.replace(w,d[0])
                        elif w[0] is "/":
                            st = st.replace(w,w[1:])
                            st = st.replace("-", " ")

                    temp = self.nlp(st).similarity(q)
                    # print(q,"-",st,"-",temp)
                    if temp>max:
                        max=temp
                        ans = d[2]

                    st = sent[2]
                    for w in sent[2].split():
                        if re.match(w,"/word"):
                            st = st.replace(w,d[2])
                        elif w[0] is "/":
                            st = st.replace(w,w[1:])
                            st = st.replace("-", " ")

                    temp = self.nlp(st).similarity(q)
                    # print(q,"-",st,"-",temp)
                    if temp>max:
                        max=temp
                        ans = d[0]

            if max>0.95:
                print("hello",ans,max)
                ans = ans
            else:
                print("hello human",ans,max)
                ans = "No Data"
            print(ans)
            if ans.lower() == "i":
                if re.match(user,asker):
                    print("you")
                    return "You"
                else:
                    print(user)
                    return user
            else:
                print(ans)
                return ans

