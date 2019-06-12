from spacy import load
from similarity import sent_sim
nlp = load('en')


a = {"I like to dance":["who likes to dance","what do I like to do","what do i like"],"she makes me laugh":["who makes me laugh"],
     "patient was 40 years old":["how old was patient","who was 40 years old"]}
b = ""

b = nlp(b)
max = 0
for l in list(a.keys()):
    temp = sent_sim(b,nlp(l))
    if temp > max:
        max = temp
        max_sent = l
print(max_sent,max)
q = ["who likes to party","what does she like to do","what does she like","when does she dance","how does she dance","where does she dance"]
cq = set()
for i in q:
    for j in a[str(max_sent)]:
        temp = nlp(j).similarity(nlp(i))
        if temp > 0.85:
            cq.add(i)
print(cq)

# a = "she likes to party"
# b = "who like to "

# for i in a.split():
#     if i not in b.split():
#         print(i,end=" ")