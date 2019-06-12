import match
import action
from spacy import load





class main():
    print("Loading Resources...")
    nlp = load('en')
    m = match.match(nlp)
    a = action.action(nlp)
    while True:
        inp = input("Query: ")
        matches = m.find_match(inp.lower(),0.90)
        best_match = m.get_dominant_res(matches)
        act = a.get_action(best_match, inp)
        if act is None:
            print(matches[2])
            act = m.get_da(matches[2])
        print("ANS: ",act)




