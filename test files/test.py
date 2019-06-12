import wikipedia
import re
import requests
from bs4 import BeautifulSoup as bs
# while True:
#     q = input(">>")
#     q = q.replace(" ","+")
#     req = requests.get("http://www.ask.com/web?q="+q)
#
#     soup = bs(req.content,'lxml')
#     web_res = soup.find("span",{"class":"sa_headline"})
#
#     try:
#         print(web_res.text)
#     except:
#         print("Not found")


a = wikipedia.search("Apple")

def get_cap(inp):
    appl = wikipedia.page(inp).html()
    res,rez = [],[]
    soup = bs(appl,'lxml')
    web_res = soup.find_all("th",{"scope":"row"})
    # for w in web_res:
    #     print(w.text)
    for w in web_res:
        if re.match("Capital",w.text):
            print("capital: ",w.parent.find("a").text)

        if re.match("• Total", w.text):
            res.append(w.parent.find("td").text)
        if re.match("Currency", w.text):
            rez.append(w.parent.find("td").text)
        if re.match("Calling code", w.text):
            print("Calling code",w.parent.find("td").text)
    print("currency",rez[0])

    print("area: ", res[0])
    print("gdp: ", res[2])
#
# appl = wikipedia.page("india").html()
# soup = bs(appl,'lxml')
# web_res = soup.find_all("th",{"scope":"row"})
# res=[]
# for w in web_res:
#     if re.match("• Total",w.text):
#         res.append(w.parent.find("td").text)
#
# print("area: ",res[0])
# print("gdp: ",res[1])
#

'''
import requests
from bs4 import BeautifulSoup as bs

req = requests.get("http://www.ask.com/web?q=37+celcius+to+farenheit")

soup = bs(req.content,'lxml')
#about some one / get from ddg instead
web_res = soup.find("div",{"class":"sa_abstract"})
#stock quote
web_res1 = soup.find("span",{"class":"sa_stk_quote"})
#conversions
web_res2 = soup.find("span",{"class":"sa_headline"})
#weather reading
web_res3 = soup.find("span",{"class":"sa_current_reading"})

print(web_res)
print(web_res1)
print(web_res2)
print(web_res3)



js_text = soup.find_all()
for j in js_text:
    print(j.text)
'''
