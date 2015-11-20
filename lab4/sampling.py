import random

def precision(expected, actual, positive):
    # expected = correct label
    # actual = predicted label
    paired = list(zip(expected, actual))
    TP = sum(1 for e, a in paired if e == positive and a == positive)
    FP = sum(1 for e, a in paired if e != positive and a == positive)
    return TP / (TP + FP)

def recall(expected, actual, positive):
    paired = list(zip(expected, actual))
    TP = sum(1 for e, a in paired if e == positive and a == positive)
    FN = sum(1 for e, a in paired if e == positive and a != positive)
    return TP / (TP + FN)

def pf(expected, actual, positive):
    paired = list(zip(expected, actual))
    FP = sum(1 for e, a in paired if e != a and a == positive)
    TN = sum(1 for e, a in paired if e == a and a != positive)
    return FP / (FP + TN)

def f_measure(expected, actual, positive):
    prec = precision(expected, actual, positive)
    rec = recall(expected, actual, positive)
    return (2 * prec * rec) / (prec + rec)

def accuracy(expected, actual):
    paired = list(zip(expected, actual))
    Dtrue = sum(1 for e, a in paired if e == a)
    return float(Dtrue) / float(len(expected))

def error_rate(expected, actual):
    return 1 - accuracy(expected, actual)

def hunk(data, hunksize):
    if hunksize == 0:
        return [data]
    if hunksize == -1:
        return [[i] for i in data]
    hunkable = list(data)
    random.shuffle(hunkable)
    hunks = []
    for start in range(0, len(data), hunksize):
        hunks.append(hunkable[start:start + hunksize])
    return hunks

def pull_each(data):
    """ Returns an iterator over data which returns pairs consisting
    of each element paired with a list containing all the other
    elements of data"""
    return ((i, [j for j in data if j != i]) for i in data)
