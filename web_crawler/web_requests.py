import requests
from bs4 import BeautifulSoup as bs
from duckduckpy import query
import wikipedia
import re

class countries():
    def get_cap(self,inp):
        # print("{{{{{{",inp,"}}}}}}}")
        appl = wikipedia.page(inp).html()
        soup = bs(appl, 'lxml')
        web_res = soup.find_all("th", {"scope": "row"})
        for w in web_res:
            if re.match("Capital", w.text):
                return w.parent.find("a").text

    def get_area(self,inp):
        appl = wikipedia.page(inp).html()
        soup = bs(appl, 'lxml')
        web_res = soup.find_all("th", {"scope": "row"})
        res=[]
        for w in web_res:
            if re.match("• Total", w.text):
                res.append(w.parent.find("td").text)
        return res[0]

    def get_cur(self,inp):
        appl = wikipedia.page(inp).html()
        soup = bs(appl, 'lxml')
        web_res = soup.find_all("th", {"scope": "row"})
        for w in web_res:
            if re.match("Currency", w.text):
                return w.parent.find("td").text

    def get_gdp(self,inp):
        appl = wikipedia.page(inp).html()
        soup = bs(appl, 'lxml')
        web_res = soup.find_all("th", {"scope": "row"})
        res=[]
        for w in web_res:
            if re.match("• Total", w.text):
                res.append(w.parent.find("td").text)
        return res[1]

    def get_cc(self,inp):
        appl = wikipedia.page(inp).html()
        soup = bs(appl, 'lxml')
        web_res = soup.find_all("th", {"scope": "row"})
        for w in web_res:
            if re.match("Calling code", w.text):
                return w.parent.find("td").text

class ddg_requests():
    def get_info(self,inp):
        q = query(inp)
        return q.abstract

class ask_requests():
    def get_time(self,ext):
        if ext is None:
            q = "current+time"
        else:
            q = "current+time+in+"+ext
        req = requests.get("http://www.ask.com/web?q="+q)
        soup = bs(req.content,'lxml')
        web_res_hour = soup.find("span",{"id":"sa_time_ctHours"})
        web_res_min = soup.find("span",{"id":"sa_time_ctMinutes"})
        if web_res_hour is not None:
            return web_res_hour.text+":"+web_res_min.text
        else:
            return None

    def get_date(self,ext):
        if ext is None:
            q = "current+time"
        else:
            q = "current+time+in+"+ext
        req = requests.get("http://www.ask.com/web?q="+q)
        soup = bs(req.content,'lxml')
        web_res = soup.find("div",{"id":"sa_time_ctDate"})
        if web_res is not None:
            return web_res.text
        else:
            return None

    def get_day(self,ext):
        req = requests.get("http://www.ask.com/web?q=current+time")
        soup = bs(req.content,'lxml')
        web_res = soup.find("div",{"id":"sa_time_ctWeekday"})
        if web_res is not None:
            return web_res.text
        else:
            return None

    def get_temp(self,ext):
        if ext is None:
            q = "current+temperature"
        else:
            q = "current+temperature+in+"+ext
        req = requests.get("http://www.ask.com/web?q="+q)
        soup = bs(req.content,'lxml')
        web_res = soup.find("span",{"class":"sa_current_reading"})
        if web_res is not None:
            return web_res.text
        else:
            return None

