from diary import diary
from spacy import load
nlp = load("en")
#
d = diary(nlp)
dia = d.get_entries("karan")
print(d.loop_qs("what was patient suffering from",dia))