from model import Node, Label
import math

def run(d, attributes, threshold):
    return Label("done")

def select_splitting_attribute(d, threshold):
    p0 = entropy(d)

def entropy_ci(category, d):
    D_i = len([t for t in d if t[1] == category])
    D = len(d)
    Pr = D_i/D
    return Pr * math.log2(Pr)

def entropy(d):
    categories = set(t[1] for t in d)
    return -sum(entropy_ci(c, d) for c in categories)

def entropy_wrt(d, attr):
    values = set(t[0][attr] for t in d)
    def entropy_j(j):
        Dj = [t for t in d if t[0][attr] == j]
        return len(Dj)/len(d) * entropy(Dj)
    return sum([entropy_j(j) for j in values])

