from model import Node, Label
import math
import itertools

def run(d, attributes, threshold):
    maybeLeaf = has_single_class(d)
    if maybeLeaf:
        return maybeLeaf
    else:
        maybeLeaf = has_no_attrib(d)
        if maybeLeaf:
            return maybeLeaf
        else:
            Ag = select_splitting_attribute_idx(d, len(attributes), threshold)
            if not Ag:
                return Label(find_most_frequent_label(d))
            else:
                dom = set(t[0][Ag] for t in d)
                nodes = []
                for v in dom:
                    Dv = [t for t in d if t[Ag] == v]
                    if len(Dv) > 0:
                        nodes.append((Ag, run(Dv, set(attributes) - set([Ag]), threshold)))
                return Node(Ag, *nodes)

def select_splitting_attribute_idx(d, attr_count, threshold):
    p0 = entropy(d)
    p = [entropy_wrt(d, i) for i in range(attr_count)]
    gain = [p0 - p[i] for i in range(attr_count)]
    idx = idx_of_max(gain)
    if idx and gain[idx] > threshold:
        return idx
    else:
        return

def entropy_ci(cat, d):
    D_i = sum(1 for t in d if category(t) == cat)
    D = len(d)
    Pr = D_i/D
    return Pr * math.log2(Pr)

def entropy(d):
    categories = set(category(t) for t in d)
    return -sum(entropy_ci(c, d) for c in categories)

def entropy_wrt(d, attr_idx):
    value_sets = []
    def keyfunc(t):
        return attrib(t)[attr_idx]
    data = sorted(d, key=keyfunc)
    for value, all_values in itertools.groupby(data, keyfunc):
        value_sets.append(list(all_values))
    return sum(len(Dj)/len(d) * entropy(Dj) for Dj in value_sets)

def has_single_class(D):
    cls = D[0][1]
    for d in D:
        if d[1] != cls:
            return None
    return Label(cls)

def find_most_frequent_label(D):
    classes = {}
    for d in D:
        cls = category(d)
        if cls in classes:
            classes[cls] += 1
        else:
            classes[cls] = 1
    return idx_of_max(classes, classes.keys())

def has_no_attrib(D, attributes):
    if len(attributes) == 0:
        maxKey = find_most_frequent_label(D)
        return Label(maxKey)
    else:
        return None
    
def idx_of_max(lst, keys=None):
    length = len(lst)
    if length == 0:
        return None

    if not keys:
        keys = range(length)

    maxKey = None
    maxVal = float('-inf')
    for key in keys:
        val = lst[key]
        if val > maxVal:
            maxVal = val
            maxKey = key
    return maxKey

def first(lst):
    return lst[0]

def attrib(pair):
    return pair[0]

def category(pair):
    return pair[1]
