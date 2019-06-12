from scipy import spatial
ALPHA = 0.4

def sent_sim(sent1,sent2):
    uniq_set = [w for w in sent1]
    uniq_set = uniq_set + [w for w in sent2 if w.text not in [str(t) for t in uniq_set]]
    sent1_vec,sent2_vec = [],[]

    for w in uniq_set:
        if w.text in [str(t) for t in sent1]:
            sent1_vec.append(1.0)

        else:
            max=0
            for r in sent1:
                temp = w.similarity(r)
                if temp > max:
                    max = temp
            if max>ALPHA:
                sent1_vec.append(max)
            else:
                sent1_vec.append(0.0)

    for w in uniq_set:
        if w.text in [str(t) for t in sent2]:
            sent2_vec.append(1.0)
        else:
            max=0
            for r in sent2:
                temp = w.similarity(r)
                if temp > max:
                    max = temp
            if max > ALPHA:
                sent2_vec.append(max)
            else:
                sent2_vec.append(0.0)

    result1 = 1 - spatial.distance.cosine(sent1_vec,sent2_vec)
    result2 = sent1.similarity(sent2)
    return (result1+result2)/2
