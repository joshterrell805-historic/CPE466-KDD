from model import Node, Label
import math
import itertools

def run(d, attributes, threshold):
    maybeLeaf = has_single_class(d)
    if maybeLeaf:
        print("Found only one class")
        return maybeLeaf
    elif len(attributes) == 0:
        print("No attributes left")
        return Leaf(find_most_frequent_label(d))
    else:
            splitting_attr = select_splitting_attribute_heading(d, list(attributes), threshold)
            if not splitting_attr:
                print("No attribute suitable to split from {}".format(str(attributes)))
                return Label(find_most_frequent_label(d))
            else:
                print("Splitting on ", splitting_attr)
                Ag = splitting_attr[0]
                domain_Ag = set(attrib(t)[Ag] for t in d)
                nodes = []
                for value in domain_Ag:
                    Dv = [t for t in d if attrib(t)[Ag] == value]
                    if len(Dv) > 0:
                        reduced_attrs = list(attributes)
                        reduced_attrs.remove(splitting_attr)
                        nodes.append((value, run(Dv, reduced_attrs, threshold)))
                return Node(splitting_attr[1], *nodes)

def select_splitting_attribute_heading(d, attrs, threshold):
    attr_idxs = [a[0] for a in attrs]
    p0 = entropy(d)
    p = [entropy_wrt(d, i) for i in attr_idxs]
    gain = [p0 - p[i] for i in range(len(attr_idxs))]
    idx = idx_of_max(gain)
    if idx != None and gain[idx] > threshold:
        return attrs[idx]
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
    tag = category(first(D))
    for d in D:
        if category(d) != tag:
            return None
    return Label(tag)

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
