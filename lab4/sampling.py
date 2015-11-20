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
