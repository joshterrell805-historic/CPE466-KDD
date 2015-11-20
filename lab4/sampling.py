def precision(expected, actual, positive):
    paired = list(zip(expected, actual))
    TP = sum(1 for e, a in paired if e == a and a == positive)
    FP = sum(1 for e, a in paired if e != a and a == positive)
    return TP / (TP + FP)

def recall(expected, actual, positive):
    paired = list(zip(expected, actual))
    TP = sum(1 for e, a in paired if e == a and a == positive)
    FN = sum(1 for e, a in paired if e != a and a != positive)
    return TP / (TP + FN)

def accuracy(expected, actual):
    paired = list(zip(expected, actual))
    Dtrue = sum(1 for e, a in paired if e == a)
    return float(Dtrue) / float(len(expected))

