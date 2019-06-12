from spacy import load
from similarity import sent_sim


nlp = load('en')

while True:
    w = nlp(input(">"))
    y = nlp(input(">>"))



'''

sen = ["A nova was killed by me","i killed a nova.","i went to her house.","she likes apple.","i like coffee.","dodo likes to dance"]

while True:
    w = nlp(input(">"))
    print([(a,a.pos_,a.tag_) for a in w])
    print([a for a in w.noun_chunks],end=" ")
    print([a for a in w if a.pos_ is "VERB"])






db = "do you like \\coffee"
dbn = nlp(db.replace("\\",""))
print(dbn)
inpa = ["do you like coffee","do you like beer","is this beer liked by you","is coffee to you liking","do you like ice tea","do you like cold coffee","do you like ship","do you like this potato","is coffee liked by you","is cold coffee to you liking","is cold coffee liked by you", "is ice tea liked by you"]

for inp in inpa:
    inp = nlp(inp)
    print(inp,end=" - ")
    print("a:",sent_sim(dbn,inp),end=" - ")
    print("b:",dbn.similarity(inp),end=" - ")
    print("avg:",(sent_sim(dbn,inp)+dbn.similarity(inp))/2,end=" - ")

    i = nlp("".join([t[1:] for t in db.split() if t[0] is "\\"]))

    for w in inp:
        if w.similarity(i)>0.30:
            print("Extract:",w,end=" ")

    print("")

'''
