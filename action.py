from web_crawler.web_requests import ask_requests,ddg_requests,countries
from mathop import mathop
import re

class action:
    nlp = None
    def __init__(self,nlp):
        self.nlp = nlp


    def get_action(self,match,inp):
        if match is None:
            return None
        elif match[3] is "$":
            return match[4]
        elif match[3] is "*":
            return self.get_star(match,inp)
        else:
            return self.get_type(match,inp)


    def get_star(self,match,inp):
        ext,out = set(),[]
        inpp = inp
        inp = self.nlp(inp.replace("?",""))
        ip = "".join([t[1:] for t in match[2].split() if t[0] is "\\"])
        ip = ip.split("-")
        for w in inp.noun_chunks:
            for i in ip:
                if w.similarity(self.nlp(i))>0.30 and i not in inpp.split():
                    ext.add(w.text)
        ext = " ".join(ext)
        for w in match[4].split():
            if w[0] is "\\":
                out.append(ext.title())
            else:
                out.append(w)
        return " ".join(out)


    def get_type(self,match,inp):
        # print()
        if match[3] in dir(ask_requests):
            ext = set()
            ar = ask_requests()
            inp = self.nlp(inp.replace("?",""))
            ip = "".join([t[1:] for t in match[2].split() if t[0] is "\\"])
            if ip is not "":
                ip = ip.split("-")
                for w in inp:
                    for i in ip:
                        if w.similarity(self.nlp(i))>0.40:
                            ext.add(w.text)
                ext = " ".join(ext)
            else:
                ext = None
            op = getattr(ar,match[3])(ext)
            if op is not None:
                out = []
                for w in match[4].split():
                    if re.match(r"\\q",w):
                        out.append(ext)
                    elif re.match(r"\\res",w):
                        out.append(op)
                    else:
                        out.append(w)
                return " ".join(out)
            else:
                return None

        elif match[3] in dir(countries):
            # print("countries")
            ext = set()
            ar = countries()
            inp = self.nlp(inp.replace("?",""))
            ip = "".join([t[1:] for t in match[2].split() if t[0] is "\\"])
            if ip is not "":
                ip = ip.split("-")
                for w in inp:
                    for i in ip:
                        if w.similarity(self.nlp(i))>0.40:
                            ext.add(w.text)
                ext = " ".join(ext)
            else:
                ext = None

            op = getattr(ar,match[3])(ext)
            if op is not None:
                out = []
                for w in match[4].split():
                    if re.match(r"\\q",w):
                        out.append(ext)
                    elif re.match(r"\\res",w):
                        out.append(op)
                    else:
                        out.append(w)
                return " ".join(out)
            else:
                return None

        elif match[3] in dir(ddg_requests):
            ddg = ddg_requests()
            return getattr(ddg,match[3])(inp)

        elif match[3] in dir(mathop):
            mat = mathop()
            ext = [i for i in inp.split() if i.isdigit()]
            if len(ext) == 1:
                return getattr(mat, match[3])(int(ext[0]))
            elif len(ext) == 2:
                return getattr(mat, match[3])(int(ext[0]), int(ext[1]))


        else:
            print(match[2])

